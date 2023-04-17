# Papaya

> A fun GroupMe chat bot using GPT 3.5 Turbo.

## Prerequisites
Papaya is meant to run on AWS Lambda using the Serverless framework.

To install serverless on your local machine:
```sh
npm install -g serverless
```

## Deployment
Install `pip` dependencies locally in the `vendor` directory:
```sh
pip install -r requirements.txt -t vendor
```

Deploy using serverless:
```sh
serverless deploy
```

Later, to view the logs:
```sh
serverless logs -f receive
```
