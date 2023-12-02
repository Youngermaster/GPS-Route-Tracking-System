# Backend API

This repository contains the backend API, built using FastAPI and MongoDB.

## Project Structure

```plaintext
.
├── app
│   ├── main.py
│   └── server
│       ├── app.py
│       ├── config.py
│       ├── database
│       ├── dependencies.py
│       ├── graphql
│       ├── models
│       └── routes
├── db
│   └── docker-compose.yaml
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── static
│   ├── icons
│   └── projects
└── tests
```

## Environment Setup

To set up the project, copy the `.env.example` file to a new file named `.env` and modify the environment variables according to your setup.

```plaintext
MONGO_URL="mongodb://root:examplepassword@localhost:27017/?authMechanism=DEFAULT"
SECRET_KEY="your_secret_key"
PORT=8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_ENVIRONMENT="DEVELOPMENT" # Or use RELEASE
```

## Running the Application

### Using Docker

You can easily run the entire application stack using Docker Compose:

```bash
docker-compose up -d
```

This will set up the MongoDB instance and the FastAPI application.

### Manually

If you prefer to run the application without Docker, follow these steps:

1. Ensure MongoDB is running on your system.
2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

3. Run the FastAPI application:

```bash
python app/main.py
```

## Testing

To run the automated tests for the API:

```bash
# Command to run tests
```
