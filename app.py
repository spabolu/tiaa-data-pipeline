from io import BytesIO
import zipfile
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from aws.s3 import get_s3
from pipe._0ingestion import fetch_files
from pipe._1cleaning import cleaning
# from pipe._2transform import transform
# from pipe._3check import data_quality_checks
# from pipe._4report import generate_summary_report

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/pipeline', methods=['POST'])
def pipeline():
    try:
        data = request.get_json()
        bucket_name = data.get('bucket')
        file_keys = data.get('file_keys', [])

        if not bucket_name or not file_keys:
            return jsonify({"error": "Invalid input. 'bucket' and 'file_keys' are required."}), 400

        # Step 1: Ingestion
        ingested_files = fetch_files(bucket_name, file_keys)

        # Step 2: Cleaning
        cleaned_dataframes = cleaning(ingested_files)

        # Steps 3 and 4: Transformation and Reporting (commented for now)
        # transformed_dataframes = transform(cleaned_dataframes)
        # report = generate_summary_report(transformed_dataframes)
        # data_quality_checks(transformed_dataframes)

        return jsonify({"message": "Pipeline executed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_to_existing_bucket():
    # Handle OPTIONS (preflight) requests
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file.filename is None or not file.filename.endswith(".zip"):
        return jsonify({"error": "Only .zip files are allowed"}), 400

    # Secure the filename
    filename = secure_filename(file.filename)

    # Use an existing bucket name from environment variable
    bucket_name = "saketh-fat-bucket"
    
    try:
        # Initialize S3 client
        s3_client = get_s3()

        # Step 1: Delete all existing files in the bucket
        try:
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            if "Contents" in objects:
                keys = [{"Key": obj["Key"]} for obj in objects["Contents"]]
                s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={"Objects": keys}
                )
        except ClientError as e:
            return jsonify({"error": f"Failed to delete existing files: {str(e)}"}), 500

        # Step 2: Extract the .zip file
        try:
            file_content = BytesIO(file.read())
            with zipfile.ZipFile(file_content) as z:
                for zipped_file in z.namelist():
                    if zipped_file.endswith("/"):
                        continue  # Skip directories
                    file_data = z.read(zipped_file)  # Read the file contents
                    s3_client.put_object(
                        Bucket=bucket_name,
                        Key=zipped_file,  # Use the file's name as the key
                        Body=file_data
                    )
        except zipfile.BadZipFile:
            return jsonify({"error": "The uploaded file is not a valid .zip archive"}), 400

        return jsonify({
            "message": f"Contents of '{filename}' uploaded successfully to bucket '{bucket_name}'."
        }), 200

    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the Data Pipeline API!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
