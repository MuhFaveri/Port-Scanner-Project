# 🔍 Port Scanner Python — Scanner de Portas TCP e UDP

Um scanner de portas **TCP e UDP** simples, eficiente e interativo, escrito em Python. Utiliza **multi-threading**, **barra de progresso com `tqdm`**, captura **banners de serviços**, e gera arquivos de resultado com **timestamp automático**. Ideal para escanear hosts locais ou remotos com rapidez, clareza e profundidade.

---

## 📋 Descrição

Este programa escaneia portas TCP ou UDP de um host específico para identificar quais estão abertas e quais serviços podem estar ativos. É útil para:

- Testes de segurança em redes próprias  
- Verificação de serviços em execução  
- Diagnóstico de conectividade  
- Aprendizado sobre redes e cibersegurança

---

## 🚀 Instalação

### ✅ Pré-requisitos

- Python 3.6 ou superior  
- Biblioteca externa: `tqdm`

### 📦 Instalar `tqdm`

```bash
pip install tqdm
```

### 🔍 Verificar versão do Python

```bash
python --version
# ou
python3 --version
```

---

## 🎯 Como Usar

### 1. Executar o scanner

```bash
python scanner.py
```

### 2. O programa solicitará:

```text
Digite o IP ou domínio para escanear: [ex: google.com]
Tipo de escaneamento (TCP/UDP): [ex: TCP]
Porta inicial: [ex: 1]
Porta final: [ex: 1024]
```

---

## 📊 Funcionalidades

- ✅ Multi-threading: escaneamento paralelo de portas  
- ✅ Barra de progresso com `tqdm`  
- ✅ Suporte a escaneamento TCP e UDP  
- ✅ Identificação de serviços comuns (HTTP, FTP, SSH etc.)  
- ✅ Captura de banners de serviços TCP (quando disponíveis)  
- ✅ Validação de IP/domínio antes da varredura  
- ✅ Entrada personalizada de intervalo de portas  
- ✅ Tempo total de execução exibido  
- ✅ Resultado salvo automaticamente com nome único  
- ✅ Abertura automática do arquivo de resultado após a varredura  
- ✅ Resumo final com serviços conhecidos e desconhecidos

---

## 🖥️ Exemplos de Uso

### Escanear localhost (TCP)

```bash
python scanner.py
# Digite: 127.0.0.1
# Tipo: TCP
```

### Escanear roteador local (UDP)

```bash
python scanner.py
# Digite: 192.168.0.1
# Tipo: UDP
```

### Escanear site público (TCP)

```bash
python scanner.py
# Digite: google.com
# Tipo: TCP
```

---

## 📋 Saída Esperada

```text
🚀 Iniciando varredura TCP em google.com...

Escaneando: 100%|████████████████████████| 1024/1024 [00:02<00:00, 500.00it/s]

✅ Resultados salvos em: resultado_scan_google_com_20250814_1345.txt
⏱️ Varredura concluída em 2.34 segundos.

🔓 Portas com serviços conhecidos:
 Porta 80/TCP: HTTP
 --> Banner: HTTP/1.1 200 OK

🔍 Portas sem serviço conhecido:
 9999/TCP
```

---

## 📁 Estrutura do Projeto

```
port-scanner/
│
├── scanner.py                         # Arquivo principal do scanner
├── resultado_scan_<host>_<data>.txt  # Arquivos gerados com os resultados
└── README.md                          # Documentação do projeto
```

> Os arquivos de resultado são gerados com nome único, como `resultado_scan_google_com_20250814_1345.txt`, permitindo histórico de varreduras.

---

## ⚠️ Avisos Importantes

### Uso Responsável

- ⚠️ Use apenas em redes que você possui ou tem permissão para testar.  
- ❌ Não utilize para atividades maliciosas ou invasivas.

---

## 👨‍💻 Autor

**Murilo Vinícius de Faveri**  
Projeto desenvolvido para estudo de programação, redes e cibersegurança.

---
