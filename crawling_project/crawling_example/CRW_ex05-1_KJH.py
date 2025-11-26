import os
import urllib.request
import json
import csv
from dotenv import load_dotenv

load_dotenv()

def search_naver_blog(query, display=100):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정")
        return None
    
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display}"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            print(f"Error Code: {rescode}")
            return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def save_to_csv(data, filename):
    if not data or 'items' not in data:
        print("저장할 데이터가 없습니다.")
        return
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['제목', '링크', '설명', '블로거명', '블로그명', '작성일']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for item in data['items']:
            writer.writerow({
                '제목': remove_html_tags(item['title']),
                '링크': item['link'],
                '설명': remove_html_tags(item['description']),
                '블로거명': item['bloggername'],
                '블로그명': item['bloggerlink'],
                '작성일': item['postdate']
            })
    
    print(f"총 {len(data['items'])}개의 검색 결과를 '{filename}' 파일로 저장했습니다.")

def main():
    search_query = "월드컵"
    
    result = search_naver_blog(search_query, display=100)
    
    if result:
        print(f"검색 완료! (총 {result['total']}개 중 {len(result['items'])}개 가져옴)")
        
        filename = f"worldcup_blog_results.csv"
        save_to_csv(result, filename)

    else:
        print("검색 결과를 가져오는데 실패했습니다.")


if __name__ == "__main__":
    main()