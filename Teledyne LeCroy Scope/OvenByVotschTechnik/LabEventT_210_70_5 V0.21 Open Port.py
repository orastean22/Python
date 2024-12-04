# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 16/10/2024
# -- Update on 04/12/2024 - DRAFT!!!!
# -- Author: AdrianO
# -- Version 0.2 - Read real time temperature for oven based on socket via TCP/IP
# -- Script Task: Remote control LabEvent oven for Burin IN 2 (set and read temperature and humidity)
# -- Oven Brand: Votschtechnik
# -- Oven Model: LabEvent T/210/70/5     
# -- Setting the IP: 192.168.122.50
# -- see pdf doc section 6.2.11 command list
# -- Port 502 (JUMO diraTRON controller communication)


import socket

def send_command(ip, port, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print(f"Connected to {ip}:{port}")
            s.sendall(command.encode('latin-1'))  # Use 'latin-1' encoding
            print(f"Sent: {command}")
            response = s.recv(1024).decode('latin-1').strip()  # Decode using 'latin-1'
            print(f"Response: {response}")
            return response
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    oven_ip = "127.0.0.1"
    oven_port = 7777

    # Separator
    separator = chr(182)  # ASCII code 182

    # Command with Simpati ID and separator
    initialization_command = f"10006{separator}1\r\n"

    print("Sending initialization command...")
    response = send_command(oven_ip, oven_port, initialization_command)
    print(f"Initialization Response: {response}")











































