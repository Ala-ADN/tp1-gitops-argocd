from fastapi import FastAPI

app = FastAPI(title="GitOps Demo API", version="1.0.0")


@app.get("/")
def home():
    return {"message": "Bonjour depuis FastAPI et Argo CD", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
