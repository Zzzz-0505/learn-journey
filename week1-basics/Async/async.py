import httpx
from time import perf_counter
import asyncio

OPEN_URL="https://api.open-meteo.com/v1/forecast"
TIME_OUT=10
PARAMS={
    "latitude": 40.7128,
    "longitude": -74.0060,
    "current_weather": True
}

def count_time_sync(url,params=None):
    start_time = perf_counter()
    i = 1
    try:
        while i < 6:   
            res = httpx.get(url=url,params=params,timeout=TIME_OUT)
            res.raise_for_status()
            data = res.json()
            i += 1
        end_time = perf_counter()
        return {"ok":True,"sync_content":data,"sync_time":end_time - start_time,"error":None}
    except httpx.TimeoutException:
            end_time = perf_counter()
            return {"ok":False,"sync_content":None,"sync_time":end_time - start_time,"error":"获取超时"}
    except httpx.ConnectError:
            end_time = perf_counter()
            return {"ok":False,"sync_content":None,"sync_time":end_time - start_time,"error":"连接错误"} 
    except httpx.HTTPStatusError:
        end_time = perf_counter()
        return {"ok":False,"sync_content":None,"sync_time":end_time - start_time,"error":"4xx/5xx"}
    except httpx.RequestError:
        end_time = perf_counter()
        return {"ok":False,"sync_content":None,"sync_time":end_time - start_time,"error":"httpx请求异常"}

async def count_time_async(url,params=None):
    start_time = perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url=url,params=params,timeout=TIME_OUT)
            res.raise_for_status()
            data = res.json()
        end_time = perf_counter()
        return {"ok":True,"async_content":data,"async_time":end_time - start_time,"error":None}
    except httpx.TimeoutException:
        end_time = perf_counter()
        return {"ok":False,"async_content":None,"async_time":end_time - start_time,"error":"获取超时"}
    except httpx.ConnectError:
        end_time = perf_counter()
        return {"ok":False,"async_content":None,"async_time":end_time - start_time,"error":"连接错误"}
    except httpx.HTTPStatusError:
        end_time = perf_counter()
        return {"ok":False,"async_content":None,"async_time":end_time - start_time,"error":"4xx/5xx"}
    except httpx.RequestError:
        end_time = perf_counter()
        return {"ok":False,"async_content":None,"async_time":end_time - start_time,"error":"httpx请求异常"}
         

async def main():
    sync_result = count_time_sync(OPEN_URL,PARAMS)
    
    async_start = perf_counter()
    tasks = [count_time_async(OPEN_URL, PARAMS) for _ in range(5)]
    results = await asyncio.gather(*tasks)
    async_total = perf_counter() - async_start

    print(sync_result['sync_time'])
    print(async_total)

if __name__ == "__main__":
    asyncio.run(main())

