from pathlib import Path

import boto3
from tqdm import tqdm


class S3(object):
    __access_key: str
    __secret_key: str
    bucket_name: str
    endpoint: str

    def __new__(cls, access_key: str, secret_key: str, bucket_name: str, endpoint: str):
        instance = super(S3, cls).__new__(cls)
        return instance

    def __init__(self, access_key: str, secret_key: str, bucket_name: str, endpoint: str):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint = endpoint

    def upload_file(self, file_path: str, remote_path: str, content_type: str = "binary/octet-stream"):
        """
        Upload a file to an S3 bucket.

        @param file_path: path to the file to be uploaded
        @param remote_path: remote path of the file
        @param content_type: MIME type of the file
        @return: return 1 if fails with error message, 0 otherwise
        """

        session = boto3.Session()
        s3 = session.resource("s3",
                              endpoint_url=self.endpoint,
                              aws_access_key_id=self.__access_key,
                              aws_secret_access_key=self.__secret_key
                              )
        file_size = Path(file_path).stat().st_size
        with tqdm(total=file_size, unit='B', unit_scale=True, position=1, leave=None, dynamic_ncols=True) as pbar:
            s3.Bucket(self.bucket_name).upload_file(
                file_path,
                remote_path,
                ExtraArgs={'ContentType': content_type},
                Callback=pbar.update
            )
