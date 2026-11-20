# AWS Serverless File Processing
An AWS SAM demo: S3 upload event -> SQS -> Lambda -> DynamoDB metadata + processed S3 JSON output.

## Deploy
Requires AWS CLI, SAM CLI, Python 3.12 and configured AWS credentials.
`sam build` then `sam deploy --guided`. Upload a file to the stack's upload bucket under `incoming/`.
Inspect the DynamoDB table and processed bucket from the stack outputs.
Run tests with `pip install -r requirements-dev.txt && pytest`.

This template creates billable AWS resources. Deploy only in an account you control and run
`sam delete` when finished. Never commit AWS keys. Add encryption, alarms, retention policies,
and a dead-letter queue before production use.
