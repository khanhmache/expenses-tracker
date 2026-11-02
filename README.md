
# Expense Tracker API

A simple expense tracking REST API built with
Python, FastAPI and Pydantic.

## Features

Create, read, update and delete expenses.

## Setup

Create and activate a Python virtual environment.

Install dependencies:

python -m pip install fastapi uvicorn pytest httpx

## Run the API

python -m uvicorn main:app --reload

API documentation:
http://127.0.0.1:8000/docs

## Run Tests

python -m pytest -v

## Current Limitations

Expenses are stored in memory and disappear
when the application restarts.

add for tests improve
