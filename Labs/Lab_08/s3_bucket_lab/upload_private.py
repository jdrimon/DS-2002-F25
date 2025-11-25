#!/usr/bin/env python3

# This python script is written as specified by part 4.2.

import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'ds2002-f25-ytt6hb'
local_file = 'gmail_emblem.png'

with open(local_file, 'rb') as data:
    resp = s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=local_file
    )