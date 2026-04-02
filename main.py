from fastapi import FastAPI
import requests
import os

app = FastAPI()

VWORLD_KEY = os.getenv("VWORLD_KEY")


@app.get("/")
def root():
    return {"status": "proxy running"}


# 1️⃣ 좌표 → PNU 조회
@app.get("/pnu")
def get_pnu(lat: float, lng: float):

    url = (
        f"https://api.vworld.kr/req/data?"
        f"service=data"
        f"&request=GetFeature"
        f"&data=LP_PA_CBND_BUBUN"
        f"&key={VWORLD_KEY}"
        f"&geomFilter=POINT({lng} {lat})"
        f"&geometry=true"
        f"&size=1"
    )

    res = requests.get(url)
    data = res.json()

    try:
        feature = data["response"]["result"]["featureCollection"]["features"][0]
        pnu = feature["properties"]["pnu"]
        return {"pnu": pnu}
    except:
        return {"error": "pnu not found", "raw": data}


# 2️⃣ PNU → polygon 조회
@app.get("/polygon")
def get_polygon(pnu: str):

    url = (
        f"https://api.vworld.kr/req/data?"
        f"service=data"
        f"&request=GetFeature"
        f"&data=LP_PA_CBND_BUBUN"
        f"&key={VWORLD_KEY}"
        f"&attrFilter=pnu:like:{pnu}"
        f"&geometry=true"
    )

    res = requests.get(url)
    return res.json()
