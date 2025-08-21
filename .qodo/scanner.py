import socket
import threading
import time
import os
import ipaddress
from concurrent.futures import ThreadPoolExecutor

# Dicionário com serviços comuns mapeados por porta
commom_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 123: "NTP", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

# Lista global para armazenar resultados (porta, protocolo, banner)
open_ports = []

# Lock para evitar conflitos entre threads
lock = threading.Lock()

# Valida se o destino informado é um IP ou domínio válido
def is_valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

# Obtém o nome do serviço a partir da porta
def get_service_name(port, protocol="tcp"):
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return commom_ports.get(port, "Desconhecido")

# Captura o banner de um serviço TCP
def get_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        if port in (80, 8080, 8000):
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        time.sleep(1)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else None
    except:
        return None

# Tenta obter banner inteligente de serviços UDP conhecidos
def get_udp_banner(ip, port):
    probes = {
        53: b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + b"\x06google\x03com\x00\x00\x01\x00\x01",
        123: b'\x1b' + 47 * b'\0',
        161: b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa0\x19\x02\x04\x70\x00\x00\x01\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00",
        1900: b"M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nMAN:\"ssdp:discover\"\r\nMX:1\r\nST:ssdp:all\r\n\r\n"
    }

    if port not in probes:
        return None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(probes[port], (ip, port))
        data, _ = sock.recvfrom(1024)
        return data.decode(errors="ignore").strip()
    except:
        return None
    finally:
        sock.close()

# Escaneia uma porta TCP
def scan_tcp_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            banner = get_banner(target, port)
            with lock:
                open_ports.append((port, "TCP", banner))
        sock.close()
    except:
        pass

# Escaneia uma porta UDP com tentativa de banner inteligente
def scan_udp_port(target, port):
    try:
        banner = get_udp_banner(target, port)
        with lock:
            open_ports.append((port, "UDP", banner))
    except:
        pass

# Salva o resultado em um arquivo de texto
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
                    port, proto, banner = port_info
                    service = get_service_name(port, proto.lower())
                    arquivo.write(f" Porta {port}/{proto}: {service}\n")
                    if banner:
                        arquivo.write(f" --> Banner: {banner}\n")
            else:
                arquivo.write("Nenhuma porta aberta encontrada.\n")
        os.startfile(nome_arquivo)
    except:
        pass

# Prepara os dados para o gráfico (sem exibir diretamente)
def preparar_dados_grafico(open_ports):
    if not open_ports:
        return None
    portas = [str(p) for p, _, _ in open_ports]
    protocolos = [proto for _, proto, _ in open_ports]
    cores = ['blue' if proto == 'TCP' else 'green' for proto in protocolos]
    return portas, cores

# Gera lista de IPs a partir de uma faixa CIDR
def gerar_ips(faixa):
    try:
        rede = ipaddress.ip_network(faixa, strict=False)
        return [str(ip) for ip in rede.hosts()]
    except ValueError:
        return []

# Função principal que executa o scan
def executar_scan(target, tipo_scan, start_port, end_port, threads=100, mostrar_desconhecidos=False):
    global open_ports
    open_ports = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port in range(start_port, end_port + 1):
            if tipo_scan == "TCP":
                executor.submit(scan_tcp_port, target, port)
            else:
                executor.submit(scan_udp_port, target, port)

    tempo_execucao = time.time() - start_time
    total_ports = end_port - start_port + 1
    tempo_medio = tempo_execucao / total_ports if total_ports else 0
    stats = {
        "tempo_medio": tempo_medio,
        "total_ports": total_ports,
        "threads": threads
    }

    # Filtra serviços desconhecidos se necessário
    if not mostrar_desconhecidos:
        open_ports = [
            (port, proto, banner)
            for (port, proto, banner) in open_ports
            if get_service_name(port, proto.lower()) != "Desconhecido"
        ]

    salvar_resultado_txt(target, open_ports, tempo_execucao, stats)
    return tempo_execucao, stats