from fastapi import FastAPI, HTTPException,Form
import shortuuid
import redis
import  os

app = FastAPI()

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_password = os.environ.get("REDIS_PASSWORD", None)

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)



@app.post("/shorten")
def shorten_url(long_url: str = Form(...)):
    short_url = shortuuid.ShortUUID().random(6)
    redis_client.set(short_url, long_url)
    return {"short_url": f"http://localhost:8000/{short_url}"
            ,"handled_by_pod":os.environ.get("HOSTNAME")}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/{short_url}")
def redirect_url(short_url: str):
    long_url = redis_client.get(short_url)
    if long_url:
        return {"redirect_to": long_url,"handled_by_pod":os.environ.get("HOSTNAME")}
    raise HTTPException(status_code=404, detail="URL not found")



print(app.routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
