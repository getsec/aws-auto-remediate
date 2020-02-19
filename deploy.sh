

NAME="AWSAutoRemediations"
ENV="PROD"
S3_BUCKET="getty-sam-templates-canada"
SAM_FORMATED_FILE_NAME="out-$ENV.yaml"
REGION="ca-central-1"

# this step is needed to build python deps.... yeah i know, dum
sam build -m lambda/requirements.txt


sam package -t .aws-sam/build/template.yaml \
    --s3-bucket  $S3_BUCKET  \
    --output-template-file $SAM_FORMATED_FILE_NAME \
    --region $REGION


sam deploy --template-file $SAM_FORMATED_FILE_NAME \
    --capabilities CAPABILITY_NAMED_IAM \
    --stack-name "$NAME-$ENV" \
    --region $REGION