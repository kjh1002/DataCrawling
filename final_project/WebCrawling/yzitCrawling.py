from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import re
from collections import Counter
from kiwipiepy import Kiwi
from wordcloud import WordCloud
import matplotlib.pyplot as plt

BASE = "https://yozm.wishket.com"

def clean_kor(text):
    # 한글/영문/숫자 + 공백만 허용
    text = re.sub(r"[^가-힣A-Za-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Kiwi 형태소 분석기 초기화
kiwi = Kiwi()
stopwords = set([
    "하다", "되다", "있다", "같다", "보다", "이것", "저것", "그리고", "그러나",
    "개발자", "시간", "코드", "분전", "일전", "요즘", "올해", "인기", "댓글", "이번"
])

def get_nouns(text):
    # 1) 한국어 명사 추출 (Kiwi)
    tokens = kiwi.tokenize(text)
    korean_nouns = [token.form for token in tokens if token.tag.startswith("NN")]
    korean_nouns = [n for n in korean_nouns if len(n) > 1 and n not in stopwords]

    # 2) 영어 단어 추출 (2글자 이상)
    english_words = re.findall(r'\b[A-Za-z]{2,}\b', text)
    english_stopwords = set([
        'the', 'is', 'are', 'was', 'were', 'of', 'to', 'and', 'in', 'on', 'at',
        'show', 'gn', 'for', 'with', 'that', 'this', 'from', 'by'
    ])
    english_words = [w.upper() for w in english_words if w.lower() not in english_stopwords]

    # 3) 합치기
    return korean_nouns + english_words

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

def get_yozm_articles(driver, category, page=1):
    # 카테고리별 리스트 페이지
    url = f"{BASE}/magazine/list/{category}/?page={page}"
    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = []
    seen = set()  # 중복 방지

    # 각 글의 상세 페이지 링크: /magazine/detail/숫자/ 형식
    for a in soup.select('a[href*="/magazine/detail/"]'):
        href = a.get('href', '')
        if not href:
            continue
        
        # 전체 URL 생성
        full_url = BASE + href if href.startswith('/') else href
        
        # 중복 체크
        if full_url in seen:
            continue
        
        text = a.get_text(" ", strip=True)
        # 카드 안의 제목은 보통 꽤 길기 때문에, 너무 짧은 텍스트는 제외
        if text and len(text) > 10:
            articles.append({
                'category': category,
                'title': text,
                'url': full_url
            })
            seen.add(full_url)

    return articles

if __name__ == "__main__":
    driver = get_driver()
    
    # 크롤링할 카테고리 목록
    categories = ['develop', 'ai', 'itservice', 'plan', 'design', 'business']
    
    try:
        all_articles = []
        max_pages = 10
        
        for category in categories:
            for p in range(1, max_pages + 1):
                articles = get_yozm_articles(driver, category, page=p)
                
                if not articles:
                    break
                
                all_articles.extend(articles)
                time.sleep(1)

        df = pd.DataFrame(all_articles)
        
        import os
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, f"yozm_articles_{timestamp}.csv")
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        all_text = " ".join(df['title'].astype(str).tolist())
        cleaned = clean_kor(all_text)
        tokens = get_nouns(cleaned)
        freq = Counter(tokens)
        
        if freq:
            wc = WordCloud(
                font_path="C:/Windows/Fonts/malgun.ttf",
                width=1200,
                height=800,
                background_color="white",
                colormap="viridis",
                relative_scaling=0.3,
                min_font_size=10
            )
            wc.generate_from_frequencies(freq)
            
            plt.figure(figsize=(12, 8))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title("YOZM IT Magazine - Word Cloud", fontsize=20, pad=20)
            plt.tight_layout()
            
            wordcloud_file = os.path.join(script_dir, "yzitCrawling.png")
            plt.savefig(wordcloud_file, dpi=200, bbox_inches='tight')
            plt.show()
        
    finally:
        driver.quit()
