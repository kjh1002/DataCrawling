from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time


CATEGORIES = {
    'artificial-intelligence': {'name': 'AI 기술', 'max_pages': 9},
    'Applied-ai': {'name': 'AI 활용', 'max_pages': 7}
}


def init_driver(headless=True):
    """Chrome WebDriver 초기화"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless=new')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    chrome_options.page_load_strategy = 'normal'
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    return driver


def scroll_to_bottom(driver, pause=0.8, max_scroll=20):
    """페이지 끝까지 스크롤"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def crawl_category_with_selenium(driver, category_slug: str, category_name: str, max_pages: int):
    print(f"\n[{category_name}] 카테고리 크롤링 시작")

    course_data = []
    wait = WebDriverWait(driver, 15)

    for page in range(1, max_pages + 1):
        if page == 1:
            url = f"https://www.inflearn.com/courses/{category_slug}"
        else:
            url = f"https://www.inflearn.com/courses/{category_slug}?page_number={page}"

        print(f"  {page}페이지 크롤링 중: {url}")

        try:
            driver.get(url)

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'main')))
            except Exception:
                time.sleep(0.1)
            
            scroll_to_bottom(driver, pause=0.5, max_scroll=15)

            cards = []
            selectors = [
                'a[href*="/course/"]',
                'div.course_card_item a',
                'div[class*="course"] a',
                'article a[href*="/course/"]'
            ]
            
            for selector in selectors:
                try:
                    cards = driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        break
                except Exception:
                    continue
            
            if not cards:
                break

            page_titles = set()

            for card in cards:
                try:
                    text = card.text.strip()
                    if not text:
                        continue

                    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
                    if not lines:
                        continue

                    title = lines[0]

                    if len(title) < 5:
                        continue
                    if not any(c.isalpha() for c in title):
                        continue

                    page_titles.add(title)

                except Exception:
                    continue

            if not page_titles:
                break

            print(f"  {page}페이지에서 {len(page_titles)}개 강좌 제목 수집")

            for title in page_titles:
                course_data.append({
                    'category': category_name,
                    'category_slug': category_slug,
                    'title': title
                })

        except Exception as e:
            print(f"  {page}페이지 크롤링 중 에러 발생: {e}")
            if "chrome" in str(e).lower() or "driver" in str(e).lower():
                break
            continue

    print(f"[{category_name}] 총 {len(course_data)}개 강좌 수집 완료")
    return course_data


def crawl_inflearn_ai_courses(output_csv: str = "./final_project/WebCrawling/inflearnCrawling.csv", headless: bool = True):
    """인프런 AI 강좌 크롤링"""
    print('=' * 60)
    print('INFLEARN AI COURSES CRAWLING START (Selenium 동적 크롤링)')
    print('=' * 60)

    driver = None
    all_courses = []

    try:
        driver = init_driver(headless=headless)
        
        for category_slug, info in CATEGORIES.items():
            courses = crawl_category_with_selenium(
                driver,
                category_slug,
                info['name'],
                info['max_pages']
            )
            all_courses.extend(courses)
    except Exception as e:
        print(f"\n크롤링 중 에러 발생: {e}")
    finally:
        if driver:
            try:
                driver.quit()
                print("\n브라우저를 종료했습니다.")
            except Exception:
                pass

    if all_courses:
        df = pd.DataFrame(all_courses)
        df_unique = df.drop_duplicates(subset=['title'])
        df_unique = df_unique.sort_values(['category', 'title']).reset_index(drop=True)
        df_unique.to_csv(output_csv, index=False, encoding="utf-8-sig")

        print('\n' + '=' * 60)
        print(f"총 {len(all_courses)}개(중복 포함) / {len(df_unique)}개(중복 제거) 강좌를 '{output_csv}'에 저장했습니다.")
        print(f"\n카테고리별 강좌 수:")
        for info in CATEGORIES.values():
            category_name = info['name']
            count = len(df_unique[df_unique['category'] == category_name])
            print(f"  - {category_name}: {count}개")
        print('=' * 60)
    else:
        print("수집된 강좌가 없습니다.")

    print('FINISHED')


if __name__ == "__main__":
    crawl_inflearn_ai_courses(headless=True)
