import socket
import threading
import time
import os
from tqdm import tqdm

# Dicionário de portas mais comuns
commom_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

# Validação de IP/Domínio
def is_valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

# Obter nome do serviço
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return commom_ports.get(port, "Desconhecido")

# Obter banner do serviço
def get_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner
    except:
        return None

# Função para escanear uma porta
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
            print(f"[+] Porta {port} aberta")
        sock.close()
    except:
        pass

# Função para salvar e abrir o resultado
def salvar_resultado_txt(target, open_ports, tempo_execucao):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"resultado_scan_{target.replace('.', '_')}_{timestamp}.txt"
    print(f"\n📁 Criando arquivo: {nome_arquivo}")

    try:
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(f"Resultado da varredura em {target}\n")
            arquivo.write(f"Tempo de execução: {tempo_execucao:.2f} segundos\n\n")

            if open_ports:
                arquivo.write("Portas abertas encontradas:\n")
                for port in open_ports:
                    service = get_service_name(port)
                    banner = get_banner(target, port)
                    arquivo.write(f" Porta {port}: {service}\n")
                    if banner:
                        arquivo.write(f"   ↪ Banner: {banner}\n")
            else:
                arquivo.write("Nenhuma porta aberta encontrada.\n")

        print(f"✅ Resultados salvos em: {nome_arquivo}")

        # Abrir o arquivo automaticamente
        try:
            os.startfile(nome_arquivo)  # Windows
        except AttributeError:
            try:
                os.system(f"open {nome_arquivo}")  # macOS
            except:
                os.system(f"xdg-open {nome_arquivo}")  # Linux

    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

# Entrada do usuário
target = input("Digite o IP ou domínio para escanear: ").strip()
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

# Lista para armazenar portas abertas
open_ports = []

# Início da varredura
print(f"\n🚀 Iniciando varredura em {target}...\n")
start_time = time.time()

threads = []
for port in tqdm(range(start_port, end_port + 1), desc="Escaneando"):
    thread = threading.Thread(target=scan_port, args=(port,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end_time = time.time()
tempo_execucao = end_time - start_time

# Salvar e abrir resultado
salvar_resultado_txt(target, open_ports, tempo_execucao)

# Exibir resumo no terminal
print(f"\n⏱️ Varredura concluída em {tempo_execucao:.2f} segundos.")
if open_ports:
    print(f"🔓 Portas abertas encontradas: {', '.join(map(str, open_ports))}")
    for port in open_ports:
        service = get_service_name(port)
        print(f" Porta {port}: {service}")
else:
    print("🔒 Nenhuma porta aberta encontrada.")