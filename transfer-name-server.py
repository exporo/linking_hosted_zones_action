import boto3
import os
import ast

sub_route53=boto3.client('route53',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_DEFAULT_REGION'])
sub_account_id=boto3.client('sts',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_DEFAULT_REGION']).get_caller_identity()['Account']
root_route53=boto3.client('route53',
    aws_access_key_id=os.environ['AWS_ROOT_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_ROOT_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_DEFAULT_REGION'])
record_name=os.environ['RECORD_NAME']
root_hosted_zone_name=os.environ['ROOT_HOSTED_ZONE_NAME']

def check_if_existing():
    global sub_route53
    global root_route53
    global record_name
    global root_hosted_zone_name

    sub_record = get_record_set(sub_route53, record_name)
    print(sub_record)
    print()
    root_record = get_record_set(root_route53, root_hosted_zone_name)
    print(root_record)
    print()
    if root_record != None:
        if root_record == sub_record:
            print('The Root Account is already set up to forward to the Sub Account with {} dns requests'.format(record_name))
            exit(0)
        else:
           print('ERROR: Root Account already has a record for {} and it does not match the one from the Sub Account'.format(record_name)) 
           exit(1)
    else:
        deploy_names_server_to_root(sub_record)

def get_record_set(route53, hosted_zone_name):
    global record_name
    results=None
    
    hosted_zone=route53.list_hosted_zones_by_name(DNSName=hosted_zone_name)
    hosted_zone_name=str(hosted_zone['HostedZones'][0]['Name']).rstrip('.')
    hosted_zone_id=str(hosted_zone['HostedZones'][0]['Id']).replace('/hostedzone/','')
    try:
        record_sets=route53.list_resource_record_sets(HostedZoneId='{}'.format(hosted_zone_id),
            StartRecordName=record_name,
            StartRecordType='NS'
            )['ResourceRecordSets']
        if str(record_sets) == '[]' or str(record_sets[0]['Name']).rstrip('.') != record_name:
            return None 
        else:
            return str(record_sets[0]).lstrip('{').rstrip('}')
    except:
        if hosted_zone==None:
            print('ERROR: Was unable to get the hosted zone. Please check the Access Key and Secret Key')
            exit(1)
        elif hosted_zone_name==None:
            print('ERROR: Was unable to find the hosted zone {}'.format(hosted_zone_name))
            exit(1)
        elif hosted_zone_id==None:
            print('ERROR: Was unable to get the ID for hosted zone {}'.format(hosted_zone_name))
            exit(1)
        elif results==None and record_name is hosted_zone_name:
            print('ERROR: Could not find the name server {} inside the hosted zone {}'.format(record_name,hosted_zone_name))
            exit(1)
        else:
            print('ERROR: Was unable to get Name Server')
            exit(1)

def deploy_names_server_to_root(record):
    global root_route53
    global sub_account_id
    global record_name
    global root_hosted_zone_name
    try:
        root_hosted_zone_id=str(root_route53.list_hosted_zones_by_name(DNSName=root_hosted_zone_name)['HostedZones'][0]['Id']).replace('/hostedzone/','')
    except:
        print('ERROR: Could not find the root hosted zone {}'.format(root_hosted_zone_name))
        exit(1)
    comment='Taking {} Name Server Record from Account {} and placing it in the Root Account Hosted Zone {}'.format(record_name,sub_account_id,root_hosted_zone_name)
    change_batch='{"Comment":"'+comment+'","Changes":[{"Action":"CREATE","ResourceRecordSet": {'+record+'}}]}'
    root_route53.change_resource_record_sets(
        HostedZoneId=root_hosted_zone_id,
        ChangeBatch=ast.literal_eval(change_batch))
    print('The Hosted Zone {} in Root Account has been successfully updated with {} Name Server'.format(root_hosted_zone_name, record_name))

check_if_existing()