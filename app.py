from flask import Flask, request, jsonify

from pipe._0ingestion import fetch_files
from pipe._1cleaning import cleaning
# from pipe._2transform import 
# from pipe._4report import 
# from pipe._3check import 

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
        # transformed_dataframes = transform(cleaned_dataframes)

        # Step 4: Metadata and Reporting
        # report = generate_summary_report(transformed_dataframes)
        # data_quality_checks(transformed_dataframes)

        return jsonify({
            "message": "Pipeline executed successfully",
            # "report": report.to_dict(orient="records"),
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
