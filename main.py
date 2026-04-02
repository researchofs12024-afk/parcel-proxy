from fastapi import FastAPI
import requests
import os

app = FastAPI()

VWORLD_KEY = os.getenv("VWORLD_KEY")


@app.get("/")
def root():
    return {"status": "proxy running"}


@app.get("/pnu")
def get_pnu(lat: float, lng: float):

    if not VWORLD_KEY:
        return {"error": "VWORLD_KEY missing"}

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

    try:
        res = requests.get(url)

        return {
            "status_code": res.status_code,
            "text": res.text[:500]   # 🔥 핵심 (응답 그대로 보기)
        }

    except Exception as e:
        return {"error": str(e)}
