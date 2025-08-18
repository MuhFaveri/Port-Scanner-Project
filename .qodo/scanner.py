import socket
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor

# Dicionário com os nomes dos serviços mais comuns por porta
commom_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 123: "NTP", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

# Lista global para armazenar portas abertas
open_ports = []

# Lock para evitar conflitos ao acessar a lista de portas abertas em múltiplas threads
lock = threading.Lock()

# Verifica se o IP ou domínio informado é válido
def is_valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

# Retorna o nome do serviço associado à porta e protocolo
def get_service_name(port, protocol="tcp"):
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return commom_ports.get(port, "Desconhecido")

# Tenta obter o banner de um serviço TCP (informações da resposta do servidor)
def get_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner
    except:
        return None

# Escaneia uma porta TCP e adiciona à lista se estiver aberta
def scan_tcp_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            with lock:
                if (port, "TCP") not in open_ports:
                    open_ports.append((port, "TCP"))
        sock.close()
    except:
        pass

# Escaneia uma porta UDP e adiciona à lista se houver resposta ou timeout
def scan_udp_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)

        # Envia pacote DNS se for porta 53, senão envia "PING"
        if port == 53:
            dns_query = b"\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01"
            sock.sendto(dns_query, (target, port))
        else:
            sock.sendto(b"PING", (target, port))

        try:
            data, _ = sock.recvfrom(1024)
            with lock:
                if (port, "UDP") not in open_ports:
                    open_ports.append((port, "UDP"))
        except socket.timeout:
            # Mesmo sem resposta, pode estar aberta (UDP não garante retorno)
            with lock:
                if (port, "UDP") not in open_ports:
                    open_ports.append((port, "UDP"))
    except:
        pass
    finally:
        sock.close()

# Salva os resultados da varredura em um arquivo .txt e tenta abrir automaticamente
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
                for port, proto in sorted(open_ports):
                    service = get_service_name(port, proto.lower())
                    arquivo.write(f" Porta {port}/{proto}: {service}\n")
                    if proto == "TCP":
                        banner = get_banner(target, port)
                        if banner:
                            arquivo.write(f" --> Banner: {banner}\n")
            else:
                arquivo.write("Nenhuma porta aberta encontrada.\n")

        print(f"✅ Resultados salvos em: {nome_arquivo}")
        try:
            os.startfile(nome_arquivo)
        except AttributeError:
            try:
                os.system(f"open {nome_arquivo}")
            except:
                os.system(f"xdg-open {nome_arquivo}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

# Função principal que executa a varredura usando múltiplas threads
def executar_scan(target, tipo_scan, start_port, end_port):
    global open_ports
    open_ports = []

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            if tipo_scan == "TCP":
                executor.submit(scan_tcp_port, target, port)
            else:
                executor.submit(scan_udp_port, target, port)

    tempo_execucao = time.time() - start_time
    salvar_resultado_txt(target, open_ports, tempo_execucao)
    return tempo_execucao