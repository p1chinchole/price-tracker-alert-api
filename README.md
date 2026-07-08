# Price Tracker & Alert API

A professional Django REST API for tracking product prices, scraping product data, and sending alerts when prices cross a user-defined threshold.

## Overview

This project provides a backend service that allows users to:
- register and authenticate securely
- track products by URL and source site
- store price history over time
- receive alert notifications when prices change
- use a scraper pipeline for collecting product price data

## Tech Stack

- Python
- Django
- Django REST Framework
- JWT Authentication
- Celery + Redis
- Scrapy
- SQLite by default

## Project Structure

- api: authentication and API endpoints
- pricing: product tracking, pricing history, and alerts
- scraper: scraping logic and spider integration
- notifications: alert-related background tasks
- price_tracker_api: Django project configuration

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/p1chinchole/price-tracker-alert-api.git
cd price-tracker-alert-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and update it as needed:

```bash
copy .env.example .env
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

## API Endpoints

The API exposes endpoints for:
- user registration: `/api/register/`
- JWT token authentication: `/api/token/`
- products: `/api/products/`
- tracked products: `/api/tracked-products/`
- alerts: `/api/alerts/`

## Testing

Run the test suite with:

```bash
python manage.py test
```

## Contributing

Contributions are welcome. Please review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is intended for learning and development purposes.
