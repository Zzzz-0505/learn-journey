from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
async def get_headers(request: Request):
    # FastAPI 的 request.headers 是一个类似字典的对象
    # 直接转换为普通字典返回，FastAPI 会自动将其序列化为 JSON
    return dict(request.headers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)