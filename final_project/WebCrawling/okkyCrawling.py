import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import Counter
from kiwipiepy import Kiwi
from wordcloud import WordCloud
import matplotlib.pyplot as plt

BASE = "https://okky.kr"

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

def get_titles_and_snippets(driver, page=1):
    url = f"{BASE}/community/ai?page={page}"
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    main = soup.select_one("main")
    if main is None:
        main = soup

    texts = []

    for a in main.select('a[href*="/articles/"][aria-label]'):
        t = a.get_text(" ", strip=True)
        if t and len(t) > 2:
            texts.append(t)

    return texts

def clean_kor(text):
    text = re.sub(r"[^가-힣A-Za-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

kiwi = Kiwi()
stopwords = set(["하다","되다","있다","같다","보다","이것","저것","그리고","그러나"])

def get_nouns(text):
    tokens = kiwi.tokenize(text)
    korean_nouns = [token.form for token in tokens if token.tag.startswith("NN")]
    korean_nouns = [n for n in korean_nouns if len(n) > 1 and n not in stopwords]
    

    english_words = re.findall(r'\b[A-Za-z]{2,}\b', text)

    english_stopwords = set(['the', 'is', 'are', 'was', 'were', 'of', 'to', 'and', 'in', 'on', 'at'])
    english_words = [w.upper() for w in english_words if w.lower() not in english_stopwords]
    

    return korean_nouns + english_words

print("Selenium 드라이버 시작...")
driver = get_driver()

def get_titles(driver, page=1):
    url = f"{BASE}/community/ai?page={page}"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles = []
    for a in soup.select('a[href*="/articles/"]'):
        href = a.get("href", "")
        text = a.get_text(" ", strip=True)
        if "topic=ai" in href and text and len(text) > 2:
            titles.append(text)
    return titles

try:
    all_text = ""
    total_titles = 0

    for p in range(1, 20):
        print(f"\n페이지 {p} 크롤링 중...")
        titles = get_titles(driver, page=p)
        print(f"  - {len(titles)}개 제목 발견")
        total_titles += len(titles)
        all_text += " " + " ".join(titles)

    print(f"\n총 {total_titles}개 제목 수집")
    print(f"총 수집된 텍스트 길이: {len(all_text)}자")
finally:
    driver.quit()
    print("드라이버 종료")

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

wc = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf",
    width=800,
    height=600,
    background_color="white"
)
wc.generate_from_frequencies(freq)

plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig("./final_project/WebCrawling/okkyCrawling.png", dpi=200)
plt.show()
