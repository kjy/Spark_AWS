This is the dataset we will use to run our analyses.

It is a subset of the files in the full Gutenberg project.

You need to get this dataset into your own S3 bucket.

To do that, create a bucket using the AWS management console

SSH into your EC2 Spark master

Run these commands to set up your shell environment (edit as appropriate):
```
export AWS_SECRET_ACCESS_KEY=PUT YOUR KEY HERE
export AWS_ACCESS_KEY_ID=PUT YOUR KEY HERE
```

Edit the python script upload_data.py, put in your bucket name to the variable S3_BUCKET_NAME

Finally, run the upload_data.py script:

```
python3 upload_data.py
```

It should upload all the files from the gutenberg_sub folder to your bucket.
