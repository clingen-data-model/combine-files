# combine-files
A utility to combine files into a single file in GCS.


Example to build on macosx and target git docker registry
```
docker build --platform linux/amd64 -t us-east1-docker.pkg.dev/clingen-stage/cloud-run-source-deploy/combine-files .
```

Example to push to docker registry
```
docker push us-east1-docker.pkg.dev/clingen-stage/cloud-run-source-deploy/combine-files
```

Example to call service against some example files in gcs.
```
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" 'https://combine-files-wawwp3ppza-ue.a.run.app?bucket_name=clinvar-gk-pilot&folder_path=2024-04-07/dev/scv_subset_v2/&file_pattern=scv.*\.csv\.gz&output_file_path=gs://clinvar-gk-pilot/2024-04-07/dev/combined-scv_subset_v2.json.gz/'
```

