import requests
import csv
import os
from datetime import datetime
from urllib.parse import unquote
from dotenv import load_dotenv
import pandas as pd
import folium
import webbrowser

load_dotenv()

SIDO_CODES = {
    "서울": "11",
    "부산": "26",
    "대구": "27",
    "인천": "28",
    "광주": "29",
    "대전": "30",
    "울산": "31",
    "세종": "36",
    "경기": "41",
    "강원": "42",
    "충북": "43",
    "충남": "44",
    "전북": "45",
    "전남": "46",
    "경북": "47",
    "경남": "48",
    "제주": "50"
}

SEOUL_GUGUN_CODES = {
    "680": "강남구",
    "740": "강동구",
    "305": "강북구",
    "500": "강서구",
    "620": "관악구",
    "215": "광진구",
    "530": "구로구",
    "545": "금천구",
    "350": "노원구",
    "320": "도봉구",
    "230": "동대문구",
    "590": "동작구",
    "440": "마포구",
    "410": "서대문구",
    "650": "서초구",
    "200": "성동구",
    "290": "성북구",
    "710": "송파구",
    "470": "양천구",
    "560": "영등포구",
    "170": "용산구",
    "380": "은평구",
    "110": "종로구",
    "140": "중구",
    "260": "중랑구",
}

def fetch_accident_data(auth_key, year, sido_code, gugun_code="", num_of_rows=100, page_no=1):
    url = "https://opendata.koroad.or.kr/data/rest/frequentzone/bicycle"
    
    auth_key = unquote(auth_key)
    
    params = {
        "authKey": auth_key,
        "searchYearCd": str(year),
        "siDo": sido_code,
        "type": "json",
        "numOfRows": num_of_rows,
        "pageNo": page_no
    }
    
    if gugun_code:
        params["guGun"] = gugun_code
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"HTTP 오류: {response.status_code}")
            return None
        
        data = response.json()
        result_code = data.get("resultCode", "")
        result_msg = data.get("resultMsg", "")
        
        if result_code == "00":
            return data
        elif result_code == "03":
            print(f"데이터 없음: {result_msg}")
            return None
        else:
            print(f"API 오류 - 코드: {result_code}, 메시지: {result_msg}")
            return None
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def fetch_all_accident_data(auth_key, year, sido_code, gugun_code="", num_of_rows=100):
    all_items = []
    page_no = 1
    
    print(f"\n{year}년 자전거 사고 다발지역 데이터 수집 중...")
    print(f"시도코드: {sido_code}, 시군구코드: {gugun_code if gugun_code else '전체'}")
    
    while True:
        print(f"페이지 {page_no} 조회 중...", end=" ")
        
        data = fetch_accident_data(auth_key, year, sido_code, gugun_code, num_of_rows, page_no)
        
        if not data:
            print("조회 종료")
            break
        
        items = data.get("items", {})
        
        if isinstance(items, dict):
            item_list = items.get("item", [])
        elif isinstance(items, list):
            item_list = items
        else:
            item_list = []
        
        if isinstance(item_list, dict):
            item_list = [item_list]
        
        if not item_list:
            print("더 이상 데이터 없음")
            break
        
        all_items.extend(item_list)
        print(f"{len(item_list)}건 수집 (누적: {len(all_items)}건)")
        
        total_count = data.get("totalCount", 0)
        if len(all_items) >= total_count:
            print(f"전체 데이터 수집 완료: 총 {len(all_items)}건")
            break
        
        page_no += 1
    
    return all_items

def save_to_csv(data, filename):
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    headers = [
        "다발지역FID", "다발지역ID", "법정동코드", "지점코드",
        "시도시군구명", "지점명", "사고건수", "사상자수",
        "사망자수", "중상자수", "경상자수", "부상신고자수",
        "경도", "위도"
    ]
    
    field_mapping = {
        "다발지역FID": "afos_fid",
        "다발지역ID": "afos_id",
        "법정동코드": "bjd_cd",
        "지점코드": "spot_cd",
        "시도시군구명": "sido_sgg_nm",
        "지점명": "spot_nm",
        "사고건수": "occrrnc_cnt",
        "사상자수": "caslt_cnt",
        "사망자수": "dth_dnv_cnt",
        "중상자수": "se_dnv_cnt",
        "경상자수": "sl_dnv_cnt",
        "부상신고자수": "wnd_dnv_cnt",
        "경도": "lo_crd",
        "위도": "la_crd"
    }
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for item in data:
            row = {}
            for header in headers:
                field_name = field_mapping.get(header, header)
                row[header] = item.get(field_name, "")
            writer.writerow(row)
    
    print(f"\nCSV 파일 저장 완료: {filename}")
    print(f"   총 {len(data)}건의 데이터 저장됨")

def visualize_accident_spots(csv_filename, output_html=None):
    try:
        df = pd.read_csv(csv_filename, encoding='utf-8-sig')
        
        if df.empty:
            print("데이터가 없습니다.")
            return
        
        if '위도' not in df.columns or '경도' not in df.columns:
            print("위도, 경도 정보가 없습니다.")
            return
        
        df_valid = df.dropna(subset=['위도', '경도'])
        
        if df_valid.empty:
            print("유효한 위치 데이터가 없습니다.")
            return
        
        print(f"\n지도 시각화 중... (총 {len(df_valid)}개 지점)")
        
        center_lat = df_valid['위도'].astype(float).mean()
        center_lon = df_valid['경도'].astype(float).mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles='OpenStreetMap'
        )
        
        for idx, row in df_valid.iterrows():
            try:
                lat = float(row['위도'])
                lon = float(row['경도'])
                spot_name = row.get('지점명', '정보 없음')
                accident_cnt = row.get('사고건수', 0)
                casualties = row.get('사상자수', 0)
                deaths = row.get('사망자수', 0)
                
                if accident_cnt >= 10:
                    color = 'red'
                elif accident_cnt >= 7:
                    color = 'orange'
                elif accident_cnt >= 5:
                    color = 'yellow'
                else:
                    color = 'blue'
                
                popup_html = f"""
                <div style="font-family: Arial; width: 250px;">
                    <h4 style="margin: 0 0 10px 0; color: #d32f2f;">{spot_name}</h4>
                    <hr style="margin: 5px 0;">
                    <p style="margin: 5px 0;"><b>사고건수:</b> <span style="color: red; font-weight: bold;">{accident_cnt}건</span></p>
                    <p style="margin: 5px 0;"><b>사상자수:</b> {casualties}명</p>
                    <p style="margin: 5px 0;"><b>사망자수:</b> {deaths}명</p>
                    <p style="margin: 5px 0; font-size: 0.9em; color: #666;">
                        <b>중상:</b> {row.get('중상자수', 0)}명 | 
                        <b>경상:</b> {row.get('경상자수', 0)}명
                    </p>
                </div>
                """
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{spot_name} ({accident_cnt}건)",
                    icon=folium.Icon(color=color, icon='warning-sign')
                ).add_to(m)
            
            except (ValueError, TypeError) as e:
                print(f"마커 추가 실패 (행 {idx}): {e}")
                continue
        
        if output_html is None:
            output_html = csv_filename.replace('.csv', '_map.html')
        
        m.save(output_html)
        print(f"\n지도 저장 완료: {output_html}")
        
        try:
            path = os.path.abspath(output_html)
            url = "file://" + path
            webbrowser.open(url, new=2)
        except Exception as e:
            print(f"브라우저 열기 실패: {e}")
    
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {csv_filename}")
    except Exception as e:
        print(f"시각화 중 오류 발생: {e}")

def main():
    auth_key = os.getenv("KOROAD_API_KEY")
    
    if not auth_key:
        print("API 키를 찾을 수 없습니다.")
        print("   .env 파일에 KOROAD_API_KEY를 설정해주세요.")
        return
    
    current_year = datetime.now().year
    year_input = input(f"조회할 연도를 입력하세요 (2012-2024, 기본값: {current_year - 1}): ").strip()
    year = int(year_input) if year_input else current_year - 1
    
    sido_name = "서울"
    sido_code = "11"
    
    print("\n서울시 자치구 목록:")
    sorted_guguns = sorted(SEOUL_GUGUN_CODES.items(), key=lambda x: x[1])
    for i, (code, name) in enumerate(sorted_guguns, 1):
        print(f"{i:2d}. {name} ({code})", end="   ")
        if i % 4 == 0:
            print()
    print()
    
    gugun_input = input("\n시군구 코드를 입력하세요 (예: 680, 기본값: 680-강남구): ").strip()
    gugun_code = gugun_input if gugun_input else "680"
    
    if gugun_code not in SEOUL_GUGUN_CODES:
        print(f"유효하지 않은 시군구 코드: {gugun_code}")
        print(f"강남구(680)로 진행합니다.")
        gugun_code = "680"
    
    all_data = fetch_all_accident_data(auth_key, year, sido_code, gugun_code)
    
    if not all_data:
        print("\n수집된 데이터가 없습니다.")
        return
    
    total_accidents = sum(int(item.get("occrrnc_cnt", 0)) for item in all_data)
    total_casualties = sum(int(item.get("caslt_cnt", 0)) for item in all_data)
    total_deaths = sum(int(item.get("dth_dnv_cnt", 0)) for item in all_data)
    
    print(f"다발지역 개수: {len(all_data)}개소")
    print(f"총 사고 건수: {total_accidents}건")
    print(f"총 사상자 수: {total_casualties}명")
    print(f"총 사망자 수: {total_deaths}명")
    
    print("\n사고 건수 상위 5개 지역:")
    sorted_data = sorted(all_data, key=lambda x: int(x.get("occrrnc_cnt", 0)), reverse=True)
    for i, item in enumerate(sorted_data[:5], 1):
        print(f"{i}. {item.get('spot_nm', '')} - {item.get('occrrnc_cnt', 0)}건")
    
    gugun_name = SEOUL_GUGUN_CODES.get(gugun_code, gugun_code)
    filename = f"bicycle_accident_{year}_{sido_name}_{gugun_name}.csv"
    
    save_to_csv(all_data, filename)
    visualize_accident_spots(filename)

if __name__ == "__main__":
    main()
