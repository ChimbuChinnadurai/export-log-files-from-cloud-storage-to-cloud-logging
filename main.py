import base64
import json
import logging
from google.cloud import logging as cloud_logging
from google.cloud import storage

# Initialize the Cloud Logging client
client = cloud_logging.Client()

def process_log(event, context):
    # Get the log file information from the event payload
    # print(event)
    bucket_name = event['attributes']['bucketId']
    file_name = event['attributes']['objectId']
    logging.info(f"Processing log file: {file_name}")

    # Create a Cloud Storage client
    storage_client = storage.Client()

    # Get the log file from the bucket
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    log_contents = blob.download_as_text()

    # Send the log contents to Cloud Logging
    logger = client.logger('my-test-log') #log filename in cloud logging

    for line in log_contents.splitlines():
        # Parse the log line assuming it's in JSON format
        try:
            log_data = json.loads(line)
            logger.log_struct(log_data)
        except json.JSONDecodeError:
            logging.warning(f"Failed to parse log line: {line}")

    logging.info(f"Log file processed: {file_name}")
