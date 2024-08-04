import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_xray_config_json():
    with open("compose-data/xray/config/config.json", "r") as f:
        config = f.read()
        return json.loads(config)
