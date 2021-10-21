import boto3
import os
from flask import Flask
from ec2_metadata import ec2_metadata
from botocore.exceptions import ClientError

app = Flask(__name__)

@app.route("/tags")
def retrieve_tags():
    ec2 = boto3.client('ec2', region_name="us-east-2")

    response = ec2.describe_instances()
    
    for reserv in response["Reservations"]:
        for instance in reserv["Instances"]:
            if instance["InstanceId"] == ec2_metadata.instance_id:
                print(instance["Tags"])

@app.route("/shutdown")
def shutdown_instance():
    current_instance = ec2_metadata.instance_id
    try:
        ec2.stop_instances(InstanceIds=[str(current_instance)], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print("You don't have permission to reboot instances.")
            raise
