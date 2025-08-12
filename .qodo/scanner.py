import socket
import threading
import time

# Entrada do usuário
target = input("Digite o IP ou domínio para escanear: ")
start_port = 1
end_port = 1024


# Função para escanear uma porta
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[+] Porta {port} aberta")
        sock.close()
    except:
        pass

# Início do contador de tempo
    
start_time = time.time()

# Loop para escanear portas de 1 a 1024
print(f"\nIniciando varredura em {target}...\n")
threads = []
for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan_port, args=(port,))
    thread.start()
    threads.append(thread)

# Aguardar todas as threads terminarem 

for thread in threads:
    thread.join()

    end_time = time.time()
    print(f"\nVarredura concluída em {end_time - start_time:.2} segundos.")

    
