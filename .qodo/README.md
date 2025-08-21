# 🔍 Port Scanner Python — Scanner de Portas TCP e UDP

Um scanner de portas **TCP e UDP** completo, eficiente e interativo, escrito em Python. Utiliza **multi-threading**, captura **banners de serviços**, gera arquivos de resultado com **timestamp automático**, e conta com **visualização gráfica das portas abertas** via `matplotlib`. Com interface gráfica em **Tkinter**, é ideal para escanear hosts locais ou remotos com rapidez, clareza e profundidade.

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
- Bibliotecas externas: `matplotlib`

### 📦 Instalar dependências

```bash
pip install matplotlib
```

### 🔍 Verificar versão do Python

```bash
python --version
# ou
python3 --version
```

---

## 🎯 Como Usar

### 1. Executar a interface gráfica

```bash
python utils.py
```

### 2. Preencha os campos

- IP ou domínio (ex: `google.com`)  
- Tipo de escaneamento (`TCP` ou `UDP`)  
- Porta inicial (ex: `1`)  
- Porta final (ex: `1024`)  
- Marque ou desmarque a opção **"Mostrar serviços desconhecidos"**  
- Clique em **Iniciar Scan**

---

## 📊 Funcionalidades

- ✅ Multi-threading com controle de concorrência  
- ✅ Interface gráfica com Tkinter  
- ✅ Suporte a escaneamento TCP e UDP  
- ✅ Identificação de serviços comuns (HTTP, FTP, SSH etc.)  
- ✅ Captura de banners de serviços TCP e UDP (quando disponíveis)  
- ✅ Detecção inteligente de serviços UDP via pacotes específicos  
- ✅ Validação de IP/domínio antes da varredura  
- ✅ Entrada personalizada de intervalo de portas  
- ✅ Tempo total de execução exibido  
- ✅ Resultado salvo automaticamente com nome único  
- ✅ Abertura automática dos arquivos gerados após a varredura  
- ✅ Exportação automática para **TXT**, **CSV** e **JSON**  
- ✅ Aviso visual na interface sobre os arquivos gerados  
- ✅ Filtro opcional para ocultar serviços desconhecidos  
- ✅ Visualização gráfica das portas abertas com `matplotlib`  
  - Barras azuis para portas TCP  
  - Barras verdes para portas UDP  
  - Exibição segura na thread principal do Tkinter  
- ✅ Tratamento de erros durante escaneamento e exibição de mensagens amigáveis

---

## 📈 Exemplo de Gráfico Gerado

Após o escaneamento, uma janela será exibida com um gráfico de barras:

- **Eixo X**: portas abertas encontradas  
- **Eixo Y**: presença visual (valor fixo)  
- **Cores**: azul para TCP, verde para UDP

Ideal para identificar rapidamente os serviços ativos e comparar escaneamentos.

---

## 🖥️ Exemplos de Uso

### Escanear localhost (TCP)

```bash
python utils.py
# IP: 127.0.0.1
# Tipo: TCP
```

### Escanear roteador local (UDP)

```bash
python utils.py
# IP: 192.168.0.1
# Tipo: UDP
```

### Escanear site público (TCP)

```bash
python utils.py
# IP: google.com
# Tipo: TCP
```

---

## 📋 Saída Esperada

```text
🔍 Escaneando 8.8.8.8 (UDP)...

⏱️ Tempo: 1.87s | Média por porta: 0.0018s
 Porta 53/UDP: DNS
 --> Banner: resposta DNS decodificada...

📁 Resultados salvos em TXT, CSV e JSON na pasta atual.
Gráfico gerado com visualização das portas abertas.
```

---

## 📁 Estrutura do Projeto

``` -
port-scanner/
│
├── scanner.py                         # Lógica principal do escaneamento
├── utils.py                           # Interface gráfica com Tkinter
├── resultado_scan_"host_data".txt     # Arquivos gerados com os resultados
├── resultado_scan_"host_data".csv     # Exportação em CSV
├── resultado_scan_"host_data".json    # Exportação em JSON
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
