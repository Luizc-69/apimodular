# API Modular (FastAPI + SQLite) com Proxy Reverso Nginx

Este projeto implementa uma API RESTful em Python utilizando arquitetura modular (separação em `core`, `schemas`, `repositories` e `routes`) protegida por um servidor **Nginx** atuando como Proxy Reverso.

## 🏗️ Arquitetura da Aplicação

```text
[ Cliente / Navegador ] ---> Porta 8080 ---> [ Nginx (Proxy Reverso) ] ---> Porta 8000 ---> [ Uvicorn + FastAPI ] ---> [ SQLite ]
```

---

## ⚙️ Mini Tutorial: Configuração e Execução do Nginx

### 1. Pré-requisitos
* Python 3.11+ e gerenciador `uv` instalados.
* Nginx para Windows extraído na pasta `./nginx` na raiz deste projeto.

### 2. Configuração do Proxy Reverso (`nginx/conf/nginx.conf`)
Configure o bloco `server` dentro do arquivo `nginx/conf/nginx.conf` para escutar na porta **8080** e encaminhar o tráfego para a aplicação rodando na porta **8000**:

```nginx
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    server {
        listen       8080;
        server_name  localhost;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
```

### 3. Como Executar o Projeto Completo

**Passo 1 — Iniciar o Backend (FastAPI + Uvicorn):**
Na raiz do projeto, execute o servidor apontando para o módulo principal:
```powershell
uv run uvicorn app.main:app --reload
```

**Passo 2 — Iniciar o Proxy Reverso (Nginx):**
Em um segundo terminal, entre na pasta do Nginx e inicie o serviço:
```powershell
cd nginx
start nginx
```

### 4. Validação
Acesse a documentação interativa da API através da porta configurada no Nginx:
* **URL de Teste:** `http://localhost:8080/docs`

### 5. Como Encerrar os Serviços
* **Parar o Nginx:** Dentro da pasta `nginx`, execute `./nginx.exe -s stop`.
* **Parar a API:** Pressione `Ctrl + C` no terminal do Uvicorn.
