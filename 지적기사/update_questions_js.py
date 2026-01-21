
import json
import os

SOURCE_FILE = "d:/Data_Backup/AI_Class/기사기출문제/지적기사/all_questions.json"
DEST_FILE = "d:/Data_Backup/AI_Class/기사기출문제/지적기사/questions.js"

def update_js():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    print(f"Reading {SOURCE_FILE}...")
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    print(f"Writing {len(data)} questions to {DEST_FILE}...")
    
    # Check if 'explanation' field exists and count
    exp_count = sum(1 for q in data if q.get('explanation'))
    print(f"Questions with explanation: {exp_count}")

    js_content = f"const questions = {json.dumps(data, ensure_ascii=False, indent=2)};"
    
    try:
        with open(DEST_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Success!")
    except Exception as e:
        print(f"Error writing JS: {e}")

if __name__ == "__main__":
    update_js()
