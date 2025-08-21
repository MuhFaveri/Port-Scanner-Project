# Importa bibliotecas necessárias
import socket       # Comunicação de rede
import threading    # Controle de concorrência com threads
import time         # Medição de tempo
import os           # Operações com sistema de arquivos
import ipaddress    # Manipulação de faixas de IP
import csv          # Exportação para CSV
import json         # Exportação para JSON
from concurrent.futures import ThreadPoolExecutor  # Execução paralela com pool de threads

# Dicionário com mapeamento de portas comuns para nomes de serviços
commom_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 123: "NTP", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

# Lista global para armazenar resultados de portas abertas
open_ports = []

# Lock para evitar conflitos de acesso à lista entre múltiplas threads
lock = threading.Lock()

# Verifica se o alvo é um IP ou domínio válido
def is_valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

# Retorna o nome do serviço associado à porta
def get_service_name(port, protocol="tcp"):
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return commom_ports.get(port, "Desconhecido")

# Captura o banner de um serviço TCP (informações que o serviço retorna ao conectar)
def get_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        if port in (80, 8080, 8000):  # Envia requisição HTTP para serviços web
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        time.sleep(1)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else None
    except:
        return None

# Captura banner de serviços UDP conhecidos usando pacotes específicos
def get_udp_banner(ip, port):
    probes = {
        53: b"\x12\x34..." ,  # DNS
        123: b'\x1b' + 47 * b'\0',  # NTP
        161: b"\x30\x26...",  # SNMP
        1900: b"M-SEARCH * HTTP/1.1..."  # SSDP
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

# Escaneia uma porta TCP e salva se estiver aberta
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

# Escaneia uma porta UDP e tenta capturar banner
def scan_udp_port(target, port):
    try:
        banner = get_udp_banner(target, port)
        with lock:
            open_ports.append((port, "UDP", banner))
    except:
        pass

# Salva os resultados em arquivo TXT
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

# Salva os resultados em arquivo CSV
def salvar_resultado_csv(target, open_ports, tempo_execucao, stats):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"resultado_scan_{target.replace('.', '_')}_{timestamp}.csv"
    try:
        with open(nome_arquivo, mode="w", newline='', encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["Porta", "Protocolo", "Serviço", "Banner"])
            for port, proto, banner in sorted(open_ports):
                service = get_service_name(port, proto.lower())
                writer.writerow([port, proto, service, banner or ""])
        os.startfile(nome_arquivo)
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

# Salva os resultados em arquivo JSON
def salvar_resultado_json(target, open_ports, tempo_execucao, stats):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"resultado_scan_{target.replace('.', '_')}_{timestamp}.json"
    resultado = {
        "alvo": target,
        "tempo_execucao": tempo_execucao,
        "estatisticas": stats,
        "portas_abertas": []
    }

    for port, proto, banner in sorted(open_ports):
        service = get_service_name(port, proto.lower())
        resultado["portas_abertas"].append({
            "porta": port,
            "protocolo": proto,
            "servico": service,
            "banner": banner or ""
        })

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(resultado, arquivo, indent=4, ensure_ascii=False)
        os.startfile(nome_arquivo)
    except Exception as e:
        print(f"Erro ao salvar JSON: {e}")

# Prepara dados para visualização gráfica (não exibe diretamente)
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

# Função principal que executa o scan de portas
def executar_scan(target, tipo_scan, start_port, end_port, threads=100, mostrar_desconhecidos=False):
    global open_ports
    open_ports = []
    start_time = time.time()

    # Executa varredura em paralelo usando ThreadPool
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port in range(start_port, end_port + 1):
            if tipo_scan == "TCP":
                executor.submit(scan_tcp_port, target, port)
            else:
                executor.submit(scan_udp_port, target, port)

    # Calcula estatísticas de execução
    tempo_execucao = time.time() - start_time
    total_ports = end_port - start_port + 1
    tempo_medio = tempo_execucao / total_ports if total_ports else 0
    stats = {
        "tempo_medio": tempo_medio,
        "total_ports": total_ports,
        "threads": threads
    }

    # Filtra serviços desconhecidos, se necessário
    if not mostrar_desconhecidos:
        open_ports = [
            (port, proto, banner)
            for (port, proto, banner) in open_ports
            if get_service_name(port, proto.lower()) != "Desconhecido"
        ]

    # Salva os resultados em múltiplos formatos
    salvar_resultado_txt(target, open_ports, tempo_execucao, stats)
    salvar_resultado_csv(target, open_ports, tempo_execucao, stats)
    salvar_resultado_json(target, open_ports, tempo_execucao, stats)

    return tempo_execucao, stats