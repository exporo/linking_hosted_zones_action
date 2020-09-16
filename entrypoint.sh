#!/bin/bash
#This if statement is for use of github actions.
if [ -z "$AWS_DEFAULT_REGION" ]
then
    if [ -z "$INPUT_REGION" ]
    then
        echo "Could not find value for AWS_DEFAULT_REGION"
        exit 1
    else
        export AWS_DEFAULT_REGION=$INPUT_REGION
    fi
fi
if [ -z "$AWS_ACCESS_KEY_ID" ]
then

    if [ -z "$INPUT_ACCESS" ]
    then
        echo "Could not find value for AWS_ACCESS_KEY_ID"
        exit 1
    else
        export AWS_ACCESS_KEY_ID=$INPUT_ACCESS
    fi
fi
if [ -z "$AWS_SECRET_ACCESS_KEY" ]
then
    if [ -z "$INPUT_SECRET" ]
    then
        echo "Could not find value for AWS_SECRET_ACCESS_KEY"
        exit 1
    else
        export AWS_SECRET_ACCESS_KEY=$INPUT_SECRET
    fi
fi
if [ -z "$AWS_ROOT_ACCESS_KEY_ID" ]
then
    if [ -z "$INPUT_ROOT_ACCESS" ]
    then
        echo "Could not find value for AWS_ROOT_ACCESS_KEY_ID"
        exit 1
    else
        export AWS_ROOT_ACCESS_KEY_ID=$INPUT_ROOT_ACCESS
    fi
fi
if [ -z "$AWS_ROOT_SECRET_ACCESS_KEY" ]
then

    if [ -z "$INPUT_ROOT_SECRET" ]
    then
        echo "Could not find value for AWS_ROOT_SECRET_ACCESS_KEY"
        exit 1
    else
        export AWS_ROOT_SECRET_ACCESS_KEY=$INPUT_ROOT_SECRET
    fi
fi
if [ -z "$RECORD_NAME" ]
then

    if [ -z "$INPUT_RECORD" ]
    then
        echo "Could not find value for RECORD_NAME"
        exit 1
    else
        export RECORD_NAME=$INPUT_RECORD
    fi
fi
if [ -z "$ROOT_HOSTED_ZONE_NAME" ]
then

    if [ -z "$INPUT_ROOT_RECORD" ]
    then
        echo "Could not find value for ROOT_HOSTED_ZONE_NAME"
        exit 1
    else
        export ROOT_HOSTED_ZONE_NAME=$INPUT_ROOT_RECORD
    fi
fi

#Makes sure script is executable
chmod u+x transfer-name-server.py

#Runs python script
python transfer-name-server.py