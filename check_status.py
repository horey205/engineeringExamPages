
import json

def load_json_robust(filepath):
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return json.load(f)
    except Exception as e:
        print(f"FATAL: 파일을 읽을 수 없습니다. {filepath}, Error: {e}")
        return None

def main():
    filepath = "d:/Data_Backup/AI_Class/기사기출문제/지적기사/all_questions.json"
    questions = load_json_robust(filepath)
    if not questions:
        print("Failed to load json")
        return

    targets = []
    for q in questions:
        exp = q.get('explanation', '')
        # Check for weak explanations
        if "기타의 핵심 원리" in exp or len(exp) < 30 or "상세 해설" in exp:
             targets.append(q['id'])
    
    print(f"Total questions: {len(questions)}")
    print(f"Questions needing update: {len(targets)}")
    if len(targets) > 0:
        print(f"Example ID needing update: {targets[0]}")

if __name__ == "__main__":
    main()
