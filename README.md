# 🏫 서경대학교 2025-2 Data Crawling
## 📂 Report / Project Repository

---

### 📑 소개
이 레포지토리는 **2025년 2학기 데이터크롤링 수업**에서 작성한  
과제(Report) 및 프로젝트 코드를 정리한 저장소입니다.

---

## 📁 프로젝트 구조

```
📦 data_crawling
├── 📂 11장_data/          # 11장 실습 데이터 (UCI HAR Dataset 등)
├── 📂 12장_data/          # 12장 실습 데이터 (Online Retail 등)
├── 📂 13장_data/          # 13장 실습 데이터
├── 📂 14장_data/          # 14장 실습 데이터 (GOOG.csv 등)
└── 📂 crawling_project/
    ├── 📂 crawling_example/  # 크롤링 예제 코드
    │   ├── CGJchicken.py
    │   ├── datagokr.py
    │   ├── kakaoMapAPI.py
    │   ├── navernews.py
    │   └── CRW_ex05-*.py
    ├── 📓 10장_미세먼지회귀분석.ipynb
    ├── 📓 10장_자동차연비분석.ipynb
    ├── 📓 11장_(1)로지스틱회귀분석.ipynb
    ├── 📓 11장_결정트리분석.ipynb
    ├── 📓 12장_군집분석.ipynb
    ├── 📓 14장_(1)LSTM주가분석.ipynb
    ├── 📓 14장_(2)Prophet-주가예측분석.ipynb
    ├── 📓 14장_(3)CNN숫자이미지분류.ipynb
    ├── 📓 14장_(4)CNN품종분류.ipynb
    ├── main.py
    ├── requirements.txt
    └── pyproject.toml
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

### 10장 - 회귀 분석
- **미세먼지 회귀분석**: 미세먼지 데이터를 활용한 회귀 분석
- **자동차 연비분석**: 자동차 데이터셋을 이용한 연비 예측

### 11장 - 분류 분석
- **로지스틱 회귀분석**: 이진 분류를 위한 로지스틱 회귀 모델
- **결정 트리 분석**: UCI HAR Dataset을 활용한 결정 트리 모델

### 12장 - 군집 분석
- **군집분석**: Online Retail 데이터를 활용한 고객 세그먼트 분석

### 14장 - 딥러닝 분석
- **LSTM 주가분석**: LSTM 모델을 활용한 구글 주가 예측
- **Prophet 주가예측**: Facebook Prophet을 이용한 시계열 예측
- **CNN 숫자이미지분류**: CNN 모델을 활용한 숫자 이미지 분류
- **CNN 품종분류**: CNN 모델을 활용한 이미지 품종 분류

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

### Jupyter Notebook 실행

```bash
cd crawling_project
jupyter notebook
```

### Python 스크립트 실행

```bash
cd crawling_project
python main.py
```

---

## 📝 License

이 프로젝트는 교육 목적으로 작성되었습니다.

---

**📅 Last Updated**: 2025년 2학기  
**👨‍🎓 Course**: 데이터 크롤링  
**🏛️ University**: 서경대학교