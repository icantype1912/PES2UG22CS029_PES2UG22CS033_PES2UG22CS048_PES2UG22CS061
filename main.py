from fastapi import FastAPI, HTTPException
import shortuuid
import redis

app = FastAPI()
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.post("/shorten")
def shorten_url(long_url: str):
    short_url = shortuuid.ShortUUID().random(6)
    redis_client.set(short_url, long_url)
    return {"short_url": f"http://localhost:8000/{short_url}"}

@app.get("/{short_url}")
def redirect_url(short_url: str):
    long_url = redis_client.get(short_url)
    if long_url:
        return {"redirect_to": long_url}
    raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
