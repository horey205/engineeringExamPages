import json
import re
import os

def fix_jijeok_answers(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 정답 추출 패턴들 (우선순위 순서대로)
    patterns = [
        r'\[정답 확인\]\s*(\d)번',
        r'\*\*정답\s*[:\-]?\s*(\d)번?\*\*',
        r'정답\s*[:\-]?\s*(\d)번',
        r'정답은?\s*[:\-]?\s*(\d)번',
        r'정답\s*[:\-]?\s*(\d)'
    ]

    fixed_count = 0
    missing_filled_count = 0
    
    for item in data:
        original_answer = item.get('answer', 0)
        explanation = item.get('explanation', '')
        
        if not explanation:
            continue

        # 해설에서 정답 추출 시도
        extracted_ans = None
        for p in patterns:
            match = re.search(p, explanation)
            if match:
                extracted_ans = int(match.group(1))
                break
        
        if extracted_ans is not None:
            # 1. 정답이 0인 경우 채워넣기
            if original_answer == 0:
                item['answer'] = extracted_ans
                missing_filled_count += 1
            # 2. 정답이 해설과 다른 경우 해설 기준으로 수정
            elif original_answer != extracted_ans:
                item['answer'] = extracted_ans
                fixed_count += 1

    # 파일 저장 (덮어쓰기 전 백업 권장되나 여기서는 직접 수정)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n--- {os.path.basename(file_path)} 수정 완료 ---")
    print(f"해설 기준으로 수정된 정답 수: {fixed_count}")
    print(f"누락된 정답(0)을 해설에서 찾아낸 수: {missing_filled_count}")
    print(f"총 변경된 항목 수: {fixed_count + missing_filled_count}")

if __name__ == "__main__":
    target_file = r"c:\AI_Class\자격증기출\engineeringExam\지적기사\all_questions.json"
    fix_jijeok_answers(target_file)
