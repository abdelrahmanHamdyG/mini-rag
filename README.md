# mini-rag

A lightweight implementation of Retrieval-Augmented Generation (RAG) designed for question answering systems.

## Overview

This project provides a foundational backend service for building RAG-based applications. It leverages FastAPI, LangChain, and MongoDB to store, index, and retrieve documents, enabling semantic search and enhanced LLM-based responses.

## Requirements

- Python 3.8 or newer
- Docker
- MongoDB

## Setup Instructions

### 1. Python Environment

We recommend using MiniConda:

```bash
# Create a new conda environment
conda create -n mini-rag python=3.8
conda activate mini-rag
```

### 2. Improve CLI Readability (Optional)

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy and customize the environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file to include your settings, such as `OPENAI_API_KEY`.

### 5. Run with Docker Compose

```bash
cd docker
cp .env.example .env
# Update credentials in .env
sudo docker compose up -d
```

### 6. Start the FastAPI Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

```

## Technologies Used

- **FastAPI** – Web framework
- **MongoDB** – NoSQL database for storing documents and metadata
- **LangChain** – Framework for chaining LLMs with retrieval components
- **Docker** – Containerized development and deployment
