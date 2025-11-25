#!/bin/bash

# This bash script is written as specified by part 2.

aws s3 cp $2 s3://$1/
aws s3 presign --expires-in $3 s3://$1/$2