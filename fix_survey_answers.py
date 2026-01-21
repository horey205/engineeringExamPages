import json
import re
import os

def fix_survey_mismatch(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    patterns = [
        r'\[정답 확인\]\s*(\d)번',
        r'\*\*정답\s*[:\-]?\s*(\d)번?\*\*',
        r'정답\s*[:\-]?\s*(\d)번',
        r'정답은?\s*[:\-]?\s*(\d)번',
        r'정답\s*[:\-]?\s*(\d)'
    ]

    fixed_count = 0
    skipped_invalid = 0
    
    for item in data:
        original_answer = item.get('answer', 0)
        explanation = item.get('explanation', '')
        
        if not explanation:
            continue

        # 해설에서 정답 추출
        extracted_ans = None
        for p in patterns:
            match = re.search(p, explanation)
            if match:
                extracted_ans = int(match.group(1))
                break
        
        if extracted_ans is not None:
            # 추출된 정답이 유효한 범위(1~4)인 경우에만 수정
            if extracted_ans in [1, 2, 3, 4]:
                if original_answer != extracted_ans:
                    item['answer'] = extracted_ans
                    fixed_count += 1
            else:
                skipped_invalid += 1

    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 웹 앱용 questions.js 및 questions.json 동기화
    base_dir = os.path.dirname(file_path)
    
    js_path = os.path.join(base_dir, "questions.js")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(f"const questions = {json.dumps(data, ensure_ascii=False, indent=2)};")
        
    web_json_path = os.path.join(base_dir, "questions.json")
    with open(web_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n--- {os.path.basename(file_path)} 수정 및 동기화 완료 ---")
    print(f"해설 기준으로 수정된 정답 수: {fixed_count}")
    print(f"유효하지 않은 추출값(1-4 이외)으로 인해 스킵된 수: {skipped_invalid}")

if __name__ == "__main__":
    target_file = r"c:\AI_Class\자격증기출\engineeringExam\측량및지형공간정보기사\all_questions.json"
    fix_survey_mismatch(target_file)
