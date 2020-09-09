# Linking Hosted Zones

## Summary
This container can be added to Github and CircleCI pipelines that will link together the primary domain that is hosted in another account (or root account) and the subdomain.

## Requirements
 - The Sub Account user needs to have permission to view DNS records in Route53 as well as get caller identity in STS. The minimum requirements are show below:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "route53:ListResourceRecordSets",
                "Resource": "arn:aws:route53:::hostedzone/*"
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": [
                    "sts:GetCallerIdentity",
                    "route53:ListHostedZonesByName"
                ],
                "Resource": "*"
            }
        ]
    }
    ```
 - The Root Account user (or primary Route53 account) needs to have a user to read and create a DNS record in Route 53. The minimum requirements are show below:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "route53:ChangeResourceRecordSets",
                    "route53:ListResourceRecordSets"
                ],
                "Resource": "arn:aws:route53:::hostedzone/*"
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": "route53:ListHostedZonesByName",
                "Resource": "*"
            }
        ]
    }
    ```

## Examples to add to pipeline
### Example use for Github Actions
Just add the job link_hosted_zone to your code. You will need to use Secrets for the Access and Secret Keys for AWS. As well as change the RECORD_NAME to be the subdomain that will be linked to sub-account and change the ROOT_HOSTED_ZONE_NAME to be the primary domain that RECORD_NAME needs to be linked to.
```
jobs:
  link_hosted_zone:
    name: Links Name Server to Root
    runs-on: docker.pkg.github.com/exporo/hosted_name_transfer/hosted_name_transfer:latest
    env:
        AWS_DEFAULT_REGION: eu-central-1
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_SUB_ACCOUNT_ROOT_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SUB_ACCOUNT_ACCESS_KEY }}
        AWS_ROOT_ACCESS_KEY_ID: ${{ secrets.AWS_ROOT_KEY_ID }}
        AWS_ROOT_SECRET_ACCESS_KEY: ${{ secrets.AWS_ROOT_SECRET_ACCESS_KEY }}
        RECORD_NAME: test.test.io
        ROOT_HOSTED_ZONE_NAME: test.io
    steps:
      - name: Runs Python Script
        run: python transfer-name-server.py
```

### Example use for Circle CI
Just add the job link_hosted_zone to your code. You will need to use Secrets for the Access and Secret Keys for AWS. As well as change the RECORD_NAME to be the subdomain that will be linked to sub-account and change the ROOT_HOSTED_ZONE_NAME to be the primary domain that RECORD_NAME needs to be linked to.
```
jobs:
  link_hosted_zone:
    docker:
        image: docker.pkg.github.com/exporo/hosted_name_transfer/hosted_name_transfer:latest
        environment:   
            AWS_DEFAULT_REGION: eu-central-1
            AWS_ACCESS_KEY_ID: $AWS_SUB_ACCOUNT_ROOT_KEY_ID
            AWS_SECRET_ACCESS_KEY: $AWS_SUB_ACCOUNT_ACCESS_KEY
            AWS_ROOT_ACCESS_KEY_ID: $AWS_ROOT_KEY_ID
            AWS_ROOT_SECRET_ACCESS_KEY: $AWS_ROOT_SECRET_ACCESS_KEY
            RECORD_NAME: test.test.io
            ROOT_HOSTED_ZONE_NAME: test.io
```