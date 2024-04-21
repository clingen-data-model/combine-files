import requests

response = requests.get(
    "http://localhost:5000",
    params={
        "bucket_name": "clinvar-gk-pilot",
        "folder_path": "2024-04-07/dev/scv_subset_v2",
        "file_pattern": ".*.gzip",
        "output_file_path": "combined.gz",
        "output_blob_path": "2024-04-07/dev/combined-scv_subset_v2.csv.gz"
    })
