from llm.gait import gAit

def transform(dataframes):
    ai = gAit()

    tempDataframes = dataframes.copy()

    for entry in dataframes:
        df = entry["dataframe"]  # Extract the DataFrame
        # Drop unnamed columns (where column names are None, '', or contain 'Unnamed')
        entry["dataframe"] = df.drop(columns=[col for col in df.columns if col is None or col == '' or 'Unnamed' in str(col)])
        print(f"DataFrame {entry['name']}:\n{entry['dataframe'].head(10)}\n")

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
    Only respond with the code because I will directly run your response. Do not include markdown formatting like ```python.
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_AddingColForBusinessValue += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    response = ai.ask_llm(llm_prompt_data_transformation_AddingColForBusinessValue)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after"
    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        if entry['name'] == "portfolio":
            entry['dataframe'] = portfolio
        elif entry['name'] == "profile":
            entry['dataframe'] = profile
        elif entry['name'] == "transcript":
            entry['dataframe'] = transcript
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
                exec(response, globals(), locals())
                print("Code executed successfully!")
                tempDataframes = dataframes.copy()
                
                break  # Exit loop if the code is executed without errors
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Add Column Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    dataframes = tempDataframes.copy()
                    break
        else:
            print("No response from LLM. Retrying...")


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

    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).
    Only respond with the code because I will directly run your response. Do not include markdown formatting like ```python.
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_NormalizingAndScaling += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    response = ai.ask_llm(llm_prompt_data_transformation_NormalizingAndScaling)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after"
    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        if entry['name'] == "portfolio":
            entry['dataframe'] = portfolio
        elif entry['name'] == "profile":
            entry['dataframe'] = profile
        elif entry['name'] == "transcript":
            entry['dataframe'] = transcript
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
            print("\033[93m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                response += update_dataframes_code
                exec(response, globals(), locals())
                print("Code executed successfully!")
                tempDataframes = dataframes.copy()
                
                break  # Exit loop if the code is executed without errors
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Normalize & Scale Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    dataframes = tempDataframes.copy()
                    break
        else:
            print("No response from LLM. Retrying...")


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
    These specific tasks can possibly result in new columns being created.

    The goal of this script is to provide better comprehension for a business analyst when viewing the code. If there NO REASON TO CHANGE, then do NOT change the dataframe. Keep the dataframe as it is.

    Generate a Python script that applies these transformations to the dataframes in the same order every time, prints out the head of each dataframe with 10 rows after transformations, 
    and ensures dependencies between columns are maintained. 
    At the end of the code, make sure to update the original dataframe variable with the new dataframe information.

    ''Keep the overall structural integrity of the original dataframe (for example: keep the same column headings & values).'' (bold text).
    Only respond with the code because I will directly run your response. Do not include markdown formatting like ```python.
    """
    for entry in dataframes:
        name, df = entry['name'], entry['dataframe']
        llm_prompt_data_transformation_NormalizingAndScaling += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"

    response = ai.ask_llm(llm_prompt_data_transformation_NormalizingAndScaling)

    llm_prompt_data_transformation_clean_script = f"Given the script:\n{response}\n Clean and modify the code to ensure that the markdown formatting is removed, and there are no errors with the execution of the script. Provide me with ONLY (bold text) the code and nothing else. This response will directly be ran. Print the head of each dataframe after"
    update_dataframes_code = """
    # Update the dataframes list with modified DataFrames
    for entry in dataframes:
        if entry['name'] == "portfolio":
            entry['dataframe'] = portfolio
        elif entry['name'] == "profile":
            entry['dataframe'] = profile
        elif entry['name'] == "transcript":
            entry['dataframe'] = transcript
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
            print("\033[95m" + response + "\033[0m")
            
            # Attempt to execute the generated code
            try:
                response += update_dataframes_code
                exec(response, globals(), locals())
                print("Code executed successfully!")
                tempDataframes = dataframes.copy()
                
                break  # Exit loop if the code is executed without errors
            except Exception as e:
                print(f"Error executing generated code: {e}")
                attempt += 1
                # If error occurs, ask the LLM to adjust the code and retry
                if attempt < 3:
                    print("Aggregation Prompt Attempt: ", attempt)
                    llm_prompt_data_transformation_clean_script += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\nThe current code is {response}, so make sure to apply modifications to fix the code."
                else:
                    print("Max number of attempts reached. Continue to next prompt")
                    dataframes = tempDataframes.copy()
                    break
        else:
            print("No response from LLM. Retrying...")


    for i, entry in enumerate(dataframes):
        df = entry["dataframe"]  # Extract the DataFrame
        name = entry.get("name", f"dataframe_{i+1}")  # Get the name or default to 'dataframe_1', 'dataframe_2', etc.
        filename = f"{name}_transformed.csv"  # Append '_transformed' to the dataframe name
        df.to_csv(filename, index=False)  # Save the dataframe to a CSV file without the index
        print(f"DataFrame {filename} has been saved.")

    return dataframes
