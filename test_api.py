#!/usr/bin/env python3
"""
Test script to demonstrate AI SQL Assistant API usage.
Run the server first: python app.py
Then run this: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_schema():
    print("\n=== Testing Schema Endpoint ===")
    response = requests.get(f"{BASE_URL}/schema")
    print(f"Status: {response.status_code}")
    print(f"Schema:\n{response.json()['schema']}")

def test_query(natural_query):
    print(f"\n=== Query: {natural_query} ===")
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": natural_query},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    data = response.json()

    if response.status_code == 200:
        print(f"Generated SQL: {data['sql']}")
        print(f"Explanation: {data['explanation']}")
        print(f"Results ({data['result_count']} rows):")
        for row in data['results']:
            print(f"  {dict(row)}")
    else:
        print(f"Error: {data['error']}")

if __name__ == "__main__":
    print("AI SQL Assistant - API Test Script")
    print("=" * 50)

    try:
        test_health()
        test_schema()

        # Test various queries
        test_queries = [
            "Show me all customers",
            "What are the names and emails of customers from the USA?",
            "List all products with their prices",
            "How many orders are there?",
            "Show me products in the Electronics category",
            "Which customer has placed the most orders?",
        ]

        for query in test_queries:
            test_query(query)

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server.")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
