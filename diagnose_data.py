import json
import re
import os

def analyze_exam_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    missing_answer = 0
    mismatch = 0
    no_explanation = 0
    examples = []

    # 정답 추출 패턴들
    patterns = [
        r'정답은?\s*[:\-]?\s*(\d)번',
        r'정답\s*[:\-]?\s*(\d)',
        r'\[정답 확인\]\s*(\d)번',
        r'\*\*정답\s*[:\-]?\s*(\d)번?\*\*',
        r'정답\s*[:\-]?\s*(\d)번'
    ]

    for item in data:
        answer = item.get('answer', 0)
        explanation = item.get('explanation', '')
        
        if not explanation or len(explanation.strip()) < 5:
            no_explanation += 1
            if answer == 0:
                missing_answer += 1
            continue

        if answer == 0:
            missing_answer += 1

        # 해설에서 정답 추출 시도
        extracted_ans = None
        for p in patterns:
            match = re.search(p, explanation)
            if match:
                extracted_ans = int(match.group(1))
                break
        
        if extracted_ans is not None:
            if answer != extracted_ans:
                mismatch += 1
                if len(examples) < 5:
                    examples.append({
                        'id': item.get('id'),
                        'current_answer': answer,
                        'extracted_from_explanation': extracted_ans,
                        'explanation_snippet': explanation[:100] + "..."
                    })
        elif answer == 0:
            # answer도 0이고 해설에서도 못 찾은 경우
            pass

    print(f"\n--- {os.path.basename(file_path)} 분석 결과 ---")
    print(f"전체 문제 수: {total}")
    print(f"정답 누락 (answer=0): {missing_answer}")
    print(f"정답 불일치 (해설 vs 필드): {mismatch}")
    print(f"해설 없음/부족: {no_explanation}")
    
    if examples:
        print("\n불일치 사례 (최대 5개):")
        for ex in examples:
            print(f"- ID: {ex['id']}, 필드값: {ex['current_answer']}, 해설추출: {ex['extracted_from_explanation']}")
            print(f"  해설 미리보기: {ex['explanation_snippet']}")

if __name__ == "__main__":
    base_path = r"c:\AI_Class\자격증기출\engineeringExam"
    analyze_exam_data(os.path.join(base_path, "지적기사", "all_questions.json"))
    analyze_exam_data(os.path.join(base_path, "측량및지형공간정보기사", "all_questions.json"))
