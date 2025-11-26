import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc

serviceKey = "9c1Tfa3WhfHGPEcwJWTztA5wK6suu%2BbNKuBt%2B9Vl6DVPFePl6qkL7EeZ1u1YVqsBGeRvfsf85yHjawzhah06TA%3D%3D"

def main():
    jsonResult = []
    result = []
    natName = ""

    print("=== 한국문화관광연구원 출입국관광통계서비스 데이터 수집 ===")
    nat_cd = input("국가코드를 입력하세요: ")
    nStartYear = int(input("데이터를 몇 년부터 수집할까요: "))
    nEndYear = int(input("데이터를 몇 년까지 수집할까요: "))
    ed_cd = 'E'

    jsonResult, result, natName, dataEnd = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)
    if(natName==""):
        print("해당 국가의 데이터가 없습니다.")
    else:
        jsonFile = json.dumps(jsonResult, ensure_ascii=False, indent=4, sort_keys=True)
        with open("./%s_%s_%d_%d.json" % (natName, ed_cd, nStartYear, nEndYear), 'w', encoding='utf-8') as outfile:
            outfile.write(jsonFile)

        colums = ['입국자국가', '국가코드', '입국연월', '입국자수']
        result_df = pd.DataFrame(result, columns=colums)
        result_df.to_csv("./%s_%s_%d_%d.csv" % (natName, ed_cd, nStartYear, nEndYear), index=False, encoding='cp949')

    visitCnt = []
    visitYM = []
    index = []
    i = 0
    for item in jsonResult:
        index.append(i)
        visitCnt.append(item["visit_cnt"])
        visitYM.append(item["yyyymm"])
        i += 1

    plt.rc('font', family='Malgun Gothic')
    plt.xticks(index, visitYM)
    plt.plot(index, visitCnt)
    plt.xlabel('방문월')
    plt.xticks(rotation=45)
    plt.ylabel(natName + '에서 온 방문객수')
    plt.grid(True)
    plt.show()

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("Successful request")
            return response.read().decode('utf-8')
        else:
            print("Failed request")
            return None
    except Exception as e:
        print(e)
        print("Failed request")
        return None

def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey=" + serviceKey
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + nat_cd
    parameters += "&ED_CD=" + ed_cd

    url = service_url + parameters
    print(url)
    
    responseDecode = getRequestUrl(url)
    
    if(responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)
    

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName = ""
    dataEnd = f"{nEndYear}12"
    isDataEnd = 0
    for year in range(nStartYear, nEndYear + 1):
        for month in range(1, 13):
            if(isDataEnd == 1): break
            yyyymm = f"{year}{month:02d}"
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)
            if jsonData is None:
                print(f"API 요청 실패: {yyyymm}")
                continue
            if(jsonData["response"]["header"]["resultMsg"] == "OK"):
                if jsonData["response"]["body"]["items"]== "":
                    isDataEnd = 1
                    if(month - 1 == 0):
                        year = year - 1
                        month = 13
                    dataEnd = f"{year}{month-1:02d}"
                    print("데이터 없음....")
                    jsonData = getTourismStatsItem(dataEnd, nat_cd, ed_cd)
                    break
                natName = jsonData["response"]["body"]["items"]["item"]["natKorNm"]
                natName = natName.replace(" ", "")
                num = jsonData["response"]["body"]["items"]["item"]["num"]
                ed = jsonData["response"]["body"]["items"]["item"]["ed"]
                print('[ %s_%s: %s]' %(natName, yyyymm, num))
                print('-' * 70)
                jsonResult.append({"nat_name":natName, "nat_cd":nat_cd, "yyyymm":yyyymm, "visit_cnt":num})
                result.append([nat_cd, natName, yyyymm, num])
                print("<마지막 jsonData>\n", json.dumps(jsonData, ensure_ascii=False, indent=4, sort_keys=True))
            else:
                print(f"API 오류: {jsonData['response']['header']['resultMsg']}")
                break
    return (jsonResult, result, natName, dataEnd)


if __name__ == "__main__":
    main()    