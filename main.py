from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
from pathlib import Path

app = FastAPI()

@app.get("/")
def index():
    path = Path(__file__).parent / "index.html" 
    html_content = path.read_text(encoding = "utf-8")
    return HTMLResponse(content = html_content, status_code = 200)

@app.get("/호출예약")
def data():
    return "hello"

@app.websocket("/ws/vehicle/{vehicle_id}")
async def vehicle_socket(websocket: WebSocket, vehicle_id: str):
    # 연결 수락
    await websocket.accept()
    print(f"차량 {vehicle_id} 연결됨")

    try:
        # 연결 유지 중 계속 메시지 주고받기
        while True:
            msg = await websocket.receive_text()  # 클라이언트 -> 서버
            print(f"[{vehicle_id}] 수신: {msg}")
            await websocket.send_text(f"서버 응답: {msg}")  # 서버 -> 클라이언트

    except WebSocketDisconnect:
        # 연결 끊김 감지
        print(f"차량 {vehicle_id} 연결 종료")


