from datetime import datetime
import pytz
from io import BytesIO
import time
from dotenv import load_dotenv
import zipfile
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from aws.s3 import get_s3

from pipe._0ingestion import fetch_files
from pipe._1cleaning import cleaning
from pipe._2transform import transform

from pipe._5storage import Populate_RDS
from pipe._6metadata import Populate_Metadata

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

class PipelineTimer:
    def __init__(self):
        self.start_time = None
        self.stage_times = {}
        self.current_stage = None

    def start_stage(self, stage_name):
        self.current_stage = stage_name
        self.start_time = time.time()

    def end_stage(self):
        if self.start_time and self.current_stage:
            elapsed_time = time.time() - self.start_time
            self.stage_times[self.current_stage] = round(elapsed_time * 1000)  # Convert to milliseconds
            self.start_time = None
            return self.stage_times[self.current_stage]
        return 0

timer = PipelineTimer()

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

arizona_tz = pytz.timezone('America/Phoenix')

def emit_progress(step_name, status, description=None, elapsed_time=None):
    """Helper function to emit progress updates with timing"""
    socketio.emit('pipeline_update', {
        'step': step_name,
        'status': status,
        'description': description,
        'timestamp': datetime.now(arizona_tz).isoformat(),
        'elapsed_time': elapsed_time
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

        # Reset timer for new pipeline run
        timer.stage_times.clear()

        # Step 0: Ingestion
        timer.start_stage("Data Ingestion")
        emit_progress("Data Ingestion", "in_progress", "Starting data ingestion...")
        ingested_files = fetch_files(bucket_name, file_keys)
        elapsed = timer.end_stage()
        emit_progress("Data Ingestion", "completed", "Successfully ingested files", elapsed)

        # Step 1: Cleaning
        timer.start_stage("Data Cleaning")
        emit_progress("Data Cleaning", "in_progress", "Starting data cleaning...")
        # cleaned_dataframes = cleaning(ingested_files)
        time.sleep(2)  # Simulated work (REMOVE IN PROD)
        elapsed = timer.end_stage()
        emit_progress("Data Cleaning", "completed", "Successfully cleaned data", elapsed)

        # Step 2: Analysis
        timer.start_stage("Data Analysis")
        emit_progress("Data Analysis", "in_progress", "Starting analysis...")
        transformed_dataframes = transform(ingested_files)
        elapsed = timer.end_stage()
        emit_progress("Data Analysis", "completed", "Analysis completed", elapsed)

        # Step 4: Insight Generation
        timer.start_stage("Insight Generation")
        emit_progress("Insight Generation", "in_progress", "Generating insights...")
        time.sleep(2)  # Simulated work
        elapsed = timer.end_stage()
        emit_progress("Insight Generation", "completed", "Insights generated", elapsed)

        # Step 5/6: distribution/metadata
        timer.start_stage("Distribution")
        emit_progress("Distribution", "in_progress", "Preparing distribution...")
        Populate_RDS(transformed_dataframes, folder_name)
        Populate_Metadata(transformed_dataframes, folder_name)
        elapsed = timer.end_stage()
        emit_progress("Distribution", "completed", "Pipeline completed successfully", elapsed)

        return jsonify({
            "message": "Pipeline executed successfully",
            "timing": timer.stage_times
        }), 200

    except Exception as e:
        socketio.emit('pipeline_error', {'error': str(e)})
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_to_existing_bucket():
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

@app.route('/download_report', methods=['GET'])
def download_report():
    """Endpoint to download the business report PDF"""
    try:
        # Ensure the file path is correct
        pdf_path = './business_report.pdf'  # Adjust this path as needed
        
        # Serve the PDF file
        return send_file(pdf_path, as_attachment=True, mimetype='application/pdf')
    except FileNotFoundError:
        return jsonify({"error": "File not found. Please ensure 'business_report.pdf' exists in the specified path."}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the Data Pipeline API!"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)