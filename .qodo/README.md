# 🔍 Scanner de Portas TCP em Python

Um scanner de portas simples e eficiente feito em Python, com suporte a entrada dinâmica de IP ou domínio via linha de comando. Ideal para estudos de redes, segurança e automação.

---

## 🚀 Objetivo

Identificar **portas abertas** em um host (IP ou domínio) especificado pelo usuário, permitindo mapear serviços expostos e entender a superfície de ataque de um sistema.

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- Bibliotecas padrão:
  - `socket` — para conexões TCP
  - `threading` — para escaneamento paralelo
  - `argparse` — para entrada de argumentos via terminal

---

## 📦 Estrutura do Projeto

```
port_scanner/
├── scanner.py          # Código principal do scanner
├── README.md           # Documentação do projeto
```

---

## ⚙️ Como Usar

1. Clone ou baixe o projeto:
   ```bash
   git clone https://github.com/seu-usuario/port_scanner.git
   cd port_scanner
   ```

2. Execute o scanner com o IP ou domínio desejado:
   ```bash
   python scanner.py -t 192.168.0.1
   ```

   Ou, para escanear um domínio:
   ```bash
   python scanner.py -t scanme.nmap.org
   ```

---

## 🧠 Como Funciona

- Recebe o alvo via argumento `-t` ou `--target`
- Escaneia as portas de **1 a 1024**
- Usa **threads** para acelerar o processo
- Exibe no terminal as portas abertas encontradas

---

## ⚠️ Aviso de Ética e Segurança

Este projeto é **educacional**. Use **apenas em ambientes autorizados**, como:

- Sua própria máquina
- Máquinas virtuais de teste
- Hosts que permitem escaneamento (ex: `scanme.nmap.org`)

**Nunca escaneie redes ou sistemas sem permissão. Isso pode ser ilegal.**

---

## 📈 Melhorias Futuras

- Escolha de intervalo de portas via argumentos
- Banner grabbing (identificação de serviços)
- Exportar resultados para `.txt` ou `.csv`
- Interface gráfica com `tkinter` ou `PyQt`
- Detecção de portas UDP

---

## 👨‍💻 Autor

Murilo Vinícius de Faveri — projeto para estudo de programação e cibersegurança.

---



