import subprocess
import requests
from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import id_token
# from google.auth import compute_engine


# response = requests.get(
#     "http://localhost:5000",
#     params={
#         "bucket_name": "clinvar-gk-pilot",
#         "folder_path": "2024-04-07/dev/scv_subset_v2",
#         "file_pattern": ".*.gzip",
#         "output_file_path": "combined.json.gz",
#         "output_blob_path": "2024-04-07/dev/combined-scv_subset_v2.json.gz"
#     })


# catvars
# clinvar-gk-pilot/2024-04-07/dev/catvar_output_v2
dir_basename = "catvar_output_v2"
catvars_params = {
    "bucket_name": "clinvar-gk-pilot",
    "folder_path": f"2024-04-07/dev/{dir_basename}",
    "file_pattern": ".*.gzip",
    "output_file_path": f"combined-{dir_basename}.json.gz",
    "output_blob_path": f"2024-04-07/dev/combined-{dir_basename}.json.gz"
}


def request_local():
    response = requests.get(
        "http://localhost:5000",
        timeout=30*60,
        params=catvars_params
    )
    return response


# def get_id_token(audience):
#     # Load the default credentials
#     creds, _ = default(
#         scopes=["https://www.googleapis.com/auth/cloud-platform"])
#     # Request the token using the credentials and the specified audience
#     if not creds.valid:
#         creds.refresh(Request())
#     # The audience typically is the URL of the service you want to access
#     id_token_creds = id_token.IDTokenCredentials.from_credentials(
#         creds, audience)
#     id_token_creds.refresh(Request())
#     return id_token_creds.token


def request_cloud():
    service_url = "https://combine-files-wawwp3ppza-ue.a.run.app"
    # request = Request()

    _id_token = subprocess.check_output(
        'gcloud auth print-identity-token', shell=True).decode("utf-8").strip()

    print(f"{_id_token=}")

    response = requests.get(
        service_url,
        headers={"Authorization": f"Bearer {_id_token}"},
        timeout=30*60,
        params=catvars_params
    )
    return response


print(request_cloud().text)
