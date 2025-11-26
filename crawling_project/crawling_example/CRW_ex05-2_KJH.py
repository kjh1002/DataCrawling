import os
import urllib.request
import json
import csv
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

def get_free_suggestions(start_index=1, end_index=1000, api_key=None):
    if not api_key:
        api_key = os.getenv("SEOUL_API_KEY")
    
    service_name = "ChunmanFreeSuggestions"
    file_type = "json"
    url = f"http://openAPI.seoul.go.kr:8088/{api_key}/{file_type}/{service_name}/{start_index}/{end_index}"
    
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        
        if response.getcode() == 200:
            response_body = response.read()
            data = json.loads(response_body.decode('utf-8'))
            
            if service_name in data:
                result = data[service_name]
                
                if 'RESULT' in result:
                    code = result['RESULT']['CODE']
                    message = result['RESULT']['MESSAGE']
                    
                    if code == 'INFO-000':
                        if 'row' in result:
                            return result['row']
                        else:
                            print("데이터가 없습니다.")
                            return []
                    else:
                        print(f"오류 발생 [{code}]: {message}")
                        return []
            else:
                print("예상하지 못한 응답 형식입니다.")
                return []
        else:
            print(f"HTTP 오류 코드: {response.getcode()}")
            return []
            
    except urllib.error.HTTPError as e:
        print(f"HTTP 오류 발생: {e.code} - {e.reason}")
        return []
    except urllib.error.URLError as e:
        print(f"URL 오류 발생: {e.reason}")
        return []
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

def save_to_csv(data, filename):
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = [
            '제안번호', '제안제목', '제안내용', '득표', 
            '제안등록일자', '정책분류', '시민의견수', 
            '공감수', '비공감수', '답변여부'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for item in data:
            writer.writerow({
                '제안번호': item.get('SN', ''),
                '제안제목': item.get('TITLE', ''),
                '제안내용': item.get('CONTENT', ''),
                '득표': item.get('VOTE_SCORE', ''),
                '제안등록일자': item.get('REG_DATE', ''),
                '정책분류': item.get('VISIOIN_TXT', ''),
                '시민의견수': item.get('USER_COMMENT_CNT', ''),
                '공감수': item.get('VOTE_CNT', ''),
                '비공감수': item.get('VOTE_DIS_CNT', ''),
                '답변여부': item.get('REPLY_YN', '')
            })
    
    print(f"\n총 {len(data)}개의 자유제안을 '{filename}' 파일로 저장했습니다.")

def get_all_suggestions(api_key=None, max_records=None):
    all_data = []
    start_index = 1
    page_size = 1000
    
    if not api_key:
        api_key = os.getenv("SEOUL_API_KEY")
    
    print("\n전체 데이터를 가져오는 중...")
    
    while True:
        end_index = start_index + page_size - 1
        
        if max_records and end_index > max_records:
            end_index = max_records
        
        print(f"\n{start_index}번부터 {end_index}번까지 조회 중...")
        data = get_free_suggestions(start_index, end_index, api_key)
        
        if not data:
            break
        
        all_data.extend(data)
        
        if max_records and len(all_data) >= max_records:
            break
        
        if len(data) < page_size:
            break
        
        start_index = end_index + 1
    
    print(f"\n총 {len(all_data)}개의 데이터를 가져왔습니다.")
    return all_data

def main():    
    api_key = os.getenv("SEOUL_API_KEY")
    
    data = get_free_suggestions(1, 1000, api_key)
    
    if data:
        filename = "seoul_free_suggestions.csv"
        save_to_csv(data, filename)
        
    else:
        print("\n데이터를 가져오는데 실패했습니다.")

if __name__ == "__main__":
    main()

