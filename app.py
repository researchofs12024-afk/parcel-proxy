from fastapi import FastAPI
import requests
import os

app = FastAPI()

VWORLD_KEY = os.getenv("VWORLD_KEY")

@app.get("/parcel")
def get_parcel(bbox: str):
    url = f"https://api.vworld.kr/req/wfs?key={VWORLD_KEY}&service=WFS&request=GetFeature&typename=lp_pa_cbnd_bonbun&output=application/json&bbox={bbox}"
    
    res = requests.get(url)
    return res.json()
