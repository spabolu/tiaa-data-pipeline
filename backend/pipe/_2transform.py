from llm.gait import gAit
import pandas as pd
from datetime import datetime
import numpy as np
import io
import re
import sys
import pandas as pd
from datetime import datetime
import io
import sys
import sklearn
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer

import sweetviz as sv

def extract_code_from_md(markdown_text):
    pattern = r'```(?:python)?\n(.*?)```'
    code_blocks = re.findall(pattern, markdown_text, re.DOTALL)
    
    result = '\n'.join(block.replace('print("\n', 'print("\\n') for block in code_blocks)
    
    return result
    
def transform(dataframes):
    ai = gAit()

    tempDataframes = dataframes.copy()
    report_AI_txt = ""
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
        name, df = entry['name'], entry['dataframe'] #Customer_transcation/porfolio.csv
        llm_prompt_data_quality_check += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    # response = genai.generate_response(llm_prompt_data_quality_check)    
    # exec(response)
    # qualityCheckBeforeText += response
    # print(qualityCheckBeforeText+"\n\n")
    
    # response = ai.ask_llm(llm_prompt_data_quality_check)

    # # Clean up the generated script to remove unsupported arguments
    # response = response.replace("datetime_is_numeric=True", " ") if response is not None else ""    

    # # Capture the output of the generated code
    # output_capture = io.StringIO()
    # sys.stdout = output_capture  # Redirect stdout

    # Execute the cleaned-up generated code
    # exec(response)

    attempt = 0
    while True:
        # Send prompt to the LLM and get a response
            response = ai.ask_llm(llm_prompt_data_quality_check)

            # Clean up the generated script to remove unsupported arguments
            response = response.replace("datetime_is_numeric=True", " ") if response is not None else ""    

            # Capture the output of the generated code
            output_capture = io.StringIO()
            sys.stdout = output_capture  # Redirect stdout        if response:
            # Remove markdown formatting if present

            if response.startswith("```python") and response.endswith("```"):
                response = response[9:-3].strip()  # Strip the opening and closing markdown syntax
            # Print the response in green for success
            print("\033[92m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                exec(extract_code_from_md(response), globals(), locals())

            # Loop through each dataframe to compare rows and columns
                print("Quality Check Successfull")
                break
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Add Column Prompt Attempt: ", attempt)
                    llm_prompt_data_quality_check += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    break
                    # llm_prompt_data_transformation_test = llm_prompt_data_transformation
    
    # Reset stdout to normal
    sys.stdout = sys.__stdout__

    # Append captured output to the qualityCheckBeforeText
    qualityCheckBeforeText += output_capture.getvalue()

    print("QUALITY CHECK\n\n", qualityCheckBeforeText)

    # Print the final quality check text
    llm_prompt_data_transformation_AddingColForBusinessValue = """
    I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one.
    Don’t drop any unnamed columns. Assume I already imported the dataframes and their variables to directly use. Do not preprocess the data as it is already preprocessed.

    Generate a Python script and do NOT include markdown formatting, ```python, in the python script. This script is meant to be `Adding New Columns for Business Value` (bold text). 
    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).

    For example, the script can function with any of these tasks:

        •	Add a column that calculates the duration of employment from a hiredate attribute.
        •	Create a column to categorize numerical values into bins (e.g., categorize ages into “Young”, “Middle-aged”, “Senior”).
        •	Generate a column calculating percentage growth if relevant columns are present (e.g., revenue growth, salary increment).
        •	Compute and add moving averages or rolling statistics (e.g., for sales data).
        •	Add a flag column (e.g., if a value exceeds a threshold, or to show an outlier).
        •	Create a column for cumulative sums or counts where logical.
        
    The goal of this script is to provide better comprehension for a business analyst when viewing the code. If there NO REASON TO CHANGE, then do NOT change the dataframe. Keep the dataframe as it is.

    Generate a Python script that applies these transformations to the dataframes in the same order every time, prints out the head of each dataframe with 10 rows after transformations, 
    and ensures dependencies between columns are maintained. 
    At the end of the code, make sure to update the original dataframe variable with the new dataframe information.
    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).
    Give me ONLY Python code and nothing else. I will be running this code directly. Remove Markdown text from the beginning and end of the script. 
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_AddingColForBusinessValue += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"
    response = ai.ask_llm(llm_prompt_data_transformation_AddingColForBusinessValue)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after"
    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        # Dynamically access the variable with the same name as the dataframe
        df_name = entry['name']  # Get the name of the DataFrame
        if df_name in globals():  # Check if the variable exists in the global namespace
            entry['dataframe'] = globals()[df_name]  # Update the DataFrame dynamically
    """


    attempt = 0
    while True:
        # Send prompt to the LLM and get a response
        response = ai.ask_llm(llm_prompt_data_transformation_clean_script)
        if response:
            # Remove markdown formatting if present
            if response.startswith("```python") and response.endswith("```"):
                response = response[9:-3].strip()  # Strip the opening and closing markdown syntax
            # Print the response in green for success
            print("\033[92m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                response += update_dataframes_code
                exec(extract_code_from_md(response), globals(), locals())

            # Loop through each dataframe to compare rows and columns
                for df1, df2 in zip(dataframes, tempDataframes):
                    if df1["dataframe"].shape[0] == df2["dataframe"].shape[0] and df1["dataframe"].shape[1] >= df2["dataframe"].shape[1]:
                        print(f"Row count is good for {df1['name']}'.")
                        tempDataframes = dataframes.copy()
                        print("Code executed successfully!")
                        break
                    else:
                        dataframes = tempDataframes.copy()
                        print("Problem with a row or column\n")
                        # print("updated dataframe's row + col count ", dataframes["dataframe"].shape[0], " ", dataframes["dataframe"].shape[1])
                        # print("tempDataFrame's row + col count ", tempDataframes["dataframe"].shape[0], " ", dataframes["dataframe"].shape[1])
                        break
                break
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Add Column Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    feedbackAIPrompt = f'Given the script:\n {llm_prompt_data_transformation_clean_script}\n, what transform should a business analyst perform on with the data provided, and which data frame should be modified? Keep your response to only 2 sentences. Provide a title about which transform this is about. Do not mention the script, only write specific information about what the business analyst should do.'
                    feedbackAI = ai.ask_llm(feedbackAIPrompt)
                    if feedbackAI is not None:
                            report_AI_txt += feedbackAI + "\n\n"
                    else:
                            report_AI_txt += "No feedback provided by AI.\n\n"
                    print("This is the Report:\n", report_AI_txt)
                    dataframes = tempDataframes.copy()
                    break
                    # llm_prompt_data_transformation_test = llm_prompt_data_transformation
        else:
            print("No response from LLM. Retrying...")

    print("Business Column Info")
    for entry in tempDataframes:
        name, df = entry['name'], entry['dataframe']
        print(f"\n\033[38;5;37m Dataframe: {name}\nHead:\n{df.head(10).to_string(index=False)}\n\033[0m")
        
    # 2. Normalization and Scalingfin

    # 	•	Normalize numerical columns to a [0, 1] scale (e.g., min-max normalization).
    # 	•	Standardize numerical data using z-scores to center around zero.
    # 	•	Log transformation for skewed numerical data to reduce skewness.
    # 	•	Apply scaling to maintain consistency across numerical attributes (e.g., scaling prices or scores).
    # 	•	Scale specific columns proportionally to their maximum value.


    llm_prompt_data_transformation_NormalizingAndScaling = """
    I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one.
    Don’t drop any unnamed columns. Assume I already imported the dataframes and their variables to directly use. Do not preprocess the data as it is already preprocessed.

    Generate a Python script and do NOT include markdown formatting, ```python, in the python script. This script is meant to be `Normalization and Scaling` (bold text). 
    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).

    For example, the script can function with any of these tasks:

        •	Normalize numerical columns to a [0, 1] scale (e.g., min-max normalization).
        •	Standardize numerical data using z-scores to center around zero.
        •	Log transformation for skewed numerical data to reduce skewness.
        •	Apply scaling to maintain consistency across numerical attributes (e.g., scaling prices or scores).
        •	Scale specific columns proportionally to their maximum value.
    These specific tasks can possibly result in new columns being created.

    The goal of this script is to provide better comprehension for a business analyst when viewing the code. If there NO REASON TO CHANGE, then do NOT change the dataframe. Keep the dataframe as it is.

    Generate a Python script that applies these transformations to the dataframes in the same order every time, prints out the head of each dataframe with 10 rows after transformations, 
    and ensures dependencies between columns are maintained. 
    At the end of the code, make sure to update the original dataframe variable with the new dataframe information.

    Give me ONLY Python code and nothing else. I will be running this code directly. Remove Markdown text from the beginning and end of the script. 
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_NormalizingAndScaling += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    response = ai.ask_llm(llm_prompt_data_transformation_NormalizingAndScaling)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after. Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values)."

    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        # Dynamically access the variable with the same name as the dataframe
        df_name = entry['name']  # Get the name of the DataFrame
        if df_name in globals():  # Check if the variable exists in the global namespace
            entry['dataframe'] = globals()[df_name]  # Update the DataFrame dynamically
    """


    attempt = 0
    while True:
        # Send prompt to the LLM and get a response
        response = ai.ask_llm(llm_prompt_data_transformation_clean_script)
        if response:
            # Remove markdown formatting if present
            if response.startswith("```python") and response.endswith("```"):
                response = response[9:-3].strip()  # Strip the opening and closing markdown syntax
            # Print the response in green for success
            print("\033[92m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                response += update_dataframes_code
                exec(extract_code_from_md(response), globals(), locals())

            # Loop through each dataframe to compare rows and columns
                for df1, df2 in zip(dataframes, tempDataframes):
                    if df1["dataframe"].shape[0] == df2["dataframe"].shape[0] and df1["dataframe"].shape[1] >= df2["dataframe"].shape[1]:
                        print(f"Row & Col count is good for {df1['name']}'.")
                        tempDataframes = dataframes.copy()
                        print("Code executed successfully!")
                        break

                    else:
                        dataframes = tempDataframes.copy()
                        print("Problem with a row or column\n")
                        # print("updated dataframe's row + col count ", dataframes["dataframe"].shape[0], " ", dataframes["dataframe"].shape[1])
                        # print("tempDataFrame's row + col count ", tempDataframes["dataframe"].shape[0], " ", dataframes["dataframe"].shape[1])
                        break
                break
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Add Column Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    feedbackAIPrompt = f'Given the script:\n {llm_prompt_data_transformation_clean_script}\n, what transform should a business analyst perform on with the data provided, and which data frame should be modified? Keep your response to only 2 sentences. Provide a title about which transform this is about. Do not mention the script, only write specific information about what the business analyst should do.'
                    feedbackAI = ai.ask_llm(feedbackAIPrompt)
                    if feedbackAI is not None:
                            report_AI_txt += feedbackAI + "\n\n"
                    else:
                            report_AI_txt += "No feedback provided by AI.\n\n"
                    print("This is the Report:\n", report_AI_txt)
                    dataframes = tempDataframes.copy()
                    break
                    # llm_prompt_data_transformation_test = llm_prompt_data_transformation
        else:
            print("No response from LLM. Retrying...")
            
    print("Normalization Info")
    for entry in tempDataframes:
        name, df = entry['name'], entry['dataframe']
        print(f"\n\033[38;5;37m Dataframe: {name}\nHead:\n{df.head(10).to_string(index=False)}\n\033[0m")

    # 3. Aggregation

    # 	•	Aggregate data based on groupings (e.g., sum of sales by region or average scores by class).
    # 	•	Add aggregated columns for totals, averages, or counts (e.g., total revenue by category).
    # 	•	Derive weighted averages if applicable (e.g., weighted scores).


    llm_prompt_data_transformation_NormalizingAndScaling = """
    I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one.
    Don’t drop any unnamed columns. Assume I already imported the dataframes and their variables to directly use. Do not preprocess the data as it is already preprocessed.

    Generate a Python script and do NOT include markdown formatting, ```python, in the python script. This script is meant to for `Aggregation` (bold text). 
    ''Keep the overall structural integrity of the original dataframe (for example maintain the column headings & values).'' (bold text).

    For example, the script can function with any of these tasks:

        •	Aggregate data based on groupings (e.g., sum of sales by region or average scores by class).
        •	Add aggregated columns for totals, averages, or counts (e.g., total revenue by category).
        •	Derive weighted averages if applicable (e.g., weighted scores).
        
    If aggregate functions are being used, create NEW columns which represent this. 'Do NOT modify existing columns' (bold text).

    The goal of this script is to provide better comprehension for a business analyst when viewing the code. If there NO REASON TO CHANGE, then do NOT change the dataframe. Keep the dataframe as it is.

    Generate a Python script that applies these transformations to the dataframes in the same order every time, prints out the head of each dataframe with 10 rows after transformations, 
    and ensures dependencies between columns are maintained. 
    At the end of the code, make sure to update the original dataframe variable with the new dataframe information.

    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).
    Give me ONLY Python code and nothing else. I will be running this code directly. Remove Markdown text from the beginning and end of the script. 
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_NormalizingAndScaling += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    response = ai.ask_llm(llm_prompt_data_transformation_NormalizingAndScaling)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after"
    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        # Dynamically access the variable with the same name as the dataframe
        df_name = entry['name']  # Get the name of the DataFrame
        if df_name in globals():  # Check if the variable exists in the global namespace
            entry['dataframe'] = globals()[df_name]  # Update the DataFrame dynamically
    """

    attempt = 0
    while True:
        # Send prompt to the LLM and get a response
        response = ai.ask_llm(llm_prompt_data_transformation_clean_script)
        if response:
            # Remove markdown formatting if present
            if response.startswith("```python") and response.endswith("```"):
                response = response[9:-3].strip()  # Strip the opening and closing markdown syntax
            # Print the response in green for success
            print("\033[92m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                response += update_dataframes_code
                exec(extract_code_from_md(response), globals(), locals())

            # Loop through each dataframe to compare rows and columns
                for df1, df2 in zip(dataframes, tempDataframes):
                    if df1["dataframe"].shape[0] == df2["dataframe"].shape[0] and df1["dataframe"].shape[1] >= df2["dataframe"].shape[1]:
                        print(f"Row count is good for {df1['name']}'.")
                        tempDataframes = dataframes.copy()
                        print("Code executed successfully!")
                        break
                    else:
                        dataframes = tempDataframes.copy()
                        print("Problem with a row or column\n")
                        break
                break
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                if attempt < 3:
                    print("Add Column Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    feedbackAIPrompt = f'Given the script:\n {llm_prompt_data_transformation_clean_script}\n, what transform should a business analyst perform on with the data provided, and which data frame should be modified? Keep your response to only 2 sentences. Provide a title about which transform this is about. Do not mention the script, only write specific information about what the business analyst should do.'
                    feedbackAI = ai.ask_llm(feedbackAIPrompt)
                    if feedbackAI is not None:
                            report_AI_txt += feedbackAI + "\n\n"
                    else:
                            report_AI_txt += "No feedback provided by AI.\n\n"
                    print("This is the Report:\n", report_AI_txt)
                    dataframes = tempDataframes.copy()
                    break
        else:
            print("No response from LLM. Retrying...")
            
            
    print("Aggregation Info")
    for entry in tempDataframes:
        name, df = entry['name'], entry['dataframe']
    print(f"\n\033[38;5;37m Dataframe: {name}\nHead:\n{df.head(10).to_string(index=False)}\n\033[0m")

        # 4. Enhancing Column Names

    # 	•	Rename ambiguous column names (e.g., “price” to “Price (USD)”, “date” to “Transaction Date”).
    # 	•	Add contextual information to column names to clarify their purpose (e.g., “score” to “Test Score”).
    # 	•	Standardize column names to follow a consistent format (e.g., snake_case or Title Case).

    llm_prompt_data_transformation_EnhanceColumnName = """
    I am going to loop through an array of data frames. I will provide the dataframe name and the head of each one.
    Don’t drop any unnamed columns. Assume I already imported the dataframes and their variables to directly use. Do not preprocess the data as it is already preprocessed.

    Generate a Python script and do NOT include markdown formatting, ```python, in the python script. This script is meant to for `Enhancing Column Names` (bold text). 
    ''Keep the overall structural integrity of the original dataframe (for example maintain the column headings & values).'' (bold text).

    For example, the script can function with any of these tasks:

        •	Rename ambiguous column names (e.g., “price” to “Price (USD)”, “date” to “Transaction Date”).
        •	Add contextual information to column names to clarify their purpose (e.g., “score” to “Test Score”).
        •	Standardize column names to follow a consistent format (e.g., snake_case or Title Case).
        
    If aggregate functions are being used, create NEW columns which represent this. 'Do NOT modify existing columns' (bold text).

    The goal of this script is to provide better comprehension for a business analyst when viewing the code. If there NO REASON TO CHANGE, then do NOT change the dataframe. Keep the dataframe as it is.

    Generate a Python script that applies these transformations to the dataframes in the same order every time, prints out the head of each dataframe with 10 rows after transformations, 
    and ensures dependencies between columns are maintained. 
    At the end of the code, make sure to update the original dataframe variable with the new dataframe information.

    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).
    Give me ONLY Python code and nothing else. I will be running this code directly. Remove Markdown text from the beginning and end of the script. 
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_EnhanceColumnName += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    response = ai.ask_llm(llm_prompt_data_transformation_EnhanceColumnName)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after"
    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        # Dynamically access the variable with the same name as the dataframe
        df_name = entry['name']  # Get the name of the DataFrame
        if df_name in globals():  # Check if the variable exists in the global namespace
            entry['dataframe'] = globals()[df_name]  # Update the DataFrame dynamically
    """

    attempt = 0
    while True:
        # Send prompt to the LLM and get a response
        response = ai.ask_llm(llm_prompt_data_transformation_clean_script)
        if response:
            # Remove markdown formatting if present
            if response.startswith("```python") and response.endswith("```"):
                response = response[9:-3].strip()  # Strip the opening and closing markdown syntax
            # Print the response in green for success
            print("\033[92m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                response += update_dataframes_code
                exec(extract_code_from_md(response), globals(), locals())

            # Loop through each dataframe to compare rows and columns
                for df1, df2 in zip(dataframes, tempDataframes):
                    if df1["dataframe"].shape[0] == df2["dataframe"].shape[0] and df1["dataframe"].shape[1] >= df2["dataframe"].shape[1]:
                        print(f"Row count is good for {df1['name']}'.")
                        tempDataframes = dataframes.copy()
                        print("Code executed successfully!")
                        break
                    else:
                        dataframes = tempDataframes.copy()
                        print("Problem with a row or column\n")
                        # print("updated dataframe's row + col count ", dataframes["dataframe"].shape[0], " ", dataframes["dataframe"].shape[1])
                        # print("tempDataFrame's row + col count ", tempDataframes["dataframe"].shape[0], " ", dataframes["dataframe"].shape[1])
                        break
                break
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Add Column Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    feedbackAIPrompt = f'Given the script:\n {llm_prompt_data_transformation_clean_script}\n, what transform should a business analyst perform on with the data provided, and which data frame should be modified? Keep your response to only 2 sentences. Provide a title about which transform this is about. Do not mention the script, only write specific information about what the business analyst should do.'
                    feedbackAI = ai.ask_llm(feedbackAIPrompt)
                    if feedbackAI is not None:
                            report_AI_txt += feedbackAI + "\n\n"
                    else:
                            report_AI_txt += "No feedback provided by AI.\n\n"                    
                    print("This is the Report:\n", report_AI_txt)
                    dataframes = tempDataframes.copy()
                    break
                    # llm_prompt_data_transformation_test = llm_prompt_data_transformation
        else:
            print("No response from LLM. Retrying...")
            
            
    print("Enhance Column Name Info")
    for entry in tempDataframes:
        name, df = entry['name'], entry['dataframe']
        print(f"\n\033[38;5;37m Dataframe: {name}\nHead:\n{df.head(10).to_string(index=False)}\n\033[0m")
    
    # REPORT GENERATION
    # Define the filename for the PDF
    pdf_filename = "business_report.pdf"
    # Set up the PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    # Create a list to hold the elements for the PDF
    elements = []
    # Add the title
    title_style = styles['Title']
    title = Paragraph("Business Insights Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))  # Add some space below the title
    # Add the subtitle
    subtitle_style = styles['Heading2']
    subtitle = Paragraph("Generated Insights & Analysis", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.2 * inch))  # Add space below the subtitle

    # Define the LLM prompt that you want to ask the LLM
    llm_prompt_data_analysis = f"""
    I want to generate a business insight report.
    Can you respond with only the report and nothing else
    Do not include the markdown file format, do not try to bold anything.
    If you want to make a new bullet point, make a new line for it.
    1. Summarize each CSV file.
    Here are the dataframes:
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_analysis += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"
    llm_prompt_data_analysis += f"""
    2. Include information about quality checks completed on the raw data. Be straightforward and show the quality checks directly in the PDF output: {qualityCheckBeforeText}
    3. Analyze relationships between the datasets and suggest business insights based on their interaction.
    4. Provide any other relevant business recommendations based on the analysis.
    """
    # Request the LLM response
    while True:
        response = ai.ask_llm(llm_prompt_data_analysis)
        if response:
            # Print the response for debugging
            print("\033[92m" + response + "\033[0m")
            # Split the response into paragraphs and add to the PDF
            content_style = styles['BodyText']
            paragraphs = response.split("\n\n")  # Separate into paragraphs
            for paragraph in paragraphs:
                wrapped_paragraph = Paragraph(paragraph, content_style)
                elements.append(wrapped_paragraph)
                elements.append(Spacer(1, 0.2 * inch))  # Add space between paragraphs
            break  # Exit loop if the response is successfully handled
        else:
            print("No response from LLM. Retrying...")
    # Build the PDF with the collected elements


    subtitle_style = styles['Heading2']
    subtitle = Paragraph("Recommended Transformations", subtitle_style)
    elements.append(subtitle)
    paragraph2 = Paragraph(report_AI_txt, styles['Normal'])
    elements.append(paragraph2)
    elements.append(Spacer(1, 0.2 * inch))  # Add space below the subtitle

    doc.build(elements)
    # Confirmation message
    print(f"Business report has been generated and saved as '{pdf_filename}'.")


# Iterate over each dataframe entry
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        # Generate the Sweetviz report
        name = entry["name"].split('/')[1]
        name = name.split('.')[0]
            
        html_filename = f"{name}.html"  # Define the output HTML filename
        report = sv.analyze(df)  # Create the analysis report
        # Save the report as an HTML file
        report.show_html(filepath=html_filename, open_browser=False)  # Avoid automatically opening in browser
        print(f"Report saved as {html_filename}")

    return dataframes
