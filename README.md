# 🏫 서경대학교 2025-2 Data Crawling
## 📂 Report / Project Repository

---

### 📑 소개
이 레포지토리는 **2025년 2학기 데이터크롤링 수업**에서 작성한  
과제(Report), 실습 코드, 그리고 **기말 프로젝트**를 정리한 저장소입니다.

**기말 프로젝트**에서는 IT 트렌드, 채용 시장, AI 기업 주가, 직무별 AI 도구 등  
4가지 주제로 데이터를 수집하고 심층 분석했습니다.

---

## 📁 프로젝트 구조

```
📦 data_crawling
├── 📂 8장_data/           # 8장 실습 데이터 (엑셀, 워드클라우드 등)
├── 📂 11장_data/          # 11장 실습 데이터 (UCI HAR Dataset 등)
├── 📂 12장_data/          # 12장 실습 데이터 (Online Retail 등)
├── 📂 14장_data/          # 14장 실습 데이터 (GOOG.csv, CNN 이미지 등)
│
├── 📂 crawling_project/   # 수업 과제 및 실습 프로젝트
│   ├── 📂 crawling_example/  # 크롤링 예제 코드
│   │   ├── CGJchicken.py
│   │   ├── datagokr.py
│   │   ├── kakaoMapAPI.py
│   │   ├── navernews.py
│   │   └── CRW_ex05-*.py
│   ├── 📂 model/          # 학습된 모델 파일
│   ├── 📓 8장_영어단어분석.ipynb
│   ├── 📓 8장_한글단어분석.ipynb
│   ├── 📓 10장_미세먼지회귀분석.ipynb
│   ├── 📓 10장_자동차연비분석.ipynb
│   ├── 📓 11장_(1)로지스틱회귀분석.ipynb
│   ├── 📓 11장_결정트리분석.ipynb
│   ├── 📓 12장_군집분석.ipynb
│   ├── 📓 14장_(1)LSTM주가분석.ipynb
│   ├── 📓 14장_(2)Prophet-주가예측분석.ipynb
│   ├── 📓 14장_(3)CNN숫자이미지분류.ipynb
│   ├── 📓 14장_(4)CNN품종분류.ipynb
│   ├── main.py
│   ├── requirements.txt
│   └── pyproject.toml
│
└── 📂 final_project/      # 기말 프로젝트
    │
    ├── 📂 WebCrawling/    # IT 트렌드 & 교육 플랫폼 분석
    │   ├── analysis.ipynb
    │   ├── bootcampCrawling.py      # 부트캠프 정보 크롤링
    │   ├── inflearnCrawling.py      # 인프런 강의 크롤링
    │   ├── okkyCrawling.py          # OKKY 커뮤니티 크롤링
    │   ├── yzitCrawling.py          # 긱뉴스 크롤링
    │   └── 📂 분석결과/
    │       ├── AI_뉴스_리스트.csv
    │       ├── AI_부트캠프_리스트.csv
    │       ├── 플랫폼별_요약.csv
    │       └── *.png (시각화 결과)
    │
    ├── 📂 사람인 분석/     # 채용 시장 분석
    │   ├── saramin.ipynb
    │   ├── 📂 K-means 군집화 분석/
    │   │   ├── clustering_results.csv
    │   │   ├── cluster_summary.csv
    │   │   └── *.png (군집 시각화)
    │   ├── 📂 기술 스택 연관 규칙 분석/
    │   │   ├── tech_association_rules.csv
    │   │   ├── tech_stack_frequency.csv
    │   │   └── *.png (네트워크, 히트맵)
    │   └── 📂 텍스트 마이닝&키워드 분석/
    │       ├── tfidf_keywords_top20.csv
    │       ├── keyword_frequency_top30.csv
    │       └── wordcloud.png
    │
    ├── 📂 주가 분석/       # AI 기업 주가 분석
    │   ├── stock.ipynb
    │   ├── 📂 수집 결과/
    │   │   ├── NVIDIA_NVDA.csv
    │   │   ├── Microsoft_MSFT.csv
    │   │   ├── Google_GOOGL.csv
    │   │   ├── Meta_META.csv
    │   │   ├── Amazon_AMZN.csv
    │   │   ├── Tesla_TSLA.csv
    │   │   ├── AMD_AMD.csv
    │   │   └── Intel_INTC.csv
    │   ├── 📂 LSTM 분석/
    │   │   ├── LSTM_분석_결과_요약.csv
    │   │   └── *_LSTM_분석.png (종목별 예측 결과)
    │   └── 📂 단기간 성장률 분석/
    │       ├── AI주_기간별_성장률_분석.csv
    │       └── *.png (성장률 시각화)
    │
    └── 📂 직무 ai툴/       # 직무별 AI 도구 분석
        ├── ai_tool.ipynb
        ├── ANOVA.ipynb
        ├── 📂 수집 데이터 분류/
        │   └── ai_tool_analysis_ultra_final_20251213_225505.csv
        ├── 📂 직무별 ai/
        │   ├── job_tool_analysis_20251213_225506.csv
        │   └── job_tool_crosstab_*.csv
        ├── 📂 인사이트 도출/
        │   ├── job_ratings_20251213_225507.csv
        │   ├── tool_ratings_20251213_225507.csv
        │   └── variance_analysis_20251213_225507.csv
        └── 📂 시각화/
            ├── ai_tool_core_analysis_20251213_225509.png
            └── ANOVA.jpg
```

---

## 🔧 환경 설정

### 필요 라이브러리 설치

```bash
cd crawling_project
pip install -r requirements.txt
```

또는 `uv` 사용 시:

```bash
uv sync
```

---

## 📊 분석 내용

### 📚 수업 실습 (crawling_project)

#### 8장 - 텍스트 분석
- **영어단어분석**: 영어 텍스트 데이터 분석 및 워드클라우드
- **한글단어분석**: 한글 텍스트 데이터 분석 및 키워드 추출

#### 10장 - 회귀 분석
- **미세먼지 회귀분석**: 미세먼지 데이터를 활용한 회귀 분석
- **자동차 연비분석**: 자동차 데이터셋을 이용한 연비 예측

#### 11장 - 분류 분석
- **로지스틱 회귀분석**: 이진 분류를 위한 로지스틱 회귀 모델
- **결정 트리 분석**: UCI HAR Dataset을 활용한 결정 트리 모델

#### 12장 - 군집 분석
- **군집분석**: Online Retail 데이터를 활용한 고객 세그먼트 분석

#### 14장 - 딥러닝 분석
- **LSTM 주가분석**: LSTM 모델을 활용한 구글 주가 예측
- **Prophet 주가예측**: Facebook Prophet을 이용한 시계열 예측
- **CNN 숫자이미지분류**: CNN 모델을 활용한 숫자 이미지 분류
- **CNN 품종분류**: CNN 모델을 활용한 이미지 품종 분류

---

### 🎯 기말 프로젝트 (final_project)

#### 1. 📰 IT 트렌드 & 교육 플랫폼 분석 (WebCrawling)
**목적**: IT 교육 시장과 최신 기술 트렌드 파악

**수집 대상**:
- **부트캠프**: 국내 주요 부트캠프 정보 (강의명, 기관, 카테고리 등)
- **인프런**: 온라인 강의 정보 및 키워드 분석
- **OKKY**: 개발자 커뮤니티 인기 게시글 및 토론 주제
- **긱뉴스(Yozm)**: IT 업계 최신 뉴스 및 기술 트렌드

**분석 결과**:
- 플랫폼별 AI 관련 콘텐츠 비교 분석
- 부트캠프 카테고리 분포 및 인기 기관 분석
- 인프런 강의 키워드 워드클라우드
- AI 관련 뉴스 및 부트캠프 리스트 추출

---

#### 2. 👔 채용 시장 분석 (사람인 분석)
**목적**: IT 채용 시장의 요구 기술 스택 및 직무 트렌드 파악

**분석 방법**:
1. **K-means 군집화 분석**
   - 채용 공고를 유사도 기반으로 군집화
   - Elbow Method를 통한 최적 군집 수 결정
   - 군집별 특성 및 키워드 비교

2. **기술 스택 연관 규칙 분석**
   - 함께 요구되는 기술 스택 조합 발견
   - 기술 간 상관관계 히트맵
   - 기술 스택 네트워크 시각화

3. **텍스트 마이닝 & 키워드 분석**
   - TF-IDF 기반 핵심 키워드 추출
   - 빈도 분석 및 워드클라우드
   - 직무별 요구사항 요약

---

#### 3. 📈 AI 기업 주가 분석 (주가 분석)
**목적**: 주요 AI 기업들의 주가 동향 및 예측 모델 구축

**분석 대상 기업** (8개):
- NVIDIA, Microsoft, Google, Meta
- Amazon, Tesla, AMD, Intel

**분석 방법**:
1. **LSTM 딥러닝 모델**
   - 과거 주가 데이터로 학습
   - 향후 주가 예측 및 시각화
   - 모델 성능 평가 (MSE, MAE 등)

2. **단기간 성장률 분석**
   - 1개월, 3개월, 6개월, 1년 성장률 비교
   - 기간별 성장률 히트맵 및 추세선 분석
   - 종목 간 성장률 종합 비교

**주요 인사이트**:
- Google 62.94% 성장 (최고)
- NVIDIA 30.37% 성장
- Microsoft, Meta는 완만한 성장
- Amazon은 소폭 하락

---

#### 4. 🤖 직무별 AI 도구 분석 (직무 ai툴)
**목적**: 각 직무에서 사용되는 AI 도구의 활용도 및 만족도 분석

**분석 방법**:
1. **직무별 AI 도구 사용 현황**
   - 교차 분석(Crosstab)을 통한 직무-도구 매핑
   - 직무별 선호 도구 파악

2. **ANOVA 분산 분석**
   - 직무별 AI 도구 평가 점수 차이 검정
   - 통계적 유의성 확인

3. **인사이트 도출**
   - 고평가 도구 vs 저평가 도구
   - 직무별 만족도 분포
   - 도구별 평균 평점 및 분산 분석

**결과물**:
- 직무-도구 매핑 테이블
- 평가 점수 피봇 테이블
- ANOVA 결과 시각화

---

## 🕷️ 크롤링 예제

`crawling_example/` 폴더에는 다양한 크롤링 실습 코드가 포함되어 있습니다:

- **CGJchicken.py**: CGJ 치킨 매장 정보 크롤링
- **datagokr.py**: 공공데이터포털 API 활용
- **kakaoMapAPI.py**: 카카오맵 API 연동
- **navernews.py**: 네이버 뉴스 크롤링
- **CRW_ex05-*.py**: 크롤링 실습 예제

---

## 🚀 실행 방법

### 📚 수업 실습 프로젝트

#### Jupyter Notebook 실행

```bash
cd crawling_project
jupyter notebook
```

#### Python 스크립트 실행

```bash
cd crawling_project
python main.py
```

---

### 🎯 기말 프로젝트 실행

#### 1. WebCrawling - 크롤링 실행

```bash
cd final_project/WebCrawling
python bootcampCrawling.py    # 부트캠프 정보 크롤링
python inflearnCrawling.py     # 인프런 강의 크롤링
python okkyCrawling.py         # OKKY 커뮤니티 크롤링
python yzitCrawling.py         # 긱뉴스 크롤링
```

#### 2. 분석 노트북 실행

```bash
cd final_project/WebCrawling
jupyter notebook analysis.ipynb

cd ../사람인 분석
jupyter notebook saramin.ipynb

cd ../주가 분석
jupyter notebook stock.ipynb

cd ../직무 ai툴
jupyter notebook ai_tool.ipynb
jupyter notebook ANOVA.ipynb
```

---

## 📝 License

이 프로젝트는 교육 목적으로 작성되었습니다.

---

**📅 Last Updated**: 2025년 12월 17일  
**👨‍🎓 Course**: 데이터 크롤링 (2025-2학기)  
**🏛️ University**: 서경대학교

---

## 📌 주요 특징

### 🔍 다양한 데이터 소스
- 웹 크롤링 (BeautifulSoup, Selenium)
- API 활용 (카카오맵, 공공데이터포털, yfinance)
- 실시간 데이터 수집

### 📊 포괄적인 분석 기법
- 회귀/분류/군집 분석
- 딥러닝 (LSTM, CNN)
- 텍스트 마이닝 & 워드클라우드
- 시계열 예측 (Prophet)
- 연관 규칙 분석
- ANOVA 분산 분석

### 📈 실용적인 주제
- IT 교육 시장 트렌드
- 채용 시장 기술 스택 분석
- AI 기업 주가 예측
- 직무별 AI 도구 활용도