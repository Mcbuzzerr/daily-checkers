## The Daily Checkers

The Daily Checkers is an asynchronous checkers game that you can play with others! You take turns making moves, but only one move per game per day,

## Pre-requisites

- AWS CLI already configured with Administrator permission
- [Docker installed](https://www.docker.com/community-edition)
- [SAM CLI installed](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Live Server Extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) for VS Code

## Starting the project

The backend is built using AWS SAM and the frontend is built using vanilla HTML, CSS, and JavaScript.

To run API locally

```bash
sam local start-api
```

To Deploy API

```bash
sam build && sam deploy --no-confirm-changeset
```

To run frontend locally us a live server extension in vs-code or open the index.html file in a browser.