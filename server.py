import asyncio
import websockets
import json
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

# Dữ liệu người dùng giả lập
user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "user_type": "PATIENT",
    "fullname": "John Doe",
    "date_of_birth": "1990-01-01",
    "gender": "MALE",
    "address": "123 Main St",
    "phone": "123456789",
    "profile_image": "https://example.com/image.jpg"
}

# Hàm xử lý kết nối WebSocket
async def handle_client(websocket, path):  # Đảm bảo hàm này có `path`
    global user_data
    logging.info("New client connected!")
    try:
        async for message in websocket:
            logging.info(f"Received message: {message}")
            if message == "get_user_info":
                response = {
                    "code": 200,
                    "message": "User retrieved successfully",
                    "user_data": user_data
                }
                await websocket.send(json.dumps(response))
                logging.info("Sent user info to client.")
            elif message.startswith("{"):
                try:
                    data = json.loads(message)
                    if data.get("action") == "update_user_info":
                        user_data.update(data["user_data"])
                        response = {
                            "code": 200,
                            "message": "User info updated successfully",
                            "user_data": user_data
                        }
                        await websocket.send(json.dumps(response))
                        logging.info("User info updated and response sent.")
                except json.JSONDecodeError:
                    logging.error("Invalid JSON format received.")
                    await websocket.send(json.dumps({
                        "code": 400,
                        "message": "Invalid JSON format."
                    }))
    except websockets.ConnectionClosed as e:
        logging.warning(f"Connection closed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Khởi chạy WebSocket server
async def main():
    async with websockets.serve(handle_client, "localhost", 8765):  # Đảm bảo gọi hàm đúng
        logging.info("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())