# Port Scanner Python - Scanner de Portas TCP

Um scanner de portas TCP simples e eficiente escrito em Python que utiliza multi-threading para escanear portas em hosts remotos ou locais.

## 📋 Descrição

Este programa escaneia portas TCP em um host específico para identificar quais portas estão abertas. É útil para:
- Testes de segurança em sua própria rede
- Verificação de serviços em execução
- Diagnóstico de problemas de conectividade
- Aprendizado sobre redes e segurança

## 🚀 Instalação

### Pré-requisitos
- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (usa apenas bibliotecas padrão do Python)

### Verificar Python
```bash
python --version
# ou
python3 --version
```

## 🎯 Como Usar

### 1. Executar o scanner
```bash
python scanner.py
```

### 2. O programa solicitará:
```
Digite o IP ou domínio para escanear: [digite o host]
```

### 3. Exemplos de entrada:
- IP local: `127.0.0.1`
- IP de rede: `192.168.1.1`
- Domínio: `google.com` ou `localhost`
- Site: `example.com`

## 📊 Funcionalidades

- ✅ **Multi-threading**: Escanear múltiplas portas simultaneamente
- ✅ **Timeout configurável**: 1 segundo por porta
- ✅ **Range de portas**: 1-1024 (padrão)
- ✅ **Feedback em tempo real**: Mostra portas abertas conforme são encontradas
- ✅ **Contador de tempo**: Mostra tempo total de execução
- ✅ **Tratamento de erros**: Graceful handling de timeouts e erros de conexão

## 🔧 Personalização

### Alterar range de portas
Edite as variáveis no código:
```python
start_port = 1      # Porta inicial
end_port = 1024     # Porta final
```

### Alterar timeout
Edite a linha:
```python
sock.settimeout(1)  # Tempo em segundos
```

## 🖥️ Exemplos de Uso

### 1. Escanear localhost
```bash
python scanner.py
# Digite: 127.0.0.1
```

### 2. Escanear roteador local
```bash
python scanner.py
# Digite: 192.168.1.1
```

### 3. Escanear site
```bash
python scanner.py
# Digite: google.com
```

### 4. Escanear com IP específico
```bash
python scanner.py
# Digite: 8.8.8.8
```

## 📋 Saída Esperada

```
Iniciando varredura em google.com...

[+] Porta 80 aberta
[+] Porta 443 aberta

Varredura concluída em 2.34 segundos.


```

## 📁 Estrutura do Projeto

port-scanner/
│
├── .qodo/                    # Diretório do projeto
│   ├── scanner.py           # Arquivo principal do scanner
│   ├── utils.py             # Utilitários auxiliares
│   └── README.md            # Este arquivo de documentação


```

## ⚠️ Avisos Importantes

### Uso Responsável
- **Use apenas em redes que você possui ou tem permissão para testar**
- **Não use para atividades maliciosas**

## 👨‍💻 Autor

Murilo Vinícius de Faveri — projeto para estudo de programação e cibersegurança.

---



