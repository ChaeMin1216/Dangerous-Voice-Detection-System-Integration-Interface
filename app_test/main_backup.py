# app/main.pyhttp://221.156.38.124/http://221.156.38.124/http://221.156.3
from fastapi import FastAPI, WebSocket, File, UploadFile
from fastapi.responses import HTMLResponse
from websocket_manager import websocket_manager
from audio_handler_backup import process_audio_file
import os
import asyncio
from pathlib import Path
import uvicorn
import shutil

app = FastAPI()
Audio_Id = 0
# 설정할 파일 저장 경로
UPLOAD_DIRECTORY = "/home/jaehoon/바탕화면/audio_predict/raw_data"
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    return {"filename": file.filename, "path": file_path}



@app.get("/test2.html")
async def get():
    # 정적 파일로부터 HTML 반환
    file_path = "test2.html"
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# WebSocket 연결을 관리하고 데이터를 지속적으로 전송
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
        websocket_manager.disconnect(websocket)

# 파일 모니터링 및 처리
async def monitor_and_process(directory: str, Audio_Id: str):
    processed_files = set()  # 처리된 파일을 추적하기 위한 집합
    audiofile_path = Path('../audio_storage')

    if not audiofile_path.exists():
        audiofile_path.mkdir(parents=True, exist_ok=True)

    while True:
        for file_path in Path(directory).iterdir():
            if file_path.is_file() and file_path.name not in processed_files:
                print(f"Detected new file: {file_path.name}")  # 파일 감지 로그

                try:
                    await process_audio_file(str(file_path), Audio_Id, websocket_manager)
                    processed_files.add(file_path.name)  # 파일 처리 후 집합에 추가

                    shutil.move(str(file_path), audiofile_path/file_path.name)
                    print(f"Moved file {file_path.name.split('/')[-1]} to {audiofile_path}")
                
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

        await asyncio.sleep(1)  # 1초 간격으로 디렉토리 체크
# 백그라운드 작업으로 파일 모니터링 시작
@app.on_event("startup")
async def startup_event():
    global audio_counter
    raw_audio_directory = "../raw_data/"
    # 디렉토리가 존재하지 않으면 생성
    os.makedirs(raw_audio_directory, exist_ok=True)

    # 파일 모니터링 작업을 비동기로 시작
    asyncio.create_task(monitor_and_process(raw_audio_directory, Audio_Id))


if __name__ == "__main__":
    uvicorn.run("main_backup:app", host="0.0.0.0", port=15411, reload=True)
