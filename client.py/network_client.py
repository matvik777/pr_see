import socket
import struct

def send_image_to_server(host: str, port: int, image_path: str):
    with open(image_path, "rb") as f:
        img_data = f.read()
    file_size = len(img_data) 
      
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"[CLIENT] Connected to {host}:{port}")

        lenght_bytes = struct.pack("!I", file_size)
        client_socket.sendall(lenght_bytes)
        
        
        client_socket.sendall(img_data)
        print(f"[CLIENT] Sent {len(img_data)} bytes")

        response = client_socket.recv(1024)
        print(f"[CLIENT] Received {len(response)} bytes of response")

    finally:
        client_socket.close()
    
    return response