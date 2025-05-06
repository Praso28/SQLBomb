import re
from backend.utils import check_stage_completion

def start_timer():
    """Start a timer for the game - now just returns a placeholder value"""
    return 1  # Placeholder value since we're removing the timer concept

def validate_query(query):
    """
    Validate SQL query for safety and game rules
    - No DROP, DELETE, UPDATE, INSERT statements allowed
    - No system table access
    - Only SELECT statements allowed
    - JOIN operations are allowed
    """
    # Convert to lowercase for easier checking
    query_lower = query.lower().strip()

    # Check if it's a SELECT statement
    if not query_lower.startswith('select'):
        return False

    # Check for forbidden operations - using word boundaries to avoid false positives
    forbidden_operations = [
        r'\bdrop\b', r'\bdelete\b', r'\bupdate\b', r'\binsert\b',
        r'\balter\b', r'\bcreate\b', r'\btruncate\b', r'\bgrant\b',
        r'\brevoke\b'
    ]

    # Check for system tables
    forbidden_tables = [
        r'\bpg_\w+\b', r'\binformation_schema\b', r'\bsqlite_\w+\b'
    ]

    # Check for forbidden operations
    for pattern in forbidden_operations:
        if re.search(pattern, query_lower):
            return False

    # Check for system tables
    for pattern in forbidden_tables:
        if re.search(pattern, query_lower):
            return False

    # Basic SQL injection prevention - but allow semicolons in string literals
    # This is a simplified check and not foolproof
    if '--' in query:
        return False

    # Allow JOIN operations and other valid SQL constructs
    return True

def update_game_state(current_stage, results, game_state):
    """
    Update game state based on query results and current stage
    Returns: (bool) whether the stage was completed
    """
    # Check if the current stage is completed
    stage_completed = check_stage_completion(current_stage, results)

    if stage_completed:
        if current_stage == 1:
            # Found the real bomb
            # Check if results are dictionaries or tuples
            is_dict_results = isinstance(results[0], dict) if results else False

            if is_dict_results:
                # For dictionary results
                for row in results:
                    if 'Airport' in str(row.get('location', '')):
                        game_state['bomb_id'] = row.get('bomb_id')
                        game_state['clues_found'].append("Stage 1 complete: Bomb identified")
                        break
            else:
                # For tuple results (fallback)
                for row in results:
                    if 'Airport' in str(row):
                        game_state['bomb_id'] = row[0] if len(row) > 0 else None
                        game_state['clues_found'].append("Stage 1 complete: Bomb identified")
                        break

        elif current_stage == 2:
            # Found the defusal code
            game_state['clues_found'].append("Stage 2 complete: Defusal mechanism found")

        elif current_stage == 3:
            # Found the culprit
            game_state['clues_found'].append("Stage 3 complete: Suspect identified")

    return stage_completed
