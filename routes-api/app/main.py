from decouple import config
import uvicorn

if __name__ == "__main__":
    port = config("PORT", default=8000, cast=int)
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=True)
