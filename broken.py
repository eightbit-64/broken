import socket, threading

def handle_pair(agent_sock, operator_sock):
    def forward(src, dst):
        while True:
            try:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
            except:
                break
        src.close()
        dst.close()

    threading.Thread(target=forward, args=(agent_sock, operator_sock), daemon=True).start()
    threading.Thread(target=forward, args=(operator_sock, agent_sock), daemon=True).start()

def start_broker(agent_port=4444, operator_port=5555):
    agent_queue = []
    lock = threading.Lock()

    def agent_listener():
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', agent_port))
        s.listen(10)
        print(f"[*] In ascolto agent su :{agent_port}")
        while True:
            conn, addr = s.accept()
            print(f"[+] Agent connesso da {addr}")
            with lock:
                agent_queue.append(conn)

    def operator_listener():
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', operator_port))
        s.listen(5)
        print(f"[*] In ascolto operator su :{operator_port}")
        while True:
            conn, addr = s.accept()
            print(f"[+] Operator connesso da {addr}")
            with lock:
                if agent_queue:
                    agent = agent_queue.pop(0)
                    threading.Thread(target=handle_pair, args=(agent, conn), daemon=True).start()
                else:
                    conn.send(b"Nessun agent disponibile.\n")
                    conn.close()

    threading.Thread(target=agent_listener, daemon=True).start()
    operator_listener()

start_broker()
```

---

**`requirements.txt`:**
```
# no dependencies
