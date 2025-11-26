import requests
import csv
import os
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

SIDO_CODES = {
    "서울특별시": "11",
    "부산광역시": "21",
    "대구광역시": "22",
    "인천광역시": "23",
    "광주광역시": "24",
    "대전광역시": "25",
    "울산광역시": "26",
    "경기도": "31",
    "강원도": "32",
    "충청북도": "33",
    "충청남도": "34",
    "전라북도": "35",
    "전라남도": "36",
    "경상북도": "37",
    "경상남도": "38",
    "제주특별자치도": "39"
}

def fetch_ev_stations(api_key, metro_cd):
    url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
    params = {
        "apiKey": api_key,
        "metroCd": metro_cd,
        "returnType": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"HTTP 오류: {response.status_code}")
            return None
        
        data = response.json()
        
        if isinstance(data, dict) and 'data' in data:
            return data['data']
        elif isinstance(data, list):
            return data
        else:
            return None
            
    except Exception as e:
        print(f"오류: {e}")
        return None

def fetch_all_stations(api_key):
    all_data = []
    
    print("\n전국 전기차 충전소 데이터 수집 중...")
    print("-" * 80)
    
    for sido_name, sido_code in SIDO_CODES.items():
        print(f"{sido_name} (코드: {sido_code}) 조회 중...", end=" ")
        
        data = fetch_ev_stations(api_key, sido_code)
        
        if data:
            count = len(data)
            all_data.extend(data)
            print(f"{count}개소 수집 (누적: {len(all_data)}개소)")
        else:
            print(f"⚠️ 실패")
    
    print("-" * 80)
    return all_data

def aggregate_by_sido(data):
    sido_stats = defaultdict(lambda: {
        '충전소수': 0,
        '급속충전기': 0,
        '완속충전기': 0,
        '전체충전기': 0
    })
    
    for item in data:
        metro = item.get('metro', '알 수 없음')
        rapid_cnt = int(item.get('rapidCnt', 0))
        slow_cnt = int(item.get('slowCnt', 0))
        
        sido_stats[metro]['충전소수'] += 1
        sido_stats[metro]['급속충전기'] += rapid_cnt
        sido_stats[metro]['완속충전기'] += slow_cnt
        sido_stats[metro]['전체충전기'] += rapid_cnt + slow_cnt
    
    return dict(sido_stats)

def print_statistics(sido_stats):
    print("\n" + "="*80)
    print("지역별(시도) 전기차 충전소 통계")
    print("="*80)
    print(f"{'시도명':<20} {'충전소수':>10} {'급속충전기':>12} {'완속충전기':>12} {'전체충전기':>12}")
    print("-"*80)
    
    sorted_sidos = sorted(sido_stats.items(), key=lambda x: x[0])
    
    total_stations = 0
    total_rapid = 0
    total_slow = 0
    total_all = 0
    
    for sido, stats in sorted_sidos:
        print(f"{sido:<20} {stats['충전소수']:>10,}개 {stats['급속충전기']:>12,}대 "
              f"{stats['완속충전기']:>12,}대 {stats['전체충전기']:>12,}대")
        total_stations += stats['충전소수']
        total_rapid += stats['급속충전기']
        total_slow += stats['완속충전기']
        total_all += stats['전체충전기']
    
    print("-"*80)
    print(f"{'합계':<20} {total_stations:>10,}개 {total_rapid:>12,}대 "
          f"{total_slow:>12,}대 {total_all:>12,}대")
    print("="*80)
    
    print("\n충전소 설치 상위 5개 시도:")
    top5 = sorted(sido_stats.items(), key=lambda x: x[1]['충전소수'], reverse=True)[:5]
    for i, (sido, stats) in enumerate(top5, 1):
        print(f"  {i}. {sido}: {stats['충전소수']:,}개소 "
              f"(급속 {stats['급속충전기']:,}대, 완속 {stats['완속충전기']:,}대)")

def save_summary_csv(sido_stats, filename):
    if not sido_stats:
        print("저장할 데이터가 없습니다.")
        return
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['시도명', '충전소수', '급속충전기', '완속충전기', '전체충전기']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        sorted_sidos = sorted(sido_stats.items(), key=lambda x: x[0])
        
        for sido, stats in sorted_sidos:
            writer.writerow({
                '시도명': sido,
                '충전소수': stats['충전소수'],
                '급속충전기': stats['급속충전기'],
                '완속충전기': stats['완속충전기'],
                '전체충전기': stats['전체충전기']
            })
        
        total_stations = sum(s['충전소수'] for s in sido_stats.values())
        total_rapid = sum(s['급속충전기'] for s in sido_stats.values())
        total_slow = sum(s['완속충전기'] for s in sido_stats.values())
        total_all = sum(s['전체충전기'] for s in sido_stats.values())
        
        writer.writerow({
            '시도명': '합계',
            '충전소수': total_stations,
            '급속충전기': total_rapid,
            '완속충전기': total_slow,
            '전체충전기': total_all
        })
    
    print(f"\nCSV 파일 저장 완료: {filename}")
    print(f"   총 {len(sido_stats)}개 시도의 데이터 저장됨")

def save_detail_csv(data, filename):
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['시도명', '시군구명', '건물명', '주소', '급속충전기', '완속충전기', '지원차종']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for item in data:
            writer.writerow({
                '시도명': item.get('metro', ''),
                '시군구명': item.get('city', ''),
                '건물명': item.get('stnPlace', ''),
                '주소': item.get('stnAddr', ''),
                '급속충전기': item.get('rapidCnt', 0),
                '완속충전기': item.get('slowCnt', 0),
                '지원차종': item.get('carType', '')
            })
    
    print(f"상세 데이터 CSV 파일 저장 완료: {filename}")
    print(f"   총 {len(data)}개의 충전소 데이터 저장됨")

def main():
    api_key = os.getenv("KEPCO_API_KEY")
    
    if not api_key:
        print("API 키를 찾을 수 없습니다.")
        print("   .env 파일에 KEPCO_API_KEY를 설정해주세요.")
        api_key = input("\nAPI 키를 직접 입력하세요 (40자리): ").strip()
        if not api_key:
            print("API 키가 입력되지 않았습니다. 프로그램을 종료합니다.")
            return
    
    print("\n" + "="*80)
    print("전기차 충전소 데이터 크롤링 시작")
    print("="*80)
    
    all_data = fetch_all_stations(api_key)
    
    if not all_data:
        print("\n수집된 데이터가 없습니다.")
        return
    
    print(f"\n총 {len(all_data)}개의 충전소 데이터를 수집했습니다.")

    sido_stats = aggregate_by_sido(all_data)
    
    print_statistics(sido_stats)
    
    summary_filename = "ev_charging_stations_by_sido.csv"
    detail_filename = "ev_charging_stations_detail.csv"
    
    save_summary_csv(sido_stats, summary_filename)
    save_detail_csv(all_data, detail_filename)
    
    print("\n모든 작업이 완료되었습니다!")
    print(f"   - 시도별 집계: {summary_filename}")
    print(f"   - 상세 데이터: {detail_filename}")

if __name__ == "__main__":
    main()
