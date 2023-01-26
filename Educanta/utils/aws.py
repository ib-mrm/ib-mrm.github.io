import boto3
import uuid 

from werkzeug.utils import secure_filename
from context import config 

s3 = boto3.client(
    "s3",
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key
)

def upload_file_to_s3(file, bucket=config.template_bucket, randomize_filename=True):
    
    file_extension = file.filename.split(".")[-1]

    if randomize_filename:
        filename = ".".join([secure_filename(uuid.uuid4().hex), file_extension])
    else:
        filename = secure_filename(file.filename)
    
    try:
        s3.upload_fileobj(
            file,
            bucket,
            filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    # after upload file to s3 bucket, return filename of the uploaded file
    return filename