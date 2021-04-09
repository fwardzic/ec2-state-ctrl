from app import app
from flask import render_template
import boto3
from botocore.exceptions import ClientError
import json
import jmespath
import itertools

@app.route('/')
def home():
   ec2 = boto3.client('ec2')
   response = ec2.describe_instances()
   AWS_InstanceID = jmespath.search('Reservations[*].Instances[*].InstanceId', response)
   AWS_Instance_Status = jmespath.search('Reservations[*].Instances[*].State.Name', response)
   AWS_Instance_Name = jmespath.search('Reservations[*].Instances[*].Tags[?Key==`Name`].Value', response)
   ## make simple flat list from each output
   ## AWS_Instance_Name is a list of nested list - require double flatten process.
   Flatten = itertools.chain.from_iterable
   AWS_InstanceID_flat = list(Flatten(AWS_InstanceID))
   AWS_Instance_Status_flat = list(Flatten(AWS_Instance_Status))
   AWS_Instance_Name_flat1 = list(Flatten(AWS_Instance_Name))
   AWS_Instance_Name_flat = list(Flatten(AWS_Instance_Name_flat1))

   return render_template('home.html', AWS_instances=zip(AWS_Instance_Name_flat, AWS_InstanceID_flat, AWS_Instance_Status_flat))

@app.route('/stop')
def stop():
   ec2 = boto3.client('ec2')
   response = ec2.describe_instances()
   AWS_InstanceID = jmespath.search('Reservations[*].Instances[*].InstanceId', response)
   Flatten = itertools.chain.from_iterable
   AWS_InstanceID_flat = list(Flatten(AWS_InstanceID))
   CurrentState_List = []
   InstanceId_List = []
   for instance_id in AWS_InstanceID_flat:
      try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
      except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

      # Dry run succeeded, run start_instances without dryrun
      try:
          response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
      except ClientError as e:
          print(e)
      CurrentState = jmespath.search('StoppingInstances[0].CurrentState.Name', response)
      InstanceId = jmespath.search('StoppingInstances[0].InstanceId', response)
      CurrentState_List.append(CurrentState)
      InstanceId_List.append(InstanceId)

   return render_template('stop.html', AWS_Stopped_Instances=zip(InstanceId_List, CurrentState_List))

@app.route('/start')
def start():
   ec2 = boto3.client('ec2')
   response = ec2.describe_instances()
   AWS_InstanceID = jmespath.search('Reservations[*].Instances[*].InstanceId', response)
   Flatten = itertools.chain.from_iterable
   AWS_InstanceID_flat = list(Flatten(AWS_InstanceID))
   CurrentState_List = []
   InstanceId_List = []
   for instance_id in AWS_InstanceID_flat:
      try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
      except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

      # Dry run succeeded, run start_instances without dryrun
      try:
          response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
      except ClientError as e:
          print(e)
      CurrentState = jmespath.search('StartingInstances[0].CurrentState.Name', response)
      InstanceId = jmespath.search('StartingInstances[0].InstanceId', response)
      CurrentState_List.append(CurrentState)
      InstanceId_List.append(InstanceId)

   return render_template('start.html', AWS_Started_Instances=zip(InstanceId_List, CurrentState_List))