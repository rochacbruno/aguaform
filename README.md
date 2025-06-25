# 🌊 AguaForm

AguaForm é uma ferramenta visual para deploy de containers usando Terraform e CDKTF. Com uma interface web amigável baseada em Gradio, você pode facilmente configurar e executar deploys de aplicações containerizadas.

## ✨ Funcionalidades

- 🖥️ Interface web intuitiva baseada em Gradio
- 🐳 Suporte para Docker containers
- 🏗️ Integração com Terraform via CDKTF
- 📦 Três tipos de aplicação: API, Worker e Service
- ⚙️ Configuração flexível de portas e imagens

## 🚀 Instalação

### Pré-requisitos

- Python 3.13+
- [UV](https://docs.astral.sh/uv/) para gerenciamento de dependências
- [Terraform](https://www.terraform.io/) instalado e disponível no PATH
- Docker (para provider Docker)

### Instalação das dependências

```bash
uv install
```

## 💻 Uso

### Iniciando a aplicação

```bash
uv run aguaform <host> <porta>
```

**Exemplo:**
```bash
uv run aguaform 0.0.0.0 8080
```

Após executar o comando, acesse `http://localhost:8080` no seu navegador.

### Interface do usuário

A interface apresenta um formulário com os seguintes campos:

- **Nome**: Nome do projeto/container
- **Provider**: Escolha entre `docker` ou `aws`
- **Nginx Image**: Imagem Docker a ser utilizada (padrão: `nginx:latest`)
- **Porta Interna**: Porta interna do container (padrão: `80`)
- **Porta Externa**: Porta externa para exposição (padrão: `8080`)
- **Aplicação**: Tipo de aplicação - `api`, `worker` ou `service`

### Tipos de aplicação

- **API**: Configurada para aplicações web/REST APIs
- **Worker**: Para aplicações que processam tarefas em background
- **Service**: Para serviços gerais

## 🏗️ Arquitetura

O projeto é estruturado da seguinte forma:

```
src/aguaform/
├── __init__.py      # Aplicação principal com interface Gradio
└── stacks.py        # Classes TerraformStack (Api, Worker, Service)
```

### Classes TerraformStack

Cada tipo de aplicação possui sua própria classe que herda de `BaseTerraformStack`:

- `Api`: Adiciona configurações específicas para APIs
- `Worker`: Configurações otimizadas para workers
- `Service`: Configurações gerais para serviços

## 🔧 Desenvolvimento

### Estrutura do projeto

- **`src/aguaform/__init__.py`**: Contém a aplicação principal Gradio e lógica de deploy
- **`src/aguaform/stacks.py`**: Define as classes TerraformStack para diferentes tipos de aplicação
- **`pyproject.toml`**: Configuração do projeto e dependências

### Dependências principais

- `gradio`: Interface web
- `cdktf`: Cloud Development Kit for Terraform
- `cdktf-cdktf-provider-docker`: Provider Docker para CDKTF

## 📝 Exemplo de uso

1. Execute o AguaForm:
   ```bash
   uv run aguaform 0.0.0.0 8080
   ```

2. Acesse `http://localhost:8080`

3. Preencha o formulário:
   - Nome: `minha-api`
   - Provider: `docker`
   - Nginx Image: `nginx:alpine`
   - Porta Interna: `80`
   - Porta Externa: `3000`
   - Aplicação: `api`

4. Clique em "🚀 Executar Deploy"

5. Aguarde o resultado do deploy na seção de saída

## ⚠️ Requisitos do sistema

- Terraform deve estar instalado e acessível via linha de comando
- Docker deve estar rodando (para deploys com provider Docker)
- Permissões adequadas para criação e execução de containers

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.
