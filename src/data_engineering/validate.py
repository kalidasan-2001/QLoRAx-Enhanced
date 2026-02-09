
import json
import sys

def validate_line(line_data, line_num):
    """
    Validates a single line of data against schema and heuristics.
    Heuristics: Input > 10 chars, Output > 20 chars.
    """
    try:
        if 'messages' not in line_data:
            return False, f"Line {line_num}: Missing 'messages' key"
        
        messages = line_data['messages']
        if not isinstance(messages, list) or len(messages) < 2:
            return False, f"Line {line_num}: Invalid messages format"

        user_msg = next((m for m in messages if m['role'] == 'user'), None)
        assist_msg = next((m for m in messages if m['role'] == 'assistant'), None)

        if not user_msg or not assist_msg:
            return False, f"Line {line_num}: Missing user or assistant message"

        # Heuristic Length Checks (from Paper)
        if len(user_msg['content']) <= 10:
             return False, f"Line {line_num}: User input too short (<=10 chars)"
        
        if len(assist_msg['content']) <= 20:
             return False, f"Line {line_num}: Assistant output too short (<=20 chars)"

        return True, None

    except Exception as e:
        return False, f"Line {line_num}: Validation error - {str(e)}"

def validate_file(filepath):
    print(f"Validating {filepath}...")
    passed = 0
    failed = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if not line.strip(): # Skip empty lines
                continue
                
            try:
                data = json.loads(line)
                is_valid, error = validate_line(data, i)
                if is_valid:
                    passed += 1
                else:
                    failed += 1
                    print(error)
            except json.JSONDecodeError:
                failed += 1
                print(f"Line {i}: Invalid JSON")

    print(f"\nValidation Complete.\nPassed: {passed}\nFailed: {failed}")
    return failed == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path_to_jsonl>")
        sys.exit(1)
    
    success = validate_file(sys.argv[1])
    if not success:
        sys.exit(1)

