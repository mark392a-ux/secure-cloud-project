import os

import boto3


BUCKET_NAME = os.getenv("AWS_S3_BUCKET")
REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if not BUCKET_NAME:
    raise RuntimeError("AWS_S3_BUCKET is not set. Add it to your environment.")

client_kwargs = {"region_name": REGION}
if AWS_ACCESS_KEY and AWS_SECRET_KEY:
    client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY
    client_kwargs["aws_secret_access_key"] = AWS_SECRET_KEY

s3 = boto3.client("s3", **client_kwargs)


def upload_to_s3(username, filename, data):
    key = f"{username}/{filename}"
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=data)


def download_from_s3(username, filename):
    key = f"{username}/{filename}"
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return obj["Body"].read()


def list_files(username):
    prefix = f"{username}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

    files = []
    if "Contents" in response:
        for item in response["Contents"]:
            key = item["Key"]
            name = key.replace(prefix, "")
            if name:
                files.append(name)

    return files


def delete_from_s3(username, filename):
    key = f"{username}/{filename}"
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
