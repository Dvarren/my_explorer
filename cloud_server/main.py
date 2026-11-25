import os
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

BASE = Path(__file__).resolve().parent
STORAGE = BASE / "storage"
STORAGE.mkdir(exist_ok=True)
TOKEN_FILE = BASE / "token.txt"


def get_token() -> str:
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    token = os.urandom(24).hex()
    TOKEN_FILE.write_text(token)
    return token


TOKEN = get_token()
app = FastAPI(title="MyExplorer Cloud")


def check(auth: str) -> None:
    if auth != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def safe(path: str) -> Path:
    p = (STORAGE / path.lstrip("/")).resolve()
    if not str(p).startswith(str(STORAGE.resolve())):
        raise HTTPException(status_code=400, detail="Bad path")
    return p


class NewFolder(BaseModel):
    path: str


@app.get("/api/status")
def status():
    return {"ok": True, "name": "MyExplorer Cloud"}


@app.get("/api/list")
def list_dir(path: str = Query(""), x_auth_token: str = Header("")):
    check(x_auth_token)
    p = safe(path)
    if not p.is_dir():
        raise HTTPException(404, "Not a directory")
    items = []
    for child in sorted(p.iterdir(), key=lambda c: (not c.is_dir(), c.name.lower())):
        items.append({
            "name": child.name,
            "is_dir": child.is_dir(),
            "size": 0 if child.is_dir() else child.stat().st_size,
        })
    return {"items": items, "path": path}


@app.get("/api/download")
def download(path: str, x_auth_token: str = Header("")):
    check(x_auth_token)
    p = safe(path)
    if not p.is_file():
        raise HTTPException(404, "Not a file")
    return FileResponse(str(p), filename=p.name)


@app.post("/api/upload")
def upload(path: str = Query(""), file: UploadFile = File(...), x_auth_token: str = Header("")):
    check(x_auth_token)
    target_dir = safe(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = safe(str(Path(path) / file.filename))
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"ok": True, "name": file.filename}


@app.post("/api/mkdir")
def mkdir(body: NewFolder, x_auth_token: str = Header("")):
    check(x_auth_token)
    safe(body.path).mkdir(parents=True, exist_ok=True)
    return {"ok": True}


@app.delete("/api/delete")
def delete(path: str, x_auth_token: str = Header("")):
    check(x_auth_token)
    p = safe(path)
    if p.is_dir():
        shutil.rmtree(p)
    elif p.is_file():
        p.unlink()
    else:
        raise HTTPException(404, "Not found")
    return {"ok": True}


if __name__ == "__main__":
    print(f"Токен доступа: {TOKEN}")
    print("Сохраните его — он понадобится в приложении")
    uvicorn.run(app, host="0.0.0.0", port=8765)