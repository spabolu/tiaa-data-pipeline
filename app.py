from dotenv import load_dotenv
import os
import boto3
import pandas as pd
from io import StringIO
from flask import Flask, request, jsonify
from genai_client import GenAIClient

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_selected_files():
    try:
        data = request.get_json()
        bucket_name = data.get('bucket')
        file_keys = data.get('file_keys', [])
        if not bucket_name or not file_keys:
            return jsonify(error="Invalid input. 'bucket' and 'file_keys' are required."), 400
    except Exception as e:
        return jsonify(error=f"Failed to parse JSON input: {str(e)}"), 400

    # Create a new AWS session
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name="us-east-1",
    )

    s3 = session.client('s3')
    
    try:
        dataframes = []
        for file in file_keys:
            try:
                obj = s3.get_object(Bucket=bucket_name, Key=file)
                if file.endswith('.xlsx'):
                    df = pd.read_excel(obj['Body'])
                    dataframes.append({"name" : file, "dataframe" : df})
                if file.endswith('.csv'):
                    df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
                    dataframes.append({"name" : file, "dataframe" : df})
            except Exception as e:
                print(f"Failed to process file: {str(e)}")
                
        datacleaning(dataframes)
        return jsonify({
            "message" : "Data Cleaning Finished"
        })

    except Exception as e:
        return jsonify(error=str(e)), 500
    

def datacleaning(dataframes):
    genai = GenAIClient()
    
    for entry in dataframes:
        print(f"DataFrame {entry['name']}:\n{entry['dataframe'].head(10)}\n")
        
        llm_prompt_data_cleaning = '''
        “I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one. Assume I already imported the dataframes to directly use. Can you generate a Python script that performs relevant data preprocessing on these dataframes?
        Apply data cleaning and preprocessing techniques only if the dataframe exhibits the following issues:
        1. Duplicate Entries
            •	Duplicate rows in their entirety.
            •	Duplicate rows based on a specific subset of columns.
            •	Duplicate rows ignoring case sensitivity in string columns.
            •	Duplicate values due to trailing or leading whitespaces in text data.
            •	Duplicate rows with minor differences caused by inconsistent formatting (e.g., different cases or extra spaces).
            •	Near-duplicates identified by domain-specific logic (e.g., names with small spelling variations).
        2. Inconsistent Formatting
            •	Negative values where they do not make logical sense (e.g., age, income, counts, or categorical values that should not include negative signs). In this case, fix the value to be appropriate by removing the negative sign.
            •	Text inconsistency in categorical fields (e.g., “Male” vs. “male”).
            •	Numerical columns stored as strings (e.g., “100.5” as text instead of float).
            •	Date columns with mixed formats (e.g., “MM/DD/YYYY” and “YYYY-MM-DD”).
            •	Irregular capitalization in text columns (e.g., “New York” vs. “new york”).
            •	Unnecessary special characters or trailing/leading whitespaces in text fields.
        3. Inconsistent Data Types
            •	Float values in integer columns.
            •	Strings in numeric columns (e.g., “100.5” stored as a string).
            •	Mixed types in categorical fields (e.g., numbers and strings in the same column).
            •	Date columns stored as strings instead of proper datetime objects.
            •	Boolean fields represented inconsistently (e.g., “True”, “false”, 1, 0).
            •	Columns with mixed types due to data entry errors.
        If a specific header/attribute/column is important to the context of the dataframe, do not make updates to the values of that header/attribute/column. For example: if the racial background, test score, credit score, bonuses, etc., of an employee is unknown, do not set a value in place of it.
        Keep prompting until the output is executable and there is no error in the Python code provided.
        Generate a Python script that applies these cleaning and preprocessing techniques to the dataframes, prints out the head of each dataframe with 10 rows after cleaning, and ensures dependencies between columns are maintained. Only respond with the code because I will directly run your response. Do not include markdown formatting like ```py. Do not include anything else.”
        '''
        
        # exec('''pip install pandas''')
        # Duplicates, Inconsistent Formatting, Data Types
        # Inconsistent formatting within the
        # column/heading/attribute, or inconsitent data types within the column/heading/attribute.
        
        for entry in dataframes:
            name, df = entry['name'], entry['dataframe']
            llm_prompt_data_cleaning += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"
        
        while True:
            # Send prompt to the LLM and get a response
            response = genai.generate_response(llm_prompt_data_cleaning)
            if response:
                # Print the response in red (error highlighting)
                print("\033[91m" + response + "\033[0m")
                # Attempt to execute the generated code
                try:
                    exec(response)
                    print("Code executed successfully!")
                    break  # Exit loop if the code is executed without errors
                except Exception as e:
                    print(f"Error executing generated code: {e}")
                    # If error occurs, ask the LLM to adjust the code and retry
                    llm_prompt_data_cleaning += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\n"
            else:
                print("No response from LLM. Retrying...")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG'))
