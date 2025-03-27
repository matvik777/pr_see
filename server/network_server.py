import socket
import struct
import cv2
import numpy as np
from process import find_squares
import json
def start_server(host: str, port: int):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = s.accept()
        print(f"[SERVER] Connected by {addr}")
        
        try:
            lenght = conn.recv(4)
            if len(lenght)< 4:
                print("[SERVER] No length received; client disconnected early?")  
                conn.close()
                continue
            file_size = struct.unpack("!I", lenght)[0]
            print(f"[SERVER] Expecting {file_size} bytes of image data")
            
            all_data = b""
            bytes_received = 0
            while bytes_received < file_size:
                chunk = conn.recv(min(4096, file_size-bytes_received))
                if not chunk:
                    break
                all_data += chunk
                bytes_received += len(chunk)
                
            img_array = np.frombuffer(all_data, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  
            if frame is None:
                print("[SERVER] Failed to decode image.")
                response = b'{"error":"decode_failed"}'
                
            else:
                squares = find_squares(frame)
                print(f"[SERVER] Found {len(squares)} square(s)")
                objects_list = []
                for square in squares:
                    points = square.reshape(4,2)
                    # Найдём минимальные и максимальные x и y
                    x_min = points[:, 0].min()
                    y_min = points[:, 1].min()
                    x_max = points[:, 0].max()
                    y_max = points[:, 1].max()

                    # Ширина и высота
                    w = x_max - x_min
                    h = y_max - y_min

                    # Создаём словарь
                    obj = {
                        "type": "square",
                        "x": int(x_min),
                        "y": int(y_min),
                        "w": int(w),
                        "h": int(h)
                    }
                    objects_list.append(obj)    
                
                
                response_dict ={"objects": objects_list}
                response_str = json.dumps(response_dict)
                response = response_str.encode("utf-8")

            conn.sendall(response)
        except Exception as e:
             print("[SERVER] Exception occurred:", e)
        finally:  
            conn.close()