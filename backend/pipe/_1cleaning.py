from llm.gait import gAit
import pandas as pd
from datetime import datetime
import io
import sys
def cleaning(dataframes):
    ai = gAit()

    qualityCheckBeforeText = ""
    for entry in dataframes:
        print(f"DataFrame {entry['name']}:\n{entry['dataframe'].head(10)}\n")
        qualityCheckBeforeText = "Quality Check Before Pipeline:\n\n"
    # Create a list of dictionaries, each containing the name and corresponding DataFrame


    for entry in dataframes:
        df = entry["dataframe"]  # Extract the DataFrame
        # Drop unnamed columns (where column names are None, '', or contain 'Unnamed')
        entry["dataframe"] = df.drop(columns=[col for col in df.columns if col is None or col == '' or 'Unnamed' in str(col)])
        df = df.drop_duplicates()

        print(f"DataFrame {entry['name']}:\n{entry['dataframe'].head(10)}\n")
        
    tempDataframes = dataframes.copy()

    llm_prompt_data_quality_check = """
    I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one.
    Don’t drop any unnamed columns. Assume I already imported the dataframes and their variables to directly use.

    Generate a Python script that does NOT include markdown formatting, ```python, in the python script. 
    This python script should provide code to find the number of NA values, duplicate entries, and statistics data to display the overall quality of a specific file.
    Provide a 1 sentence description of how each file should be changed to improve. 
    Provide these details for each specific file. Make the output as only plain text. No JSON should be in this text.
    Give me ONLY Python code and nothing else. I will be running this code directly. Remove Markdown text from the beginning and end of the script. 
    """

    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_quality_check += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    # response = genai.generate_response(llm_prompt_data_quality_check)    
    # exec(response)
    # qualityCheckBeforeText += response
    # print(qualityCheckBeforeText+"\n\n")

    response = ai.ask_llm(llm_prompt_data_quality_check)

    # Clean up the generated script to remove unsupported arguments
    response = response.replace("datetime_is_numeric=True", " ") if response is not None else ""    

    # Capture the output of the generated code
    output_capture = io.StringIO()
    sys.stdout = output_capture  # Redirect stdout

    # Execute the cleaned-up generated code
    exec(response)

    # Reset stdout to normal
    sys.stdout = sys.__stdout__

    # Append captured output to the qualityCheckBeforeText
    qualityCheckBeforeText += output_capture.getvalue()

    # Print the final quality check text
    return qualityCheckBeforeText

        # prompt = '''
        #     “I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one. Assume I already imported the dataframes to directly use. Can you generate a Python script that performs relevant data preprocessing on these dataframes?
        #     Apply data cleaning and preprocessing techniques only if the dataframe exhibits the following issues:
        #     1. Duplicate Entries
        #         •	Duplicate rows in their entirety.
        #         •	Duplicate rows based on a specific subset of columns.
        #         •	Duplicate rows ignoring case sensitivity in string columns.
        #         •	Duplicate values due to trailing or leading whitespaces in text data.
        #         •	Duplicate rows with minor differences caused by inconsistent formatting (e.g., different cases or extra spaces).
        #         •	Near-duplicates identified by domain-specific logic (e.g., names with small spelling variations).
        #     2. Inconsistent Formatting
        #         •	Negative values where they do not make logical sense (e.g., age, income, counts, or categorical values that should not include negative signs). In this case, fix the value to be appropriate by removing the negative sign.
        #         •	Text inconsistency in categorical fields (e.g., “Male” vs. “male”).
        #         •	Numerical columns stored as strings (e.g., “100.5” as text instead of float).
        #         •	Date columns with mixed formats (e.g., “MM/DD/YYYY” and “YYYY-MM-DD”).
        #         •	Irregular capitalization in text columns (e.g., “New York” vs. “new york”).
        #         •	Unnecessary special characters or trailing/leading whitespaces in text fields.
        #     3. Inconsistent Data Types
        #         •	Float values in integer columns.
        #         •	Strings in numeric columns (e.g., “100.5” stored as a string).
        #         •	Mixed types in categorical fields (e.g., numbers and strings in the same column).
        #         •	Date columns stored as strings instead of proper datetime objects.
        #         •	Boolean fields represented inconsistently (e.g., “True”, “false”, 1, 0).
        #         •	Columns with mixed types due to data entry errors.
        #     If a specific header/attribute/column is important to the context of the dataframe, do not make updates to the values of that header/attribute/column. For example: if the racial background, test score, credit score, bonuses, etc., of an employee is unknown, do not set a value in place of it.
        #     Keep prompting until the output is executable and there is no error in the Python code provided.
        #     Generate a Python script that applies these cleaning and preprocessing techniques to the dataframes, prints out the head of each dataframe with 10 rows after cleaning, and ensures dependencies between columns are maintained. Only respond with the code because I will directly run your response. Do not include markdown formatting like ```py. Do not include anything else.”
        #     '''
        
        # for entry in dataframes:
        #     name, df = entry['name'], entry['dataframe']
        #     prompt += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"
            
        # while True:
        #     # Send prompt to the LLM and get a response
        #     response = ai.ask_llm(prompt)
        #     if response:
        #         # Print the response in red (error highlighting)
        #         print("\033[91m" + response + "\033[0m")
        #         # Attempt to execute the generated code
        #         try:
        #             exec(response)
        #             print("Code executed successfully!")
        #             break  # Exit loop if the code is executed without errors
        #         except Exception as e:
        #             print(f"Error executing generated code: {e}")
        #             # If error occurs, ask the LLM to adjust the code and retry
        #             prompt += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\n"
        #     else:
        #         print("No response from LLM. Retrying...")
