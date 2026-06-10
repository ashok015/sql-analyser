import re
from database import execute_query

FORBIDDEN_KEYWORDS = ['DELETE', 'DROP', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'ATTACH', 'PRAGMA']

def is_sql_safe(sql: str) -> tuple[bool, str]:
    """
    Validate that SQL is safe to execute.
    Returns (is_safe, message)
    """
    if not sql:
        return False, "Empty SQL query"

    # Normalize SQL for checking
    normalized = sql.strip().upper()

    # Check for destructive operations
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf'\b{keyword}\b', normalized):
            return False, f"Destructive operation '{keyword}' is not allowed"

    # Check for comment injection
    if '--' in sql or '/*' in sql:
        return False, "SQL comments are not allowed"

    return True, "SQL is safe"

def execute_safe_query(sql: str) -> tuple[list, str, str]:
    """
    Execute SQL after safety validation.
    Returns (results, error, explanation)
    """
    is_safe, message = is_sql_safe(sql)
    if not is_safe:
        return None, message, ""

    results, error = execute_query(sql)
    if error:
        return None, error, ""

    return results, None, ""
