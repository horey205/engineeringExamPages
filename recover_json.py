
import json
import os

file_path = "d:/Data_Backup/AI_Class/기사기출문제/지적기사/all_questions.json"

print(f"Recovering {file_path}...")

with open(file_path, 'rb') as f:
    data = f.read()

# Try to decode
try:
    text = data.decode('utf-8')
    print("File decodes successfully as UTF-8.")
except UnicodeDecodeError as e:
    print(f"Unicode decode error: {e}")
    # Decode ignoring errors to inspect structure
    text = data.decode('utf-8', errors='ignore')

stripped_text = text.strip()

if stripped_text.endswith(']'):
    print("JSON seems structurally closed.")
    # Try to parse
    try:
        json.loads(stripped_text)
        print("JSON is valid.")
    except json.JSONDecodeError as e:
        print(f"JSON validation failed: {e}")
else:
    print("JSON is NOT closed. Attempting to fix...")
    # It probably got cut off. Find the last closing brace for an object '}'
    last_object_end = stripped_text.rfind('}')
    if last_object_end != -1:
        # Keep everything up to the last object
        fixed_text = stripped_text[:last_object_end+1] + "\n]"
        
        try:
            parsed = json.loads(fixed_text)
            print(f"Recovered! Total items: {len(parsed)}")
            
            # Use 'cp949' or 'utf-8' depending on what is safer, but standard is utf-8
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
            print("Fixed file saved.")
        except json.JSONDecodeError as e:
            print(f"Recovery failed: {e}")
    else:
        print("Could not find any JSON objects to recover.")
