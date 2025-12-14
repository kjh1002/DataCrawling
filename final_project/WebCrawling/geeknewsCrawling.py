import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import Counter
from kiwipiepy import Kiwi
from wordcloud import WordCloud
import matplotlib.pyplot as plt

BASE = "https://news.hada.io"  # GeekNews 기본 도메인[web:19]

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_titles(driver, page=1):
    """
    GeekNews 특정 페이지에서 뉴스 제목 리스트를 가져오는 함수.
    예: https://news.hada.io/?page=2 형태.[web:19]
    """
    url = f"{BASE}/?page={page}"
    driver.get(url)
    time.sleep(1)  # 로딩 약간 기다리기 (필요시 조정)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles = []

    # 각 뉴스 상세 페이지 링크: /topic?id=xxxx 형태[web:27]
    for a in soup.select('a[href*="topic?id="]'):
        text = a.get_text(" ", strip=True)
        # 짧은 숫자(순번) 같은 것 제외, 어느 정도 길이 있는 텍스트만 사용
        if text and len(text) > 3:
            titles.append(text)

    return titles

def clean_kor(text):
    # 한글/영문/숫자 + 공백만 허용
    text = re.sub(r"[^가-힣A-Za-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

kiwi = Kiwi()
stopwords = set(["하다","되다","있다","같다","보다","이것","저것","그리고","그러나", "댓글"])

def get_nouns(text):
    # 1) 한국어 명사 추출 (Kiwi)
    tokens = kiwi.tokenize(text)
    korean_nouns = [token.form for token in tokens if token.tag.startswith("NN")]
    korean_nouns = [n for n in korean_nouns if len(n) > 1 and n not in stopwords]

    # 2) 영어 단어 추출 (2글자 이상)
    english_words = re.findall(r'\b[A-Za-z]{2,}\b', text)
    english_stopwords = set(['the', 'is', 'are', 'was', 'were', 'of', 'to', 'and', 'in', 'on', 'at', 'show', 'gn'])
    english_words = [w.upper() for w in english_words if w.lower() not in english_stopwords]

    # 3) 합치기
    return korean_nouns + english_words

print("Selenium 드라이버 시작...")
driver = get_driver()

try:
    all_text = ""
    total_titles = 0

    for p in range(1, 100):
        print(f"\n페이지 {p} 크롤링 중...")
        titles = get_titles(driver, page=p)
        print(f"  - {len(titles)}개 제목 발견")
        if not titles:
            break
        total_titles += len(titles)
        all_text += " " + " ".join(titles)

    print(f"\n총 {total_titles}개 제목 수집")
    print(f"총 수집된 텍스트 길이: {len(all_text)}자")
finally:
    driver.quit()
    print("드라이버 종료")

# 전처리 + 명사 추출
cleaned = clean_kor(all_text)
print(f"전처리 후 텍스트 길이: {len(cleaned)}자")
tokens = get_nouns(cleaned)
print(f"추출된 명사 개수: {len(tokens)}개")

freq = Counter(tokens)
print(f"고유 단어 수: {len(freq)}개")
if freq:
    print(f"상위 10개 단어: {freq.most_common(10)}")

if not freq:
    print("\n단어를 추출할 수 없습니다. 셀렉터 또는 페이지 구조를 다시 확인해주세요.")
    raise SystemExit

# 워드클라우드 생성
wc = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf",  # 환경에 맞게 경로 조정
    width=800,
    height=600,
    background_color="white"
)
wc.generate_from_frequencies(freq)

plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig("./final_project/WebCrawling/geeknewsCrawling.png", dpi=200)
plt.show()
