#!/bin/bash

set -xeo pipefail

if [ -z "$instance_name" ]; then
    instance_name="combine-files"
else
    echo "instance_name set in environment"
fi

if [ "$JOB_WAIT" == "1" ]; then
    wait_opt="--wait"
else
    wait_opt="--async" # the default
fi

set -u

job_name=$instance_name
region="us-east1"

# Inputs
dir_basename="catvar_output_v2"
bucket_name="clinvar-gk-pilot"
folder_path="2024-04-07/dev/${dir_basename}"
file_pattern='.*.gzip'
output_file_path="combined-${dir_basename}.json.gz"
output_blob_path="2024-04-07/dev/combined-${dir_basename}.json.gz"

env_vars="bucket_name=$bucket_name"
env_vars="$env_vars,folder_path=$folder_path"
env_vars="$env_vars,file_pattern=$file_pattern"
env_vars="$env_vars,output_file_path=$output_file_path"
env_vars="$env_vars,output_blob_path=$output_blob_path"

gcloud run jobs execute $job_name \
    --region $region \
    $wait_opt \
    --update-env-vars=$env_vars
