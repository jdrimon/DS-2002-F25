#!/usr/bin/env python3

# This python script is written as specified by part 5.

import boto3
import urllib.request

# Fetch a file from the internet
with urllib.request.urlopen('https://i.pinimg.com/originals/5b/f4/00/5bf400ba325e910a51c8431c68e80df7.gif') as f:
    with open('diamond.gif', 'wb') as out_file:
        out_file.write(f.read())

# Upload the file to S3 bucket
s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'ds2002-f25-ytt6hb'
local_file = 'diamond.gif'
with open(local_file, 'rb') as data:
    resp = s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=local_file
    )

# Presign file
expires_in = 60 # 1 minute
response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': local_file},
    ExpiresIn=expires_in
)

# Output presigned URL
print('Presigned URL:', response)