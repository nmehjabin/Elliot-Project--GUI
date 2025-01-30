
from sosmart.model_testing_ui.values import OUTPUT_FOLDER, get_user, get_config
import json
import pandas as pd
import time
from io import StringIO

import boto3
 

#END CONVERSATION DATA FORMAT
'''
ENDCONVERSATION -- ROLE_CATEGORY: character, OVERALL: 10, HUMOR: 10, USEFULNESS: 10, CREATIVITY: 10, CHARACTER: 10, NOTES: Here are some notes about this role
'''

# Initialize the S3 client
# s3_client = boto3.client('s3')

S3_BUCKET_NAME = "sosmart-model-testing-ui"
conversation_data_folder = f"{OUTPUT_FOLDER}/conversation_data"


def lowest_missing_positive(nums):
    nums_set = set(nums)  # Convert the list to a set for O(1) lookups
    i = 1  # Start checking from 1 (smallest positive integer)
    while i in nums_set:
        i += 1
    return i

def get_id_number():
    # s3_keys = s3_client.list_objects_v2(
    #     Bucket=S3_BUCKET_NAME,
    #     Prefix=f"{conversation_data_folder}/{get_user()}"
    # )

    # if 'Contents' not in s3_keys:
    #     return 1
    # file_keys = [item['Key'].split('/')[-2] for item in s3_keys['Contents']]
    # folders = filter(lambda x: x.split('-')[0].isdigit(), file_keys)
    # ids = map(lambda x: int(x.split('-')[0]), folders)
    # id = lowest_missing_positive(ids)
    return 1



def read_csv_from_s3(object_key):
    pass
    # try:
    #     response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_key)
    #     csv_content = response['Body'].read().decode('utf-8')
    #     df = pd.read_csv(StringIO(csv_content))
    #     return df
    # except s3_client.exceptions.NoSuchKey:
    #     print(f"No file found at s3://{S3_BUCKET_NAME}/{object_key}. Returning empty DataFrame.")
    #     return pd.DataFrame()
    # except pd.errors.EmptyDataError:
    #     print(f"pd.errors.EmptyDataError:")
    #     return pd.DataFrame()
    # except Exception as e:
    #     print(f"Error reading CSV from S3 using boto3: {e}")
    #     raise

def write_data(id, messages, formatted_messages):
    pass
    # save_to_s3(id, formatted_messages, "context.txt")
    # save_to_s3(id, json.dumps(messages, indent=4), "messages.json")

def save_to_s3(id, data, filename, key=None):
    pass
    # try:
    #     if key == None:
    #         key = f"{conversation_data_folder}/{get_user()}/{id}/{filename}"
    #     s3_client.put_object(
    #         Bucket=S3_BUCKET_NAME,
    #         Key=key,
    #         Body=data
    #     )
    #     print(f"Data saved to S3 bucket '{S3_BUCKET_NAME}' with key '{key}'.")
    # except Exception as e:
    #     print(f"Error saving to S3: {e}")
    #     raise



def append_line_to_s3_csv_file(object_key, new_line, headers):
    pass

    # try:
    #     try:
    #         response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_key)
    #         file_content = response['Body'].read().decode('utf-8')
    #     except s3_client.exceptions.NoSuchKey:
    #         print(f"append_line_to_s3_csv_file {object_key} File does not exist. Creating a new one.")
    #         file_content = headers

    #     file_content += "\n" + new_line
    #     s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=object_key, Body=file_content)

    # except Exception as e:
    #     print(f"Error appending line to S3 file: {e}")
    #     raise






#end conversation csv stuff
def parse_endconversation_string(input_str):

    result = {}
    
    pairs = input_str.split('--')[1].split(',')
    
    for pair in pairs:
        if ':' not in pair:
            continue
        key, value = pair.split(':', 1)
        key = key.strip().lower()
        value = value.strip()
        result[key] = value
    
    return result


ROLES_CSV_HEADER = "overall_rating,user,role,notes,conversation_id"

def write_conversation_end_data(
    id_number,
    conversation_id,
    end_conversation_string, 
    user_input_role,
    number_of_messages,
    ending_context_length, 
    user_role_length,
    system_role_length,
    user_message_lengths,
    assistant_message_lengths,
):
    # save_to_s3(conversation_id, end_conversation_string, "end_conversation_string.txt")

    parsed_endstring = parse_endconversation_string(end_conversation_string)

    # user_csv_output_file = f"{conversation_data_folder}/{get_user()}/model_interactions.csv"
    # df_user = read_csv_from_s3(user_csv_output_file)

    # combined_csv_output_file = f"{conversation_data_folder}/combined_model_interactions.csv"
    # df_combined = read_csv_from_s3(combined_csv_output_file)

    role_category = ""
    if "role_category" in parsed_endstring:
        role_category = parsed_endstring['role_category'].lower()
    overall = -1
    if "overall" in parsed_endstring:
        overall = parsed_endstring['overall']
        # save_to_s3(conversation_id, user_input_role, f"{overall}-user-input-role.txt")
    notes = ""
    if "notes" in parsed_endstring:
        notes = parsed_endstring['notes']
    del parsed_endstring['role_category']
    del parsed_endstring['overall']
    del parsed_endstring['notes']

    #headers-data come gonna come from the user input in the gui
    #id,user,config,role_category,role,timestamp,ending_context_length,user_role_length,system_role_length,average_user_message_length,average_assistant_message_length,overall,     
    csv_row = {
        'id': id_number,
        'user': get_user(),
        'config': get_config()["name"],
        'role_category': role_category,
        'role': user_input_role,
        'timestamp': time.time(),
        'number_of_messages': number_of_messages,
        'ending_context_length': ending_context_length,
        'user_role_length': user_role_length,
        'system_role_length': system_role_length,
        'user_message_lengths': str(user_message_lengths),
        'assistant_message_lengths': str(assistant_message_lengths),
        'notes': notes,
        'overall': overall,
    }

    print("CSV ROW\n\n")
    print(csv_row)
    print("\n\n")

    # df_user = update_dataframe(df_user, csv_row, parsed_endstring)
    # write_dataframe_to_s3(df_user, user_csv_output_file)

    # df_combined = update_dataframe(df_combined, csv_row, parsed_endstring)
    # write_dataframe_to_s3(df_combined, combined_csv_output_file)

    # user_roles_csv_output_file = f"{conversation_data_folder}/{get_user()}/roles.csv"
    # combined_roles_csv_output_file = f"{conversation_data_folder}/roles.csv"
    # role_csv_row = f"{overall},{get_user()},{user_input_role},{notes},{conversation_id},"
    # append_line_to_s3_csv_file(user_roles_csv_output_file, role_csv_row, ROLES_CSV_HEADER)
    # append_line_to_s3_csv_file(combined_roles_csv_output_file, role_csv_row, ROLES_CSV_HEADER)



def update_dataframe(df, csv_row, parsed_endstring):

    combined_dict = { **csv_row, **parsed_endstring }

    for col in df.columns:
        if col not in combined_dict.keys():
            combined_dict[col] = ''

    new_columns = set(combined_dict.keys()) - set(df.columns)
    for col in new_columns:
        df[col] = ''

    new_row = pd.DataFrame([combined_dict])
    return pd.concat([df, new_row], ignore_index=True)


def write_dataframe_to_s3(df, s3_key):
    pass

    # csv_buffer = StringIO()
    # df.to_csv(csv_buffer, index=False)
    # save_to_s3(None, csv_buffer.getvalue(), None, key=s3_key)



