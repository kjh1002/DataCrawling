import os
import requests
import pandas as pd
import folium
import webbrowser
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("KAKAO_API_KEY")

def search_places(keyword, page=1, size=15):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {API_KEY}"
    }
    params = {
        "query": keyword,
        "page": page,
        "size": size
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def docs_to_df(documents):
    rows = []
    for d in documents:
        rows.append({
            "id": d.get("id"),
            "place_name": d.get("place_name"),
            "category_name": d.get("category_name"),
            "phone": d.get("phone"),
            "address": d.get("address_name"),
            "road_address": d.get("road_address_name"),
            "x": float(d.get("x")) if d.get("x") else None,
            "y": float(d.get("y")) if d.get("y") else None,
            "place_url": d.get("place_url"),
        })
    return pd.DataFrame(rows)


keyword = input("검색할 키워드를 입력하세요: ")

dfs = []
page = 1

while True:
    response = search_places(keyword, page=page, size=10)
    df = docs_to_df(response.get("documents"))
    dfs.append(df)

    if response["meta"]["is_end"]:
        break
    
    page += 1

result = pd.concat(dfs, ignore_index=True)
print(result.shape)
result.head()

result.to_csv(f"{keyword}_places.csv", index=False, encoding="utf-8-sig")

df = pd.read_csv(f"{keyword}_places.csv")
center = [37.61498, 127.0134]
m = folium.Map(location=center, zoom_start=16)

for _, row in df.dropna(subset=["x", "y"]).iterrows():
    folium.Marker(
        [row["y"], row["x"]],
        popup=f"{row['place_name']}<br>{row['category_name']}",
        tooltip=row["place_name"]
    ).add_to(m)

fnmae = f"{keyword}_places_map.html"
m.save(fnmae)
print(f"Saved Map: {keyword}_places_map.html")


path = os.path.abspath(fnmae)
url = "file://" + path
webbrowser.open(url, new=2)