import pandas as pd
from io import StringIO
from aws.s3 import get_s3

def fetch_file(bucket_name, file_key):
    """
    Fetches a single file from S3 and returns its content as a DataFrame.
    """
    s3 = get_s3()
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        if file_key.endswith('.csv'):
            print('Reading csv:', file_key)
            return pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
        elif file_key.endswith('.xlsx'):
            return pd.read_excel(obj['Body'])
        else:
            raise ValueError(f"Unsupported file format: {file_key}")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch file {file_key} from S3: {str(e)}")

def fetch_files(bucket_name, file_keys):
    """
    Fetches multiple files from S3 and returns a list of DataFrames with metadata.
    """
    dataframes = []
    for file_key in file_keys:
        try:
            df = fetch_file(bucket_name, file_key)
            dataframes.append({"name": file_key, "dataframe": df})
        except Exception as e:
            print(f"Error fetching file {file_key}: {str(e)}")
    return dataframes
