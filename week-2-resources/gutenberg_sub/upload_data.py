## Run this script to upload your own copy of the gutenberg dataset into
## your own S3 bucket.

## It will list your available buckets, then attempt to upload
## the content to the bucket you specified in the S3_BUCKET_NAME variable
## below.

## It assumes that you have created some environmemnt variables
## which allow it to access your AWS account:
## export AWS_SECRET_ACCESS_KEY=PUT YOUR KEY HERE
## export AWS_ACCESS_KEY_ID=PUT YOUR KEY HERE

import boto3
import botocore
import os.path

# edit this value to the name of the bucket you created in your AWS account
S3_BUCKET_NAME = 'bucketsparkpgexamples'

def file_to_string(filename):
    """
    reads the sent file from disk and returns contents as a string
    """
    with open (filename, "r") as myfile:
        data=myfile.read()
    return data

def get_files_to_upload(csv_file):
    try:
        data_file = csv_file
        files_to_upload = []
        data = file_to_string(data_file)
    except:
        print ("ERROR: Data file looks bad: "+csv_file)

    for line in data.split('\n'):
        # file path is the second column
        try:
            file_path = line.split(',')[1].strip()
            #print (file_path)
            if file_path.endswith('.txt'):
                files_to_upload.append(file_path)
            elif file_path.endswith('.rdf'):
                files_to_upload.append(file_path)
        except:
            continue

    return files_to_upload

if __name__ == '__main__':

    s3 = boto3.resource('s3')
    print ("Connecting to AWS and listing your buckets...")
    buckets = []
    # try and get a list of buckets
    try:
        buckets = [bucket.name for bucket in s3.buckets.all()]
    except botocore.exceptions.NoCredentialsError:
        print ("ERROR: No AWS credentials found. Did you set the AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID environment variables?")
        exit(0)
    except botocore.exceptions.ClientError:
        print ("ERROR: AWS credentials set but they do not work. Check your AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID environment variables")
        exit(0)
    # now check if we found the bucket
    if (S3_BUCKET_NAME in buckets) == False:
        print ("ERROR - requested bucket not found. You asked for '"+S3_BUCKET_NAME+"' but you only have these: "+str(buckets) + ' did you create a bucket in the AWS manager?')
        exit(0)
    # get a list of files to upload from the CSV file
    csv_file = 'gp_200mb.csv'
    if os.path.isfile(csv_file) == False:
        print ("ERROR: The data file index "+csv_file+" does not exist. Have you unzipped the dataset gutenberg_dataset.zip into this folder?")
        exit(0)
    files_to_upload = get_files_to_upload(csv_file)
    # now upload all the files listed in the CSV file...
    for filename in files_to_upload:
        filename = 'gutenberg_dataset/'+filename
        print ("Attempting to upload a book... "+filename)
        if os.path.isfile(filename) == False:
            print ('ERROR: cannot find file '+filename+' did you unzip the dataset gutenberg_dataset.zip into this folder?')
            exit(0)
        data = open(filename, 'rb')
        try:
            s3.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=data)
        except botocore.exceptions.ClientError:
            print ("ERROR: Something went wrong talking to AWS")
            exit(0)
        print ("Success!")
