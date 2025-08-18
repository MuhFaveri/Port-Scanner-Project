import tkinter as tk
from tkinter import ttk, messagebox
import threading
import scanner

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanner de Portas")
        self.root.geometry("500x600")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.pack(fill="both", expand=True)

        # IP ou Domínio
        ttk.Label(self.frame, text="IP ou Domínio:").pack(anchor="w")
        self.entry_target = ttk.Entry(self.frame)
        self.entry_target.pack(fill="x")

        # Tipo de Escaneamento
        ttk.Label(self.frame, text="Tipo de Escaneamento:").pack(anchor="w")
        self.combo_tipo = ttk.Combobox(self.frame, values=["TCP", "UDP"])
        self.combo_tipo.pack(fill="x")
        self.combo_tipo.current(0)

        # Porta Inicial
        ttk.Label(self.frame, text="Porta Inicial:").pack(anchor="w")
        self.entry_inicio = ttk.Entry(self.frame)
        self.entry_inicio.pack(fill="x")

        # Porta Final
        ttk.Label(self.frame, text="Porta Final:").pack(anchor="w")
        self.entry_fim = ttk.Entry(self.frame)
        self.entry_fim.pack(fill="x")

        # Botão de Scan
        self.btn_scan = ttk.Button(self.frame, text="Iniciar Scan", command=self.iniciar_scan)
        self.btn_scan.pack(pady=10)

        # Área de Resultado
        self.resultado_text = tk.Text(self.frame, height=15)
        self.resultado_text.pack(fill="both", expand=True)

    def iniciar_scan(self):
        target = self.entry_target.get().strip()
        tipo = self.combo_tipo.get()

        try:
            start_port = int(self.entry_inicio.get())
            end_port = int(self.entry_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Portas devem ser números inteiros.")
            return

        if not scanner.is_valid_target(target):
            messagebox.showerror("Erro", "Endereço inválido.")
            return

        if tipo not in ["TCP", "UDP"]:
            messagebox.showerror("Erro", "Tipo de escaneamento inválido. Escolha 'TCP' ou 'UDP'.")
            return

        if start_port < 1 or end_port > 65535 or start_port > end_port:
            messagebox.showerror("Erro", "Intervalo de portas inválido.")
            return

        self.btn_scan.config(state="disabled")
        self.resultado_text.delete("1.0", tk.END)

        def executar():
            self.resultado_text.insert(tk.END, f"Iniciando varredura {tipo} em {target}...\n")

            tempo_execucao = scanner.executar_scan(target, tipo, start_port, end_port)

            self.resultado_text.insert(tk.END, f"\nVarredura concluída em {tempo_execucao:.2f} segundos.\n")

            if scanner.open_ports:
                for port, proto in scanner.open_ports:
                    service = scanner.get_service_name(port, proto.lower())
                    self.resultado_text.insert(tk.END, f" Porta {port}/{proto}: {service}\n")
            else:
                self.resultado_text.insert(tk.END, "Nenhuma porta aberta encontrada.\n")

            self.btn_scan.config(state="normal")

        threading.Thread(target=executar).start()

# Execução da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()