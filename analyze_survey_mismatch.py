import json
import re
import os

def analyze_surveying_exam(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    missing_answer = 0
    mismatch = []
    invalid_extracted = []
    no_explanation = 0

    patterns = [
        r'\[정답 확인\]\s*(\d)번',
        r'\*\*정답\s*[:\-]?\s*(\d)번?\*\*',
        r'정답\s*[:\-]?\s*(\d)번',
        r'정답은?\s*[:\-]?\s*(\d)번',
        r'정답\s*[:\-]?\s*(\d)'
    ]

    for item in data:
        answer = item.get('answer', 0)
        explanation = item.get('explanation', '')
        
        if not explanation or len(explanation.strip()) < 10:
            no_explanation += 1
            if answer == 0:
                missing_answer += 1
            continue

        if answer == 0:
            missing_answer += 1

        extracted_ans = None
        for p in patterns:
            match = re.search(p, explanation)
            if match:
                extracted_ans = int(match.group(1))
                break
        
        if extracted_ans is not None:
            if extracted_ans not in [1, 2, 3, 4]:
                invalid_extracted.append({
                    'id': item.get('id'),
                    'extracted': extracted_ans,
                    'explanation': explanation[:100]
                })
            elif answer != extracted_ans:
                mismatch.append({
                    'id': item.get('id'),
                    'current': answer,
                    'extracted': extracted_ans,
                    'explanation': explanation[:200]
                })

    print(f"--- {os.path.basename(file_path)} ---")
    print(f"Total: {total}")
    print(f"Missing (answer=0): {missing_answer}")
    print(f"Mismatch: {len(mismatch)}")
    print(f"Invalid extracted (not 1-4): {len(invalid_extracted)}")
    print(f"Poor explanation: {no_explanation}")

    if mismatch:
        print("\nMismatch Examples:")
        for ex in mismatch[:5]:
            print(f"ID: {ex['id']}, Field: {ex['current']}, Extracted: {ex['extracted']}")
            # print(f"Explanation: {ex['explanation']}...")

if __name__ == "__main__":
    analyze_surveying_exam(r"c:\AI_Class\자격증기출\engineeringExam\측량및지형공간정보기사\all_questions.json")
