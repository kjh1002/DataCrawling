from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time


def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.page_load_strategy = "normal"
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)
    return driver


def extract_title_and_org_from_first_cell(cell_text: str):
    lines = [line.strip() for line in cell_text.split('\n') if line.strip()]

    if len(lines) < 2:
        return None, None

    start_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('D-') or line == 'EVENT' or any(ord(c) > 127 for c in line[:2]):
            start_idx = i + 1
        else:
            break

    if start_idx >= len(lines) - 1:
        return None, None

    org_name = lines[start_idx] if start_idx < len(lines) else None
    title = lines[start_idx + 1] if start_idx + 1 < len(lines) else None

    return title, org_name


def extract_category_from_row(row):
    try:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            first_td = cells[0].text.strip()
            category = first_td.split('\n')[0].strip()
            if category in ["데이터분석", "데이터사이언스", "AI/ML", "AI서비스"]:
                return category
    except Exception:
        pass
    return None


def extract_keywords_from_row(row):
    """
    선발절차·키워드 컬럼에서 기술 키워드만 추출.
    "선발 절차" 관련 텍스트는 제외.
    """
    try:
        cells = row.find_elements(By.TAG_NAME, "td")
        
        if len(cells) > 6:
            keyword_cell = cells[6]
            keywords = []
            
            full_text = keyword_cell.text.strip()
            if full_text:
                lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                
                for line in lines:
                    skip_keywords = ["선발", "절차", "코딩", "없음", "있음"]
                    if any(skip in line for skip in skip_keywords):
                        continue
                    
                    if len(line) >= 2:
                        keywords.append(line)
            
            return keywords
            
    except Exception:
        pass
    
    return []


def extract_row_data(row):
    """단일 행에서 데이터 추출 (키워드 포함)"""
    try:
        first_cell = row.find_element(By.TAG_NAME, "th")
        first_cell_text = first_cell.text.strip()
        
        title, org_name = extract_title_and_org_from_first_cell(first_cell_text)
        if not title:
            return None
        
        category = extract_category_from_row(row)
        keywords = extract_keywords_from_row(row)
        
        return {
            "organization": org_name if org_name else "",
            "title": title,
            "category": category if category else "",
            "keywords": ", ".join(keywords) if keywords else "",
        }
    except Exception:
        return None


def scroll_and_collect_data(driver, source_label, max_scrolls=300):
    """
    가상 스크롤 페이지에서 조금씩 스크롤하면서 데이터 수집.
    """
    try:
        bootcamp_list = driver.find_element(By.ID, "default-bootcamp-list")
        
        scrollable = None
        inner_divs = bootcamp_list.find_elements(By.CSS_SELECTOR, "div")
        for div in inner_divs:
            overflow_y = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).overflowY;", div
            )
            if overflow_y in ['auto', 'scroll']:
                scrollable = div
                break
        
        if not scrollable:
            scrollable = bootcamp_list
        
        collected_data = {}
        consecutive_no_new = 0
        max_no_new = 30
        scroll_step = 500
        
        for i in range(max_scrolls):
            rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-index]")
            
            new_count = 0
            for row in rows:
                try:
                    data_index = row.get_attribute("data-index")
                    
                    if data_index in collected_data:
                        continue
                    
                    row_data = extract_row_data(row)
                    if row_data:
                        row_data["source"] = source_label
                        collected_data[data_index] = row_data
                        new_count += 1
                        
                except Exception:
                    continue
            
                if new_count > 0:
                consecutive_no_new = 0
            else:
                consecutive_no_new += 1
                if consecutive_no_new >= max_no_new:
                    break
            
            current_scroll = driver.execute_script("return arguments[0].scrollTop;", scrollable)
            driver.execute_script(
                f"arguments[0].scrollTop = {current_scroll + scroll_step};", scrollable
            )
            time.sleep(1.2)
        
        return list(collected_data.values())
        
    except Exception as e:
        print(f"  에러 발생: {e}")
        return []


def crawl_boottent_single_page(
    driver,
    url: str,
    source_label: str = "current",
):
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "default-bootcamp-list")
            )
        )
        time.sleep(3)
        
        results = scroll_and_collect_data(driver, source_label)
        return results

    except Exception:
        return []


def crawl_boottent_data_category(
    output_csv: str = "./final_project/WebCrawling/bootcampCrawling.csv",
    headless: bool = True,
):
    BASE_URL = "https://boottent.com/camps?categories=data"

    driver = init_driver(headless=headless)
    all_results = []

    try:
        all_results.extend(
            crawl_boottent_single_page(
                driver,
                url=BASE_URL,
                source_label="data_category",
            )
        )

    finally:
        driver.quit()

    if all_results:
        df = pd.DataFrame(all_results)
        df_unique = df.drop_duplicates(subset=["title"], keep="first")
        df_unique.to_csv(output_csv, index=False, encoding="utf-8-sig")

    return all_results


if __name__ == "__main__":
    crawl_boottent_data_category(headless=True)
