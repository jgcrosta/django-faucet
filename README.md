# Ethereum Faucet

A Django-based Ethereum faucet application that allows users to request Sepolia ETH.

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (optional)
- An Infura account for Ethereum network access
- A wallet private key with some Sepolia ETH

## Local Development Setup

### Using Virtual Environment

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file with your actual values.

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

### Using Docker

1. Copy the environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your actual values.

3. Build and run with Docker Compose:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Environment Variables

The following environment variables are required:

- `WALLET_PRIVATE_KEY`: Your Ethereum wallet private key
- `INFURA_URL`: Your Infura project URL
- `ETH_AMOUNT`: Amount of ETH to send per request
- `RATE_LIMIT`: Rate limit for requests (e.g., "5/h" for 5 requests per hour)
- `DJANGO_SECRET_KEY`: Django secret key for security
- `DEBUG`: Set to True for development, False for production
