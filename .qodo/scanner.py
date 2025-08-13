# Importações necessárias
import socket
import threading
import time
import re
from tqdm import tqdm



# Dicionário de portas mais comuns
# Este dicionário pode ser usado para identificar serviços comuns associados a portas específicas.
commom_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53:"DNS",
    80:"HTTP",
    110: "POP3",
    143:"IMAP",
    443:"HTTPS",
    3306:"MySQL",
    3389:"RDP"
}

# Validação de IP/Domínio
def is_valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

# Entrada do usuário
target = input("Digite o IP ou domínio para escanear: ")

if not is_valid_target(target):
    print("Endereço inválido. Tente novamente.")
    exit()

# Intervalo de portas
try:
    start_port = int(input("Porta inicial: "))
    end_port = int(input("Porta final: "))
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        raise ValueError
except ValueError:
    print("Intervalo de portas inválido.")
    exit()



# Lista par armazenar portas abertas
open_ports = [] 


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

# Criação das threads com barra de progresso
print(f"\nIniciando varredura em {target}...\n")
threads = []
for port in tqdm(range(start_port, end_port + 1), desc="Escaneando"):
    thread = threading.Thread(target=scan_port, args=(port, ))
    thread.start()
    threads.append(thread)

# Aguardar todas as threads terminarem
for thread in threads:
    thread.join()

# Fim do contador de tempo (fora do loop!)
end_time = time.time()

# Exibir resultado resumido (apenas uma vez)
print(f"\nVarredura concluída em {end_time - start_time:.2f} segundos.")
if open_ports:
    print(f"Portas abertas encontradas: {', '.join(map(str, open_ports))}")
    for port in open_ports:
        service = commom_ports.get(port, "Desconhecido")
        print(f" Porta {port}: {service}")
    else:
        print("Nenhuma porta aberta encontrada.")

    
