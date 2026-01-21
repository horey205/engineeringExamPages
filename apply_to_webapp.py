import json
import os

def update_questions_js(base_dir):
    source_file = os.path.join(base_dir, "all_questions.json")
    dest_file = os.path.join(base_dir, "questions.js")
    
    if not os.path.exists(source_file):
        print(f"Source not found: {source_file}")
        return

    print(f"Reading {source_file}...")
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Writing to {dest_file}...")
    # 퀴즈 앱에서 사용하는 변수명에 맞춤 (보통 questions 또는 questionData)
    # 지적기사/script.js를 확인하여 변수명을 맞추는 것이 좋으나, 
    # 일반적인 기사 퀴즈 구조인 'questions' 변수명을 사용하도록 함.
    js_content = f"const questions = {json.dumps(data, ensure_ascii=False, indent=2)};"
    
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # 웹 앱용 questions.json도 동기화
    json_dest = os.path.join(base_dir, "questions.json")
    with open(json_dest, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Done! Updated {len(data)} items.")

if __name__ == "__main__":
    jijeok_dir = r"c:\AI_Class\자격증기출\engineeringExam\지적기사"
    update_questions_js(jijeok_dir)
