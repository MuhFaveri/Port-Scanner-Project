# Importa bibliotecas necessárias
import socket                 # Para comunicação de rede (TCP/UDP)
import threading              # Para uso de múltiplas threads
import time                   # Para medir tempo e usar delays
import os                     # Para abrir arquivos automaticamente
import ipaddress              # Para manipular e validar redes/intervalos de IPs
from concurrent.futures import ThreadPoolExecutor  # Gerenciamento de threads
import matplotlib.pyplot as plt  # Para gerar o gráfico das portas abertas

# Dicionário com serviços comuns mapeados por porta
commom_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 123: "NTP", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

# Lista global para armazenar resultados (porta, protocolo, banner)
open_ports = []

# Lock para evitar conflitos quando várias threads alteram open_ports ao mesmo tempo
lock = threading.Lock()

# Valida se o destino informado é um IP ou domínio válido
def is_valid_target(target):
    try:
        socket.gethostbyname(target)  # Tenta resolver o endereço
        return True
    except socket.gaierror:
        return False

# Obtém o nome do serviço a partir da porta
def get_service_name(port, protocol="tcp"):
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return commom_ports.get(port, "Desconhecido")  # Fallback para nosso dicionário

# Captura o banner de um serviço TCP, se disponível
def get_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        # Só envia requisição HTTP se a porta for típica de HTTP
        if port in (80, 8080, 8000):
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")

        time.sleep(1)  # Espera para garantir que o servidor envie dados
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else None
    except:
        return None

# Escaneia uma porta TCP
def scan_tcp_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))  # 0 = porta aberta
        if result == 0:
            banner = get_banner(target, port)
            with lock:
                open_ports.append((port, "TCP", banner))
        sock.close()
    except:
        pass

# Escaneia uma porta UDP
def scan_udp_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        if port == 53:
            # Pacote DNS padrão para teste
            dns_query = b"\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01"
            sock.sendto(dns_query, (target, port))
        else:
            sock.sendto(b"PING", (target, port))
        try:
            data, _ = sock.recvfrom(1024)  # Se receber dados, consideramos aberta
            with lock:
                open_ports.append((port, "UDP", None))
        except socket.timeout:
            with lock:
                open_ports.append((port, "UDP", None))  # UDP pode estar aberto mesmo sem resposta
    except:
        pass
    finally:
        sock.close()

# Salva o resultado em um arquivo de texto com nome único (timestamp) e abre automaticamente
def salvar_resultado_txt(target, open_ports, tempo_execucao, stats):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"resultado_scan_{target.replace('.', '_')}_{timestamp}.txt"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Resultado da varredura em {target}\n")
            arquivo.write(f"Tempo de execução: {tempo_execucao:.2f} segundos\n")
            arquivo.write(f"Portas escaneadas: {stats['total_ports']}\n")
            arquivo.write(f"Threads utilizadas: {stats['threads']}\n")
            arquivo.write(f"Tempo médio por porta: {stats['tempo_medio']:.4f} segundos\n\n")
            if open_ports:
                for port_info in sorted(open_ports):
                    if len(port_info) == 3:
                        port, proto, banner = port_info
                    else:
                        port, proto = port_info
                        banner = None
                    service = get_service_name(port, proto.lower())
                    arquivo.write(f" Porta {port}/{proto}: {service}\n")
                    if banner:
                        arquivo.write(f" --> Banner: {banner}\n")
            else:
                arquivo.write("Nenhuma porta aberta encontrada.\n")
        os.startfile(nome_arquivo)  # Abre automaticamente o arquivo no Windows
    except:
        pass

# Mostra um gráfico de barras com as portas abertas (TCP em azul, UDP em verde)
def exibir_grafico(open_ports):
    if not open_ports:
        return
    portas = [str(p) for p, _, _ in open_ports]
    protocolos = [proto for _, proto, _ in open_ports]
    cores = ['blue' if proto == 'TCP' else 'green' for proto in protocolos]
    plt.figure(figsize=(10, 5))
    plt.bar(portas, [1] * len(portas), color=cores)
    plt.xlabel("Portas")
    plt.ylabel("Status")
    plt.title("Portas Abertas")
    plt.tight_layout()
    plt.show()

# Gera lista de IPs a partir de uma faixa CIDR (ex: 192.168.0.0/24)
def gerar_ips(faixa):
    try:
        rede = ipaddress.ip_network(faixa, strict=False)
        return [str(ip) for ip in rede.hosts()]
    except ValueError:
        return []

# Função principal que executa o scan
def executar_scan(target, tipo_scan, start_port, end_port, threads=100):
    global open_ports
    open_ports = []
    start_time = time.time()

    # Cria um pool de threads e distribui as portas para varredura
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port in range(start_port, end_port + 1):
            if tipo_scan == "TCP":
                executor.submit(scan_tcp_port, target, port)
            else:
                executor.submit(scan_udp_port, target, port)

    # Calcula estatísticas
    tempo_execucao = time.time() - start_time
    total_ports = end_port - start_port + 1
    tempo_medio = tempo_execucao / total_ports if total_ports else 0
    stats = {
        "tempo_medio": tempo_medio,
        "total_ports": total_ports,
        "threads": threads
    }

    # Salva no arquivo e mostra gráfico
    salvar_resultado_txt(target, open_ports, tempo_execucao, stats)
    exibir_grafico(open_ports)

    return tempo_execucao, stats