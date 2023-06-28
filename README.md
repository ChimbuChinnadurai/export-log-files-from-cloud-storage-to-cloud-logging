# export-log-files-from-cloud-storage-to-cloud-logging

The repository contains a Python cloud function example to export log files in cloud storage to cloud logging

## Enable cloud storage notification

Run the below command  to enable cloud storage pubsub event notification based on object changes: https://cloud.google.com/storage/docs/pubsub-notifications

```
gcloud storage buckets notifications create gs://<BUCKET-NAME> --topic=<TOPIC-NAME> --event-types=OBJECT_FINALIZE --project=<PROJECT-ID>
```

## Deploy cloud function

Run the below command from the root directory of this repo to deploy the cloud function. This will use the default compute engine service account but i recommend you to create a new service account with custom roles to limit the permissions.

```
gcloud functions deploy <FUNCTION-NAME> \
--trigger-event=providers/cloud.pubsub/eventTypes/topic.publish \
--trigger-resource=<TOPIC-NAME> \
--max-instances=10 \
--runtime=python311 \
--entry-point=process_log \
--source=.
```

## Test the changes

Upload a sample json log file to the cloud storage bucket and monitor the log injection in cloud logging.