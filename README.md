# 📦 Projeto do Squad 16 - Plataforma de Cursos

Este projeto é uma aplicação web full stack que integra tecnologias modernas para garantir escalabilidade, performance e organização de código.

- O **back-end** é desenvolvido em **Python**, utilizando o **FastAPI** para criação da API REST, com gerenciamento de dependências e ambiente virtual feito via **Poetry**.
- O banco de dados está hospedado na **plataforma Neon**, um provedor de **PostgreSQL em nuvem**, que oferece escalabilidade sob demanda e fácil integração com aplicações modernas.
- O **front-end** é construído com **Next.js (React)**, permitindo rotas dinâmicas, renderização híbrida (SSR/CSR) e uma experiência fluida para o usuário.

A aplicação foi estruturada para que o frontend se comunique diretamente com o backend por meio de requisições HTTP à API FastAPI.

---

## ✅ Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Node.js (v18+ recomendado)](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

---

## ⚙️ Configuração e Execução do Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/SQUAD-SIXTEEN-JN/Projeto-JN.git
cd local-onde-clonou
```

### 2. Acessar a pasta do back-end

```bash
cd back-end
```

### 3. Instalar as dependências

```bash
poetry install
```

### 4. Ativar ambiente virtual

Em sua IDE, só basta selecionar o interpretador correspondente ao ambiente virtual do poetry. _Se caso for o VsCode, fica no canto inferior direito_

### 5. Criar o arquivo .env na pasta do back-end

| Nome               | Descrição                    |
|--------------------|------------------------------|
| `NEON_DATABASE_URL`| URL de conexão com o Neon    |
| `JWT_SECRET_KEY`   | Assinatura do jwt            |

### 6. Rodar o back-end

```bash
poetry run uvicorn app.main:app --reload
```

### 7. Acessar a pasta do front-end

```bash
cd ../front-end
```

### 8. Instalar as dependências

```bash
npm install
```

### 9. Rodar o front-end

```bash
npm run dev
```

---

## 🧩 Modelagem de Dados

A modelagem de dados do projeto foi elaborada com base em uma estrutura relacional, utilizando **PostgreSQL** como sistema de gerenciamento.

Abaixo está o diagrama ER (Entidade-Relacionamento) que representa as principais entidades e seus relacionamentos na base de dados:

![MER](https://github.com/user-attachments/assets/6fa05972-cd7b-4dfa-8568-9779d49edc2e)
