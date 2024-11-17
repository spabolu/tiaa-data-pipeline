import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from aws.s3 import get_s3

from pipe._0ingestion import fetch_files
from pipe._1cleaning import cleaning
# from pipe._2transform import 
# from pipe._3check import 
# from pipe._4report import 

load_dotenv(dotenv_path=".env.local")
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

        # Step 3: Transformation
        # transformed_dataframes = transform(cleaned_dataframes)

        # Step 4: Metadata and Reporting
        # report = generate_summary_report(transformed_dataframes)
        # data_quality_checks(transformed_dataframes)

        return jsonify({
            "message": "Pipeline executed successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_unique_bucket_name(base_name: str) -> str:
    """Generate a unique S3 bucket name."""
    unique_suffix = uuid.uuid4().hex[:8]  # Generate a random suffix
    return f"{base_name}-{unique_suffix}"

@app.route("/upload", methods=["POST"])
def upload_and_create_bucket():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file.filename is None or not file.filename.endswith(".zip"):
        return jsonify({"error": "Only .zip files are allowed"}), 400

    # Secure the filename
    filename = secure_filename(file.filename)

    try:
        # Generate a unique bucket name
        base_bucket_name = "uploaded-files"
        unique_bucket_name = create_unique_bucket_name(base_bucket_name)

        # Create the new S3 bucket
        get_s3.create_bucket(
            Bucket=unique_bucket_name,
            CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_S3_REGION")},
        )

        # Upload the file to the new bucket
        get_s3.upload_fileobj(file, unique_bucket_name, filename)

        return jsonify({
            "message": f"File '{filename}' uploaded successfully!",
            "bucket_name": unique_bucket_name,
        }), 200

    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
