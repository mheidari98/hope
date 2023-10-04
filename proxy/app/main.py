#!/usr/bin/env python3
# Install requirements     
#   pip install fastapi uvicorn[standard] aiofiles aiohttp
import asyncio
import base64
import datetime
import logging
import random
import aiofiles
import aiohttp
import uvicorn
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, HTTPException, Query

logging.basicConfig(level=logging.INFO, format='%(levelname)s:\t  %(message)s', encoding='utf-8')

proxies = []
ss, ssr, vmess, vless, trojan = [], [], [], [], []
reality = []
proxyURL = "https://raw.githubusercontent.com/mheidari98/.proxy/main/all"

app = FastAPI(title='Free proxy')

def update(new_proxies):
    proxies.clear()
    proxies.extend(base64.b64decode(new_proxies).decode().splitlines())
    ss.clear(); ss.extend(filter(lambda s: s.startswith("ss://"), proxies))
    ssr.clear(); ssr.extend(filter(lambda s: s.startswith("ssr://"), proxies))
    vmess.clear(); vmess.extend(filter(lambda s: s.startswith("vmess://"), proxies))
    vless.clear(); vless.extend(filter(lambda s: s.startswith("vless://"), proxies))
    trojan.clear(); trojan.extend(filter(lambda s: s.startswith("trojan://"), proxies))
    reality.clear(); reality.extend(filter(lambda s: "reality" in s.lower(), proxies))


async def updateFromURL():
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(proxyURL) as response:
                if response.status == 200:
                    new_proxies = await response.text()
                    update(new_proxies)
                    logging.info(f'update proxies at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}')
                else:
                    logging.error(f"Failed to fetch proxy list. Status code: {response.status}")
        await asyncio.sleep(3600)


async def updateFromFile():
    while True:
        async with aiofiles.open("all", mode='r', encoding='UTF-8') as f:
            new_proxies = await f.read()
        update(new_proxies)
        logging.info(f'update proxies at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}')
        await asyncio.sleep(3600)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(updateFromURL())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/proxy/")
async def get_proxy(n: int = Query(default=10, description="Number of proxy to retrieve"),
                    type: str = Query(None, description="proxy type", regex="^(ss|ssr|vmess|vless|trojan|reality)$")):
    try:
        if n <= 0:
            return {"error": "Invalid value for 'n'. Please provide a positive integer."}
        match type:
            case "ss":
                selected = ss
            case "ssr":
                selected = ssr
            case "vmess":
                selected = vmess
            case "vless":
                selected = vless
            case "trojan":
                selected = trojan
            case "reality":
                selected = reality
            case _:
                selected = proxies
        random_lines = random.sample(selected, min(n, 100) )
        return PlainTextResponse(base64.b64encode('\n'.join(random_lines).encode()))
    except:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run(f"__main__:app", host='0.0.0.0', port=80, log_level="info", 
                reload=True, 
                )
