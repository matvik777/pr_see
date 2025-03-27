import cv2
import json
from client_config import SERVER_HOST, SERVER_PORT, IMAGE_PATH
from network_client import send_image_to_server

if __name__ == "__main__":
    print("[CLIENT_MAIN] Starting client...")
    
    response = send_image_to_server(SERVER_HOST,SERVER_PORT, IMAGE_PATH)
    response = response.decode("utf-8", errors="replace")
    print("[CLIENT_MAIN] Server returned:", response)  
    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        print("Failed to parse server response as JSON")
        result = {}
       
    frame = cv2.imread("../images/best_frame2.png")
    objects_list = result.get("objects", [])
    for obj in objects_list:
        if obj.get("type") == "square":
            x = obj["x"]
            y = obj["y"]
            w = obj["w"]
            h = obj["h"]
            # Рисуем красный прямоугольник (BGR: (0,0,255))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
    cv2.imshow("ddf", frame)
    cv2.waitKey(0)