# 🌏 City Information Assistant API

A modern AI system that turns natural language queries into city insights and travel recommendations—using OpenAI Agents, tool orchestration, and real-time APIs.

---

[![Try it Online](https://img.shields.io/badge/Live%20Demo-Gradio-blue?logo=gradio\&logoColor=white)](https://your-gradio-link.here)

![City Assistant Demo](demo/demo.gif)

---

## 📚 Documentation

- [How It Works](https://github.com/Benybrahim/city-information-agent/wiki/How-It-Works)
- [API Overview](https://github.com/Benybrahim/city-information-agent/wiki/API-Reference)
- [Agents Overview](https://github.com/Benybrahim/city-information-agent/wiki/Agents)
- [Tools Overview](https://github.com/Benybrahim/city-information-agent/wiki/Tools)

---

## ✨ Features

* Natural-language chat about any city in the world
* Real-time **weather**, **local time**, and **facts**—via OpenAI tool calls
* Multi-turn travel planning and follow-up discussion
* Modular agent architecture (orchestration + tools)
* Robust API with error handling and clear JSON responses

---

## 📝 Requirements

* [![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/doc/)
  **Python 3.9 or higher**
  [Python Docs](https://docs.python.org/3/)

* [![uv](https://img.shields.io/badge/uv-Package_Manager-orange?logo=python)](https://github.com/astral-sh/uv)
  **uv** (fastest Python package manager)
  [uv Docs](https://github.com/astral-sh/uv)

* [![OpenAI](https://img.shields.io/badge/OpenAI%20Agents-SDK-blueviolet?logo=openai)](https://github.com/openai/openai-agents-python)
  **OpenAI Agents SDK**
  [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/)

* [![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?logo=fastapi)](https://fastapi.tiangolo.com/)
  **FastAPI**
  [FastAPI Docs](https://fastapi.tiangolo.com/)

* [![Docker](https://img.shields.io/badge/Docker-Required-blue?logo=docker)](https://docs.docker.com/get-docker/)
  **Docker** (for container deployment)
  [Docker Docs](https://docs.docker.com/)

---

## 🚀 Quick Start

1. **Install dependencies**

   ```bash
   uv pip install -r requirements.txt
   ```

2. Add `.env` to the repo for API Keys.

3. **Run the API server**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **POST `/chat` request**

   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "Tell me about Kyoto"}' \
     http://localhost:8000/chat
   ```

---

## 🔗 API Usage

### **POST** `/chat`

* **Request:**

  ```json
  {"message": "Tell me about Kyoto"}
  ```

* **Sample Response:**

  ```json
  {
    "thinking": "I'll get facts, weather, and time for Kyoto.",
    "function_calls": [
      {"tool": "city_facts_tool", "parameters": {"city": "Kyoto"}},
      {"tool": "weather_tool", "parameters": {"city": "Kyoto"}},
      {"tool": "time_tool", "parameters": {"city": "Kyoto"}}
    ],
    "response": "Kyoto was once the capital of Japan. It's 27°C and clear. The local time is 11:14. Want trip suggestions?"
  }
  ```

---

## 🧪 Testing

Run all tests with:

  ```bash
    pytest
  ```

---

## 🐳 Running with Docker

Build and run using Docker Compose:

  ```bash
    docker compose up --build
  ```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## 🖥️ Interactive UI Demo

1. **Run API Server**

   ```bash
   uvicorn app.main:app --reload
   ```
2. **Run Gradio Demo**

   ```bash
   python demo/gradio_demo.py
   ```

The UI will be available at [http://localhost:7860](http://localhost:7860).