Sim, entendi. O problema foi que, dentro do README, existem blocos com ``` e isso “quebra” a caixinha principal.

Agora vou colocar **tudo dentro de um único bloco**, usando uma caixinha maior com ````markdown.

Copia **tudo** abaixo:

````markdown
# DocMind AI

DocMind AI é uma API de Inteligência Artificial baseada em RAG (Retrieval-Augmented Generation), criada para responder perguntas sobre documentos PDF enviados pelo usuário.

O sistema permite fazer upload de um PDF, extrair o texto do documento, dividir o conteúdo em chunks, gerar embeddings, armazenar as informações em um banco vetorial e responder perguntas usando um modelo de linguagem.

---

## Objetivo do Projeto

O objetivo deste projeto é construir um assistente inteligente capaz de responder perguntas com base no conteúdo de documentos enviados pelo usuário.

Esse projeto foi desenvolvido com foco em aprendizado prático de:

- RAG
- NLP
- Embeddings
- Banco vetorial
- FastAPI
- Docker
- Organização modular de projetos de IA
- Construção de APIs para aplicações com modelos de linguagem

---

## O que é RAG?

RAG significa Retrieval-Augmented Generation.

Em português, pode ser entendido como geração aumentada por recuperação de informação.

O funcionamento básico é:

1. O usuário envia um documento.
2. O sistema extrai o texto.
3. O texto é dividido em pequenos blocos chamados chunks.
4. Cada chunk é transformado em embedding.
5. Os embeddings são salvos em um banco vetorial.
6. Quando o usuário faz uma pergunta, o sistema busca os chunks mais relevantes.
7. O modelo de linguagem gera uma resposta usando apenas o contexto encontrado.

---

## Fluxo do Projeto

```text
PDF
↓
Extração de texto
↓
Divisão em chunks
↓
Criação de embeddings
↓
Armazenamento no ChromaDB
↓
Pergunta do usuário
↓
Busca semântica
↓
Geração da resposta
↓
Resposta com fontes
```

---

## Tecnologias Utilizadas

- Python
- FastAPI
- Uvicorn
- PyPDF
- LangChain Text Splitters
- Sentence Transformers
- ChromaDB
- Hugging Face Transformers
- FLAN-T5
- PyTorch
- Docker

---

## Funcionalidades

- Upload de arquivos PDF
- Extração automática de texto
- Divisão do texto em chunks
- Criação de embeddings
- Armazenamento no ChromaDB
- Busca semântica nos documentos
- Geração de respostas com modelo de linguagem
- Retorno das fontes utilizadas na resposta
- Filtro por `document_id`
- API documentada com Swagger
- Execução com Docker

---

## Estrutura do Projeto

```text
docmind-ai/
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── vectorstore/
│   └── .gitkeep
│
├── src/
│   ├── api/
│   │   └── main.py
│   │
│   ├── embeddings/
│   │   ├── create_embeddings.py
│   │   └── index_documents.py
│   │
│   ├── generation/
│   │   └── answer_generation.py
│   │
│   ├── ingestion/
│   │   ├── load_documents.py
│   │   └── split_documents.py
│   │
│   └── retrieval/
│       └── retriever.py
│
├── tests/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Como Funciona

### 1. Upload do PDF

O usuário envia um arquivo PDF pelo endpoint `/upload`.

O sistema salva o arquivo localmente, extrai o texto, divide o conteúdo em chunks e indexa os dados no ChromaDB.

Cada documento recebe um `document_id`, que pode ser usado depois para fazer perguntas especificamente sobre aquele PDF.

---

### 2. Extração de Texto

A extração é feita com `pypdf`.

O sistema percorre as páginas do PDF e junta o conteúdo textual em uma única string.

---

### 3. Divisão em Chunks

O texto extraído é dividido em partes menores usando `RecursiveCharacterTextSplitter`.

Isso é necessário porque documentos inteiros podem ser grandes demais para serem enviados diretamente ao modelo.

---

### 4. Criação de Embeddings

Cada chunk é transformado em um vetor numérico usando o modelo:

```text
all-MiniLM-L6-v2
```

Esses vetores representam semanticamente o conteúdo do texto.

Textos com significados parecidos ficam próximos no espaço vetorial.

---

### 5. Banco Vetorial

Os embeddings são armazenados no ChromaDB.

Cada chunk salvo contém:

- texto original
- embedding
- `source`
- `document_id`
- `chunk_id`

---

### 6. Busca Semântica

Quando o usuário faz uma pergunta, o sistema transforma essa pergunta em embedding e busca os chunks mais parecidos no ChromaDB.

Também é possível filtrar a busca por `document_id`.

---

### 7. Geração da Resposta

Os chunks encontrados são enviados como contexto para um modelo de linguagem.

O modelo usado é:

```text
google/flan-t5-base
```

O modelo gera uma resposta com base apenas nas informações recuperadas do documento.

---

## Endpoints da API

### GET `/`

Verifica se a API está online.

Resposta esperada:

```json
{
  "message": "DocMind AI API online",
  "description": "Sistema RAG para perguntas e respostas sobre documentos"
}
```

---

### GET `/health`

Endpoint simples para verificar o status da aplicação.

Resposta esperada:

```json
{
  "status": "ok"
}
```

---

### POST `/upload`

Faz upload de um PDF e indexa o documento.

Exemplo de resposta:

```json
{
  "message": "PDF enviado e indexado com sucesso",
  "file_name": "documento.pdf",
  "document_id": "2bacf6e5-2e61-4357-b441-43df67dc7f24",
  "chunks_indexed": 3
}
```

---

### POST `/ask`

Faz uma pergunta sobre um documento.

Exemplo de entrada:

```json
{
  "question": "Quais informações aparecem no documento?",
  "n_results": 1,
  "document_id": "2bacf6e5-2e61-4357-b441-43df67dc7f24"
}
```

Exemplo de resposta:

```json
{
  "question": "Quais informações aparecem no documento?",
  "answer": "- Resposta gerada com base no conteúdo recuperado.",
  "sources": [
    {
      "source": "data/raw/documento.pdf",
      "document_id": "2bacf6e5-2e61-4357-b441-43df67dc7f24",
      "chunk_id": 0,
      "distance": 0.70,
      "preview": "Trecho do documento usado como fonte..."
    }
  ],
  "model": "google/flan-t5-base",
  "document_id": "2bacf6e5-2e61-4357-b441-43df67dc7f24"
}
```

---

## Como Rodar Localmente

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

### 2. Entrar na pasta do projeto

```bash
cd docmind-ai
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 5. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Rodar a API

```bash
python -m uvicorn src.api.main:app --reload
```

### 7. Abrir a documentação

```text
http://127.0.0.1:8000/docs
```

---

## Como Rodar com Docker

### 1. Build da imagem

```bash
docker build -t docmind-api .
```

### 2. Rodar o container

```bash
docker run -p 8000:8000 docmind-api
```

### 3. Abrir a API

```text
http://127.0.0.1:8000/docs
```

---

## Exemplo de Uso

### Passo 1: Enviar PDF

Acesse o Swagger:

```text
http://127.0.0.1:8000/docs
```

Use o endpoint:

```text
POST /upload
```

Envie um arquivo PDF.

Copie o `document_id` retornado.

---

### Passo 2: Fazer uma pergunta

Use o endpoint:

```text
POST /ask
```

Exemplo:

```json
{
  "question": "Quais tecnologias são mencionadas no documento?",
  "n_results": 1,
  "document_id": "COLE_O_DOCUMENT_ID_AQUI"
}
```

---

## Por que usar document_id?

O `document_id` permite perguntar sobre um documento específico.

Sem ele, o sistema pode buscar informações em todos os documentos indexados no banco vetorial.

Com ele, o sistema filtra a busca para apenas um PDF.

Isso deixa o projeto mais próximo de uma aplicação real.

---

## Demonstração

Crie uma pasta chamada `assets/` e adicione prints do projeto.

Sugestão de imagens:

```text
assets/swagger.png
assets/upload.png
assets/ask.png
assets/docker.png
```

Depois, adicione as imagens no README:

```markdown
### Swagger

![Swagger](assets/swagger.png)

### Upload de PDF

![Upload](assets/upload.png)

### Pergunta com RAG

![Ask](assets/ask.png)

### Docker

![Docker](assets/docker.png)
```

---

## Observação sobre os dados

Os arquivos PDF enviados para teste não são versionados no GitHub.

A pasta `data/raw/` está no `.gitignore` para evitar o envio de documentos pessoais ou sensíveis.

O banco vetorial local também não é versionado:

```text
vectorstore/
```

Assim, o usuário pode clonar o projeto, rodar a API e fazer upload dos próprios documentos.

---

## Aprendizados

Durante o desenvolvimento deste projeto, foram trabalhados conceitos como:

- RAG
- NLP
- embeddings
- busca semântica
- banco vetorial
- extração de texto de PDFs
- criação de APIs com FastAPI
- upload de arquivos
- filtro por documento usando `document_id`
- uso de modelos da Hugging Face
- organização modular de código
- Dockerização de aplicações de IA

---

## Desafios Encontrados

Alguns desafios enfrentados durante o projeto:

- lidar com texto extraído de PDFs de forma pouco estruturada
- melhorar a qualidade das respostas geradas
- ajustar prompts para diferentes tipos de pergunta
- lidar com múltiplos documentos no banco vetorial
- adicionar filtro por `document_id`
- containerizar uma aplicação com dependências pesadas de IA

---

## Próximas Melhorias

- Criar interface com Streamlit
- Melhorar limpeza do texto extraído
- Adicionar suporte para arquivos `.txt` e `.docx`
- Criar testes com pytest
- Adicionar Docker Compose
- Melhorar avaliação das respostas
- Implementar histórico de perguntas
- Fazer deploy em cloud
- Adicionar autenticação
- Permitir múltiplos usuários
- Criar dashboard de uso dos documentos

---

## Status do Projeto

Projeto funcional.

A aplicação já permite:

- enviar documentos PDF
- indexar documentos
- fazer perguntas sobre documentos
- recuperar fontes
- filtrar por documento
- rodar via API
- rodar com Docker

---

## Resumo Final

O DocMind AI é um projeto prático de IA Generativa com RAG.

Ele mostra como transformar documentos em uma base consultável por IA, combinando embeddings, banco vetorial, busca semântica, geração de texto, API e Docker.

Este projeto representa uma evolução em relação a projetos tradicionais de Machine Learning, pois se aproxima mais de uma aplicação real de IA usada em produtos modernos.
````
