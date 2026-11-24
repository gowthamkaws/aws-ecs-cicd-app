from fastapi import FastAPI
import os
import socket

app = FastAPI(title="Cloud Portfolio API")

@app.get("/")
def home():
    return {
        "status": "running",
        "service": "aws-ecs-fargate-demo",
        "container_host": socket.gethostname(),
        "version": os.getenv("APP_VERSION", "v1.0")
    }

@app.get("/health")
def health_check():
    return {"healthy": True}
