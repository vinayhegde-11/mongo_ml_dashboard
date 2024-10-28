import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from config_loader import load_config
from push_to_db import get_image_path

config = load_config('config.yml')

def upload_to_s3(file_path):
    try:
        # Load credentials and bucket name from config
        aws_access_key = config['aws_access_key_id']
        aws_secret_key = config['aws_secret_access_key']
        bucket_name = config['s3_bucket_name']

        # Initialize S3 client with credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        # Extract the relative file path for S3 key
        s3_key = "/".join(file_path.split("/")[-2:])

        # Upload file
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File uploaded successfully to {bucket_name}/{s3_key}")
        return f"{bucket_name}/{s3_key}"
    except FileNotFoundError:
        print("The file was not found.")
        return None
    except NoCredentialsError:
        print("Credentials not available. Check your AWS access key and secret key.")
        return None
    except KeyError as e:
        print(f"Missing configuration for {e}. Check config file.")
        return None
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
        return None

if __name__ == "__main__":
    result = upload_to_s3("2024-10-22/hrse.jpg")
    print(result)
