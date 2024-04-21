import os
import re
import gzip
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

def combine_files(bucket_name, folder_path, file_pattern, output_file_path):
    
    # Initialize Google Cloud Storage client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    if bucket is None:
        print("{bucket_name} bucket not found.")
        return

    # List all files in the folder matching the file pattern
    blobs = bucket.list_blobs(prefix=folder_path)

    if blobs is None:
        print("No blobs found in {folder_path}.")
        return

    files_to_combine = [blob.name for blob in blobs if re.match(file_pattern, os.path.basename(blob.name))]

    if len(files_to_combine) == 0:
        print("No files found matching pattern {file_pattern} to combine.")
        return

    # Initialize a list to store all lines
    all_lines = []

    # Iterate over each file
    for file_name in files_to_combine:
        print(f"Processing file: {file_name}")
        blob = bucket.get_blob(file_name)
        with gzip.open(blob.download_as_string(), 'rt') as f:
            # Read lines from the compressed file
            lines = f.readlines()
            # Append lines to all_lines
            all_lines.extend(lines)

    # Write all lines to the output file
    with gzip.open(output_file_path, 'wt') as f:
        f.writelines(all_lines)

    print("Combined file {output_file_path} created successfully.")

@app.route('/')
def combine_files_http():
    # Get query parameters
    bucket_name = request.args.get('bucket_name')
    folder_path = request.args.get('folder_path')
    file_pattern = request.args.get('file_pattern')
    output_file_path = request.args.get('output_file_path')

    # Call the function to combine files
    combine_files(bucket_name, folder_path, file_pattern, output_file_path)

    return jsonify({'message': 'Combined file created successfully.'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
