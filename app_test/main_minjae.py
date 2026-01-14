from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.responses import HTMLResponse
from websocket_manager import websocket_manager
from audio_handler import process_audio_file, extract_identifier_from_filename, update_cctv_counter
import os
import asyncio
from pathlib import Path
import uvicorn
import shutil
import json

app = FastAPI()
raw_audio_directory = "../raw_data/"
cctv_mapping_file = "../cctv_mapping.json"  # .json 확장자로 변경

# 설정할 파일 저장 경로
UPLOAD_DIRECTORY = "/home/jaehoon/바탕화면/audio_predict/raw_data"
AUDIO_STORAGE_PATH = "../audio_storage"

# CCTV 식별자 카운트를 저장할 전역 딕셔너리
cctv_counter = {}

def create_empty_cctv_mapping_file():
    if not os.path.exists(cctv_mapping_file) or os.path.getsize(cctv_mapping_file) == 0:
        with open(cctv_mapping_file, 'w') as file:
            json.dump({}, file)  # 빈 JSON 객체로 초기화

def load_cctv_mapping():
    global cctv_counter
    if os.path.exists(cctv_mapping_file):
        with open(cctv_mapping_file, 'r') as file:
            cctv_counter = json.load(file)  # JSON 파일 로드
    else:
        cctv_counter = {}  # 매핑 파일이 없는 경우 빈 딕셔너리

def save_cctv_mapping():
    with open(cctv_mapping_file, 'w') as file:
        json.dump(cctv_counter, file)

def update_cctv_counter(identifier: str):
    global cctv_counter
    if identifier in cctv_counter:
        cctv_counter[identifier] += 1
    else:
        cctv_counter[identifier] = 0  # 새 식별자가 발견되면 카운트를 0으로 설정

    save_cctv_mapping()  # JSON 파일에 즉시 저장

async def monitor_and_process(directory: str, websocket_manager):
    processed_files = set()  # 처리된 파일을 추적하기 위한 집합
    audiofile_path = Path(AUDIO_STORAGE_PATH)

    if not audiofile_path.exists():
        audiofile_path.mkdir(parents=True, exist_ok=True)

    while True:
        for file_path in Path(directory).iterdir():
            if file_path.is_file() and file_path.name not in processed_files:
                print(f"Detected new file: {file_path.name}")

                try:
                    # 파일 이름에서 식별자 추출
                    identifier = extract_identifier_from_filename(file_path.name)
                    if identifier:
                        # 파일 처리 및 카운트 업데이트
                        await process_audio_file(str(file_path), websocket_manager)
                        processed_files.add(file_path.name)  # 파일 처리 후 집합에 추가

                        shutil.move(str(file_path), audiofile_path / file_path.name)
                        print(f"Moved file {file_path.name} to {audiofile_path}")

                        # 식별자를 사용하여 카운트를 업데이트
                        update_cctv_counter(identifier)
                    else:
                        print(f"Skipping file {file_path.name} due to invalid identifier format")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

        await asyncio.sleep(1)  # 1초 간격으로 디렉토리 체크

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename, "path": file_path}

@app.get("/test.html")
async def get():
    # 정적 파일로부터 HTML 반환
    file_path = "test.html"
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            # WebSocket 연결 유지
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket_manager.disconnect(websocket)

@app.on_event("startup")
async def startup_event():
    create_empty_cctv_mapping_file()  # CCTV 매핑 파일 초기화
    load_cctv_mapping()  # CCTV 식별자 매핑 로드
    # 디렉토리 모니터링 및 처리 시작
    asyncio.create_task(monitor_and_process(raw_audio_directory, websocket_manager))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=15410)

