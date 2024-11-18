from datetime import datetime
from io import BytesIO
import time
from dotenv import load_dotenv
import zipfile
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from aws.s3 import get_s3

from pipe._0ingestion import fetch_files
from pipe._1cleaning import cleaning
from pipe._2transform import transform

from pipe._5storage import Populate_RDS

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Initialize Flask app
app = Flask(__name__)
# Configure CORS to allow all origins, methods, and headers
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": "*",
        "expose_headers": "*",
        "supports_credentials": True
    }
})
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def emit_progress(step_name, status, description=None):
    """Helper function to emit progress updates"""
    socketio.emit('pipeline_update', {
        'step': step_name,
        'status': status,
        'description': description,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/pipeline', methods=['POST', 'GET', 'OPTIONS'])
def pipeline():
    try:
        data = request.get_json()
        bucket_name = data.get('bucket')
        file_keys = data.get('file_keys', [])
        folder_name = file_keys[0].split('/')[0]

        if not bucket_name or not file_keys:
            return jsonify({"error": "Invalid input. 'bucket' and 'file_keys' are required."}), 400

        # Step 1: Ingestion
        emit_progress("Data Ingestion", "in_progress", "Starting data ingestion...")
        ingested_files = fetch_files(bucket_name, file_keys)
        # time.sleep(2)  # Simulated work
        emit_progress("Data Ingestion", "completed", "Successfully ingested files")

        # Step 2: Cleaning
        emit_progress("Data Cleaning", "in_progress", "Starting data cleaning...")
        cleaned_dataframes = cleaning(ingested_files)
        # time.sleep(2)  # Simulated work
        emit_progress("Data Cleaning", "completed", "Successfully cleaned data")

        # Step 3: Analysis
        emit_progress("Data Analysis", "in_progress", "Starting analysis...")
        transformed_dataframes = transform(cleaned_dataframes)
        # time.sleep(2)  # Simulated work
        emit_progress("Data Analysis", "completed", "Analysis completed")

        # Step 4: Insight Generation
        emit_progress("Insight Generation", "in_progress", "Generating insights...")
        # add next step code here
        # time.sleep(2)  # Simulated work
        emit_progress("Insight Generation", "completed", "Insights generated")

        # Step 5: Distribution
        emit_progress("Distribution", "in_progress", "Preparing distribution...")
        Populate_RDS(transformed_dataframes, folder_name)
        # time.sleep(1)  # Simulated work
        emit_progress("Distribution", "completed", "Pipeline completed successfully")

        return jsonify({"message": "Pipeline executed successfully"}), 200

    except Exception as e:
        socketio.emit('pipeline_error', {'error': str(e)})
        return jsonify({"error": str(e)}), 500

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_to_existing_bucket():
    # Remove the manual CORS handling since we have global CORS config
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file.filename is None or not file.filename.endswith(".zip"):
        return jsonify({"error": "Only .zip files are allowed"}), 400

    filename = secure_filename(file.filename)
    bucket_name = "sparky-pipeline-input"
    
    try:
        s3_client = get_s3()

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

        file_keys = []
        try:
            file_content = BytesIO(file.read())
            with zipfile.ZipFile(file_content) as z:
                for zipped_file in z.namelist():
                    if zipped_file.endswith("/"):
                        continue
                    file_data = z.read(zipped_file)
                    s3_client.put_object(
                        Bucket=bucket_name,
                        Key=zipped_file,
                        Body=file_data
                    )
                    file_keys.append(zipped_file)
        except zipfile.BadZipFile:
            return jsonify({"error": "The uploaded file is not a valid .zip archive"}), 400

    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the Data Pipeline API!"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)