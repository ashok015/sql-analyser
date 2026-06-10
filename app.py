import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify
from datetime import datetime
import json

from database import init_database
from sql_generator import generate_sql
from sql_executor import execute_safe_query

app = Flask(__name__)

QUERY_LOG_FILE = 'query_logs.json'

def log_query(natural_query: str, generated_sql: str, results: list, error: str = None):
    """Log query execution to JSON file"""
    logs = []
    if os.path.exists(QUERY_LOG_FILE):
        with open(QUERY_LOG_FILE, 'r') as f:
            logs = json.load(f)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "natural_query": natural_query,
        "generated_sql": generated_sql,
        "results_count": len(results) if results else 0,
        "error": error
    }
    logs.append(log_entry)

    with open(QUERY_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/query', methods=['POST'])
def query():
    """
    POST /query
    Body: {"query": "natural language question"}
    Returns: {"sql": "...", "results": [...], "explanation": "..."}
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' field"}), 400

        natural_query = data['query'].strip()
        if not natural_query:
            return jsonify({"error": "Query cannot be empty"}), 400

        # Generate SQL
        sql, explanation = generate_sql(natural_query)
        if not sql:
            log_query(natural_query, None, [], explanation)
            return jsonify({"error": explanation}), 400

        # Execute SQL safely
        results, error, _ = execute_safe_query(sql)
        if error:
            log_query(natural_query, sql, [], error)
            return jsonify({"error": error, "sql": sql}), 400

        log_query(natural_query, sql, results or [])

        return jsonify({
            "success": True,
            "query": natural_query,
            "sql": sql,
            "explanation": explanation,
            "results": results,
            "result_count": len(results) if results else 0
        }), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/schema', methods=['GET'])
def schema():
    """Get database schema"""
    from database import get_schema_description
    return jsonify({"schema": get_schema_description()}), 200

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5001)
