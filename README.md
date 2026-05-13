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
