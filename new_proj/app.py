from flask import Flask, request, jsonify
from src.ingestion import fetch_files
from src.cleaning import cleaning
from src.transform import transform
from src.metadata import retrieve_metadata, query_metadata_by_column
from src.report import generate_summary_report
from src.check import data_quality_checks

app = Flask(__name__)

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
        transformed_dataframes = transform(cleaned_dataframes)

        # Step 4: Metadata and Reporting
        report = generate_summary_report(transformed_dataframes)
        data_quality_checks(transformed_dataframes)

        return jsonify({
            "message": "Pipeline executed successfully",
            "report": report.to_dict(orient="records"),
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
