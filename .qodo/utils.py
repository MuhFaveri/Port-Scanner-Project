import tkinter as tk
from tkinter import ttk, messagebox   # ttk = widgets com tema visual
import threading                      # Para rodar o scan sem travar a interface
import scanner                         # Nosso módulo com a lógica do scan (código anterior)

# Classe principal da interface gráfica do Scanner
class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanner de Portas Avançado")   # Título da janela
        self.root.geometry("550x650")                   # Tamanho inicial da janela

        # Frame principal com padding
        self.frame = ttk.Frame(root, padding="10")
        self.frame.pack(fill="both", expand=True)

        # Campo para IP ou faixa de IPs
        ttk.Label(self.frame, text="IP ou Faixa (ex: 192.168.0.0/24):").pack(anchor="w")
        self.entry_target = ttk.Entry(self.frame)
        self.entry_target.pack(fill="x")

        # Seletor do tipo de escaneamento
        ttk.Label(self.frame, text="Tipo de Escaneamento:").pack(anchor="w")
        self.combo_tipo = ttk.Combobox(self.frame, values=["TCP", "UDP"])
        self.combo_tipo.pack(fill="x")
        self.combo_tipo.current(0)  # TCP como padrão

        # Porta inicial
        ttk.Label(self.frame, text="Porta Inicial:").pack(anchor="w")
        self.entry_inicio = ttk.Entry(self.frame)
        self.entry_inicio.pack(fill="x")

        # Porta final
        ttk.Label(self.frame, text="Porta Final:").pack(anchor="w")
        self.entry_fim = ttk.Entry(self.frame)
        self.entry_fim.pack(fill="x")

        # Botão para iniciar o scan
        self.btn_scan = ttk.Button(self.frame, text="Iniciar Scan", command=self.iniciar_scan)
        self.btn_scan.pack(pady=10)

        # Caixa de texto para mostrar resultados
        self.resultado_text = tk.Text(self.frame, height=20)
        self.resultado_text.pack(fill="both", expand=True)

    # Função chamada quando o botão "Iniciar Scan" é clicado
    def iniciar_scan(self):
        target_input = self.entry_target.get().strip()  # IP ou faixa digitada
        tipo = self.combo_tipo.get()                    # TCP ou UDP

        # Validação das portas (devem ser inteiros)
        try:
            start_port = int(self.entry_inicio.get())
            end_port = int(self.entry_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Portas devem ser números inteiros.")
            return

        # Verifica intervalo válido de portas
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            messagebox.showerror("Erro", "Intervalo de portas inválido.")
            return

        # Desativa o botão para evitar múltiplos scans simultâneos
        self.btn_scan.config(state="disabled")
        self.resultado_text.delete("1.0", tk.END)  # Limpa resultados anteriores

        # Função interna que fará o scan em uma thread separada
        def executar():
            # Se for faixa CIDR, gera lista de IPs; senão, só um IP
            ips = scanner.gerar_ips(target_input) if "/" in target_input else [target_input]
            for ip in ips:
                # Valida IP/destino
                if not scanner.is_valid_target(ip):
                    self.resultado_text.insert(tk.END, f"❌ IP inválido: {ip}\n")
                    continue

                # Informa início do scan
                self.resultado_text.insert(tk.END, f"\n🔍 Escaneando {ip} ({tipo})...\n")

                # Executa o scan e pega tempo e estatísticas
                tempo_execucao, stats = scanner.executar_scan(ip, tipo, start_port, end_port)

                # Mostra tempo total e média por porta
                self.resultado_text.insert(
                    tk.END,
                    f"⏱️ Tempo: {tempo_execucao:.2f}s | Média por porta: {stats['tempo_medio']:.4f}s\n"
                )

                # Mostra portas abertas ou informa se nenhuma foi encontrada
                if scanner.open_ports:
                    for port, proto, banner in scanner.open_ports:
                        service = scanner.get_service_name(port, proto.lower())
                        self.resultado_text.insert(tk.END, f" Porta {port}/{proto}: {service}\n")
                        if banner:
                            self.resultado_text.insert(tk.END, f" --> Banner: {banner}\n")
                else:
                    self.resultado_text.insert(tk.END, "Nenhuma porta aberta encontrada.\n")

            # Reativa o botão após finalizar
            self.btn_scan.config(state="normal")

        # Inicia a thread para rodar o scan sem travar a interface
        threading.Thread(target=executar).start()

# Execução da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()