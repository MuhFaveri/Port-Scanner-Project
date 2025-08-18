import tkinter as tk
from tkinter import ttk, messagebox
import threading
import scanner

# Função chamada ao clicar no botão "Iniciar Scan"
def iniciar_scan():
    # Captura os dados inseridos pelo usuário
    target = entry_target.get().strip()
    tipo = combo_tipo.get()
    try:
        start_port = int(entry_inicio.get())
        end_port = int(entry_fim.get())
    except ValueError:
        messagebox.showerror("Erro", "Portas devem ser números inteiros.")
        return

    # Valida o IP ou domínio
    if not scanner.is_valid_target(target):
        messagebox.showerror("Erro", "Endereço inválido.")
        return

    # Valida o tipo de escaneamento
    if tipo not in ["TCP", "UDP"]:
        messagebox.showerror("Erro", "Tipo de escaneamento inválido. Escolha 'TCP' ou 'UDP'.")
        return

    # Valida o intervalo de portas
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Erro", "Intervalo de portas inválido.")
        return

    # Desativa o botão e limpa a área de resultados
    btn_scan.config(state="disabled")
    resultado_text.delete("1.0", tk.END)

    # Função que será executada em uma thread separada
    def executar():
        resultado_text.insert(tk.END, f"Iniciando varredura {tipo} em {target}...\n")

        # Chama a função principal do scanner
        tempo_execucao = scanner.executar_scan(target, tipo, start_port, end_port)

        # Exibe o tempo de execução
        resultado_text.insert(tk.END, f"\nVarredura concluída em {tempo_execucao:.2f} segundos.\n")

        # Exibe os resultados das portas abertas
        if scanner.open_ports:
            for port, proto in scanner.open_ports:
                service = scanner.get_service_name(port, proto.lower())
                resultado_text.insert(tk.END, f" Porta {port}/{proto}: {service}\n")
        else:
            resultado_text.insert(tk.END, "Nenhuma porta aberta encontrada.\n")

        # Reativa o botão após a conclusão
        btn_scan.config(state="normal")

    # Inicia a thread para não travar a interface
    threading.Thread(target=executar).start()

# Criação da janela principal da interface gráfica
root = tk.Tk()
root.title("Scanner de Portas")
root.geometry("500x600")

# Frame principal com padding
frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

# Campo para IP ou domínio
ttk.Label(frame, text="IP ou Domínio:").pack(anchor="w")
entry_target = ttk.Entry(frame)
entry_target.pack(fill="x")

# Campo para tipo de escaneamento (TCP ou UDP)
ttk.Label(frame, text="Tipo de Escaneamento:").pack(anchor="w")
combo_tipo = ttk.Combobox(frame, values=["TCP", "UDP"])
combo_tipo.pack(fill="x")
combo_tipo.current(0)

# Campo para porta inicial
ttk.Label(frame, text="Porta Inicial:").pack(anchor="w")
entry_inicio = ttk.Entry(frame)
entry_inicio.pack(fill="x")

# Campo para porta final
ttk.Label(frame, text="Porta Final:").pack(anchor="w")
entry_fim = ttk.Entry(frame)
entry_fim.pack(fill="x")

# Botão para iniciar o escaneamento
btn_scan = ttk.Button(frame, text="Iniciar Scan", command=iniciar_scan)
btn_scan.pack(pady=10)

# Área de texto para exibir os resultados
resultado_text = tk.Text(frame, height=15)
resultado_text.pack(fill="both", expand=True)

# Inicia o loop principal da interface
root.mainloop()