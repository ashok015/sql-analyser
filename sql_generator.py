from groq import Groq
from database import get_schema_description
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(natural_language_query: str) -> tuple[str, str]:
    """
    Convert natural language query to SQL using Groq API.
    Returns (sql_query, explanation)
    """
    schema = get_schema_description()

    prompt = f"""You are a SQL expert. Convert the following natural language query into valid SQL.

{schema}

Natural Language Query: {natural_language_query}

Rules:
1. Return ONLY valid SQL that can be executed against SQLite
2. Use table names and columns exactly as defined above
3. Include a brief explanation after the SQL

Format your response as:
SQL: [your sql query here]
Explanation: [brief explanation]
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content

        # Extract SQL from markdown code blocks or explicit SQL: format
        import re

        sql = None
        explanation = None

        # Try to extract from ```sql ... ``` blocks
        sql_match = re.search(r'```(?:sql)?\s*\n?(.*?)\n?```', content, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1).strip()
        else:
            # Try SQL: format
            lines = content.strip().split('\n')
            for i, line in enumerate(lines):
                if line.startswith('SQL:'):
                    sql = line.replace('SQL:', '').strip()

        # Extract explanation
        exp_match = re.search(r'Explanation:\s*(.+?)(?:\n|$)', content)
        if exp_match:
            explanation = exp_match.group(1).strip()

        return sql, explanation or "SQL generated successfully"

    except Exception as e:
        return None, f"Error generating SQL: {str(e)}"
