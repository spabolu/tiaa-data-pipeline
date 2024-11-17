from llm.gait import gAit

def cleaning(dataframes):
    genai = gAit()
    
    for entry in dataframes:
        print(f"DataFrame {entry['name']}:\n{entry['dataframe'].head(10)}\n")
        
        prompt = '''
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
        
        for entry in dataframes:
            name, df = entry['name'], entry['dataframe']
            prompt += f"\nDataframe Name: {name}\nHead:\n{df.head(10).to_string(index=False)}\n"
        
        while True:
            # Send prompt to the LLM and get a response
            response = genai.ask_llm(prompt)
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
                    prompt += f"\nError encountered: {str(e)}\nPlease adjust the code and try again.\n"
            else:
                print("No response from LLM. Retrying...")