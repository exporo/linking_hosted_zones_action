# Linking Hosted Zones

## Summary
This repo creates a docker image that can be used by CircleCI and DockerCompose, as well as a Github Action that can be used in Github Workflows. It allows the pipelines to link a sub-domain that is hosted on a sub-account with the primary domain that is hosted in root account(or another account).

## When updating
Make sure you run the following commands when updating the action:
```
git add --all
git commit -m 'Updating action'
git push --follow-tags -u origin master
```

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
Just add the job link_hosted_zone to your code (You can also add it as a step in your current job). You will need to use Secrets for the Access and Secret Keys for AWS. As well as change the RECORD_NAME to be the subdomain that will be linked to sub-account and change the ROOT_HOSTED_ZONE_NAME to be the primary domain that RECORD_NAME needs to be linked to.
#### As a job
```
jobs:
  hosted_zone:
    name: Deploys Test Hosted Zone
    runs-on: ubuntu-latest
    env:
        AWS_REGION: eu-central-1
        ACCOUNT_ID: 770047734416
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_SANDBOX_ACCESS_KEY }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SANDBOX_SECRET_KEY }}
        ZONE_NAME: testhostedzone.exporo.io
  link_hosted_zone:
    name: Links Name Server to Root
    needs: [hosted_zone]
    runs-on: ubuntu-latest
    steps:
      - name: Links Hosted Zone to Root Account
        uses: exporo/linking_hosted_zones@v1
        with:
            region: eu-central-1
            access: ${{ secrets.AWS_SUBACCOUNT_ACCESS_KEY }}
            secret: ${{ secrets.AWS_SUBACCOUNT_SECRET_KEY }}
            root_access: ${{ secrets.ROOT_ACCESS_KEY }}
            root_secret: ${{ secrets.ROOT_SECRET_KEY }}
            record: testhostedzone.test.io
            root_record: test.io
```
#### As a step
```
jobs:
  hosted_zone:
    steps:
      - name: Deploys Test Hosted Zone
        runs-on: ubuntu-latest
        env:
            AWS_REGION: eu-central-1
            ACCOUNT_ID: 111111111111
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_SUBACCOUNT_ACCESS_KEY }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SUBACCOUNT_SECRET_KEY }}
            ZONE_NAME: testhostedzone.exporo.io
      - name: Links Hosted Zone to Root Account
        uses: exporo/linking_hosted_zones@v2
        with:
        region: eu-central-1
            access: ${{ secrets.AWS_SUBACCOUNT_ACCESS_KEY }}
            secret: ${{ secrets.AWS_SUBACCOUNT_SECRET_KEY }}
            root_access: ${{ secrets.ROOT_ACCESS_KEY }}
            root_secret: ${{ secrets.ROOT_SECRET_KEY }}
            record: testhostedzone.test.io
            root_record: test.io
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