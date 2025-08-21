# Importa bibliotecas necessárias
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import scanner  # Importa o módulo com a lógica de escaneamento

# Classe principal da aplicação
class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanner de Portas Avançado")  # Título da janela
        self.root.geometry("550x700")  # Tamanho da janela

        # Cria um frame com padding
        self.frame = ttk.Frame(root, padding="10")
        self.frame.pack(fill="both", expand=True)

        # Campo para IP ou faixa CIDR
        ttk.Label(self.frame, text="IP ou Faixa (ex: 192.168.0.0/24):").pack(anchor="w")
        self.entry_target = ttk.Entry(self.frame)
        self.entry_target.pack(fill="x")

        # Combobox para escolher tipo de escaneamento (TCP ou UDP)
        ttk.Label(self.frame, text="Tipo de Escaneamento:").pack(anchor="w")
        self.combo_tipo = ttk.Combobox(self.frame, values=["TCP", "UDP"])
        self.combo_tipo.pack(fill="x")
        self.combo_tipo.current(0)  # Seleciona TCP por padrão

        # Campo para porta inicial
        ttk.Label(self.frame, text="Porta Inicial:").pack(anchor="w")
        self.entry_inicio = ttk.Entry(self.frame)
        self.entry_inicio.pack(fill="x")

        # Campo para porta final
        ttk.Label(self.frame, text="Porta Final:").pack(anchor="w")
        self.entry_fim = ttk.Entry(self.frame)
        self.entry_fim.pack(fill="x")

        # Checkbox para mostrar serviços desconhecidos
        self.mostrar_desconhecidos = tk.BooleanVar(value=False)
        self.check_desconhecidos = ttk.Checkbutton(
            self.frame,
            text="Mostrar serviços desconhecidos",
            variable=self.mostrar_desconhecidos
        )
        self.check_desconhecidos.pack(anchor="w", pady=5)

        # Botão para iniciar o escaneamento
        self.btn_scan = ttk.Button(self.frame, text="Iniciar Scan", command=self.iniciar_scan)
        self.btn_scan.pack(pady=10)

        # Área de texto para exibir os resultados
        self.resultado_text = tk.Text(self.frame, height=20)
        self.resultado_text.pack(fill="both", expand=True)

    # Função chamada ao clicar no botão "Iniciar Scan"
    def iniciar_scan(self):
        target_input = self.entry_target.get().strip()  # IP ou faixa
        tipo = self.combo_tipo.get()  # TCP ou UDP
        mostrar_todos = self.mostrar_desconhecidos.get()  # True ou False

        # Valida se as portas são números inteiros
        try:
            start_port = int(self.entry_inicio.get())
            end_port = int(self.entry_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Portas devem ser números inteiros.")
            return

        # Valida intervalo de portas
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            messagebox.showerror("Erro", "Intervalo de portas inválido.")
            return

        # Desativa botão e limpa área de texto
        self.btn_scan.config(state="disabled", text="Escaneando...")
        self.resultado_text.delete("1.0", tk.END)

        # Função que será executada em uma thread separada
        def executar():
            # Gera lista de IPs se for uma faixa CIDR
            ips = scanner.gerar_ips(target_input) if "/" in target_input else [target_input]
            for ip in ips:
                # Valida IP
                if not scanner.is_valid_target(ip):
                    self.resultado_text.insert(tk.END, f"❌ IP inválido: {ip}\n")
                    continue

                self.resultado_text.insert(tk.END, f"\n🔍 Escaneando {ip} ({tipo})...\n")

                # Executa o escaneamento
                tempo_execucao, stats = scanner.executar_scan(
                    ip, tipo, start_port, end_port, mostrar_desconhecidos=mostrar_todos
                )

                # Exibe estatísticas
                self.resultado_text.insert(
                    tk.END,
                    f"⏱️ Tempo: {tempo_execucao:.2f}s | Média por porta: {stats['tempo_medio']:.4f}s\n"
                )

                encontrados = False
                # Exibe resultados das portas abertas
                for port, proto, banner in scanner.open_ports:
                    service = scanner.get_service_name(port, proto.lower())
                    if mostrar_todos or service != "Desconhecido":
                        encontrados = True
                        self.resultado_text.insert(tk.END, f" Porta {port}/{proto}: {service}\n")
                        if banner:
                            self.resultado_text.insert(tk.END, f" --> Banner: {banner}\n")
                        else:
                            self.resultado_text.insert(tk.END, f" --> Sem banner detectado\n")

                # Caso nenhuma porta conhecida seja encontrada
                if not encontrados:
                    self.resultado_text.insert(tk.END, "Nenhuma porta com serviço conhecido encontrada.\n")

                # Exibe gráfico na thread principal
                grafico = scanner.preparar_dados_grafico(scanner.open_ports)
                if grafico:
                    portas, cores = grafico
                    def mostrar_grafico():
                        import matplotlib.pyplot as plt
                        plt.figure(figsize=(10, 5))
                        plt.bar(portas, [1] * len(portas), color=cores)
                        plt.xlabel("Portas")
                        plt.ylabel("Status")
                        plt.title("Portas Abertas")
                        plt.tight_layout()
                        plt.show()
                    self.root.after(0, mostrar_grafico)

            # Reativa botão após o scan
            self.btn_scan.config(state="normal", text="Iniciar Scan")

        # Inicia a thread para não travar a interface
        threading.Thread(target=executar).start()

# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()