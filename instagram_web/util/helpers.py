import os
import boto3, botocore
import sendgrid
from sendgrid.helpers.mail import *

from flask import Flask, request, flash, url_for, render_template, redirect
from app import app

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs = {
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception
        print("Something happened!", e)
        return e
    
    return f"{file.filename}"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def deliver_email():
    from_email = Email("admin@flaskagram.com")
    to_email = Email("suzukisteven@gmail.com")
    subject = "Thank you for your generosity!"
    content = Content("text/plain", "Your donation was received.")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
