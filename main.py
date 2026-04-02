from fastapi import FastAPI
import requests
import os

app = FastAPI()

# 환경변수에서 VWorld 키 가져오기
VWORLD_KEY = os.getenv("VWORLD_KEY")


@app.get("/")
def root():
    return {"status": "proxy server running"}


@app.get("/parcel")
def get_parcel(bbox: str):
    # 1️⃣ 키 확인
    if not VWORLD_KEY:
        return {"error": "VWORLD_KEY missing"}

    # 2️⃣ bbox 확인
    if not bbox:
        return {"error": "bbox missing"}

    url = (
        f"https://api.vworld.kr/req/wfs?"
        f"key={VWORLD_KEY}"
        f"&service=WFS"
        f"&request=GetFeature"
        f"&typename=lp_pa_cbnd_bonbun"
        f"&output=application/json"
        f"&bbox={bbox}"
    )

    try:
        res = requests.get(url)

        # 3️⃣ 상태코드 확인
        if res.status_code != 200:
            return {
                "error": "vworld request failed",
                "status_code": res.status_code,
                "text": res.text[:200]
            }

        # 4️⃣ JSON 파싱
        data = res.json()

        return data

    except Exception as e:
        return {"error": str(e)}
