import urllib
import urllib.request
import urllib.parse
import os
import pandas as pd
import time
import json
import datetime
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 ID와 Secret 가져오기
client_id = os.environ.get("NAVER_CLIENT_ID")
client_secret = os.environ.get("NAVER_CLIENT_SECRET")

def getRequestUrl(url):
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)

    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            print("Successful request")
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("Failed request")
        return None

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

def getPostData(post, jsonResult, cnt):
    title = post["title"]
    description = post["description"]
    org_link = post["originallink"]
    link = post["link"]
    
    pDate = datetime.datetime.strptime(post["pubDate"], "%a, %d %b %Y %H:%M:%S +0900")
    pDate = pDate.strftime("%Y-%m-%d %H:%M:%S")

    jsonResult.append({'cnt':cnt, 'title':title, 'description':description, 'org_link':org_link, 'link':link, 'pDate':pDate})
    return

def main():
    if not client_id or not client_secret:
        print("에러: NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET를 .env 파일에 설정해주세요.")
        return
    
    print("=== Naver 뉴스 검색 ===")
    node = 'news'
    srcText = input("검색할 키워드를 입력하세요: ")
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    
    if jsonResponse is None:
        print("API 요청에 실패했습니다.")
        return
    
    total = jsonResponse['total']
    
    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)
        
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)
        
        if cnt >= total:
            break
    
    print(f"총 {cnt}개의 뉴스를 수집했습니다.")
    
    # JSON 파일 저장
    with open('./naver_news.json', 'w', encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, ensure_ascii=False)
        outfile.write(jsonFile)
    
    # CSV 파일 저장
    df = pd.DataFrame(jsonResult)
    df.to_csv('./naver_news.csv', index=False, encoding='utf-8-sig')
    
    print("naver_news.json과 naver_news.csv 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()

