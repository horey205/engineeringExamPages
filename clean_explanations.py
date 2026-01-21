import json
import re
import os

def clean_explanation(text):
    if not text:
        return text
    
    # 1. 대제목 및 문제/보기 반복 제거
    # '정답' 또는 '해설' 키워드가 처음 나타나는 지점 찾기
    markers = [
        r'### \*\*정답\*\*', 
        r'## \*\*정답\*\*', 
        r'\*\*정답\*\*:', 
        r'\*\*정답\s*[:\-]\s*\d', 
        r'\*\*해설\*\*:', 
        r'### \*\*해설\*\*',
        r'# \*\*정답\*\*',
        r'# 정답'
    ]
    
    first_marker_pos = -1
    for m in markers:
        match = re.search(m, text)
        if match:
            if first_marker_pos == -1 or match.start() < first_marker_pos:
                first_marker_pos = match.start()
    
    # 마커 이전의 텍스트가 "문제:", "보기:" 등을 포함하는 노이즈라면 잘라냄
    if first_marker_pos != -1:
        prefix = text[:first_marker_pos]
        if "문제" in prefix or "보기" in prefix or "해설" in prefix:
            text = text[first_marker_pos:]

    # 2. 고정적인 맺음말 및 챗봇 멘트 제거
    noise_endings = [
        r'이 문제를 통해.*?바랍니다\.?',
        r'추가 질문이 있으시면.*?주세요\.?',
        r'학습에 도움이 되길 바랍니다\.?',
        r'궁금한 점이 있으시면.*?주세요\.?',
        r'열공하시기 바랍니다\.?',
        r'합격을 기원합니다\.?',
        r'도움이 되셨길 바랍니다\.?',
        r'이해하기 쉽도록.*?설명합니다\.?',
        r'친절하고 전문적인 설명체로.*?주세요\.?',
        r'전문 강사 AI입니다\.?'
    ]
    
    for pattern in noise_endings:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 3. 마크다운 구조 정리 (연속된 개행 처리)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def process_cleaning(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Cleaning explanations in {os.path.basename(file_path)}...")
    count = 0
    for item in data:
        original = item.get('explanation', '')
        if original:
            cleaned = clean_explanation(original)
            if original != cleaned:
                item['explanation'] = cleaned
                count += 1

    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 웹 앱용 파일 동기화
    base_dir = os.path.dirname(file_path)
    js_path = os.path.join(base_dir, "questions.js")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(f"const questions = {json.dumps(data, ensure_ascii=False, indent=2)};")
    
    json_dest = os.path.join(base_dir, "questions.json")
    with open(json_dest, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Done! Cleaned {count} items.")

if __name__ == "__main__":
    target_file = r"c:\AI_Class\자격증기출\engineeringExam\측량및지형공간정보기사\all_questions.json"
    process_cleaning(target_file)
