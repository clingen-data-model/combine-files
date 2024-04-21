import os
import re
import gzip
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)


def combine_files(bucket_name, folder_path, file_pattern, output_file_path, output_blob_path=None):

    # Initialize Google Cloud Storage client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    if bucket is None:
        print(f"{bucket_name} bucket not found.")
        return

    # List all files in the folder matching the file pattern
    blobs = bucket.list_blobs(prefix=folder_path)

    if blobs is None:
        print(f"No blobs found in {folder_path}.")
        return

    files_to_combine = [blob.name for blob in blobs if re.match(
        file_pattern, os.path.basename(blob.name))]

    if len(files_to_combine) == 0:
        print(f"No files found matching pattern {file_pattern} to combine.")
        return

    with gzip.open(output_file_path, 'wt') as f_out:
        # Initialize a list to store all lines
        all_lines = []

        # Iterate over each file
        for file_name in files_to_combine:
            print(f"Processing file: {file_name}")
            blob = bucket.get_blob(file_name)
            with gzip.open(blob.open("rb"), 'rt') as f_in:
                # Read lines from the compressed file
                lines = f_in.readlines()
                # Append lines to all_lines
                all_lines.extend(lines)

        f_out.writelines(all_lines)

    print(f"Combined file {output_file_path} created successfully.")

    if output_blob_path:
        # Upload the combined file to the output_blob_uri
        blob = bucket.blob(output_blob_path)
        blob.upload_from_filename(output_file_path)

        print(
            f"Combined file {output_file_path} uploaded to {output_blob_path}."
        )


@app.route('/')
def combine_files_http():
    # Get query parameters
    bucket_name = request.args.get('bucket_name')
    folder_path = request.args.get('folder_path')
    file_pattern = request.args.get('file_pattern')
    output_file_path = request.args.get('output_file_path')
    output_blob_path = request.args.get('output_blob_path', default=None)

    # Call the function to combine files
    combine_files(bucket_name, folder_path, file_pattern,
                  output_file_path, output_blob_path)

    ret = {'message': 'Combined file created successfully.'}
    if output_blob_path:
        ret['output_blob_path'] = f"gs://{bucket_name}/{output_blob_path}"

    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
