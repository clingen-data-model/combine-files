#!/usr/bin/env bash

set -xeo pipefail

if [ -z "$instance_name" ]; then
    instance_name="combine-files"
else
    echo "instance_name set in environment"
fi

echo "Instance name: $instance_name"

set -u

region="us-east1"
image=us-east1-docker.pkg.dev/clingen-stage/cloud-run-source-deploy/combine-files:latest
pipeline_service_account=combine-files@clingen-stage.iam.gserviceaccount.com
deployment_service_account=clinvar-ingest-deployment@clingen-dev.iam.gserviceaccount.com

################################################################
# Build the image

docker build \
    --platform linux/amd64 \
    -t $image .

docker push $image

################################################################
# Deploy job
# if gcloud run jobs list --region $region | awk '{print $2}' | grep "^$instance_name$"  ; then
#     echo "Cloud Run Job $instance_name already exists - updating it"
#     command="update"
# else
#     echo "Cloud Run Job $instance_name doesn't exist - creating it"
#     command="create"
# fi
if gcloud run jobs list --region $region | awk '{print $2}' | grep "^$instance_name$"  ; then
    echo "Cloud Run Job $instance_name already exists deleting it first"
    gcloud run jobs delete $instance_name --region $region
fi

gcloud run jobs create $instance_name \
    --cpu=2 \
    --memory=8Gi \
    --task-timeout=10h \
    --image=$image \
    --region=$region \
    --service-account=$pipeline_service_account
