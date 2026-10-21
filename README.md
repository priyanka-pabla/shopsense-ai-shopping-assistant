# ShopSense AI — Intelligent Shopping Assistant

ShopSense AI is an AI-powered shopping assistant designed to help customers discover products through natural language conversations.

The application provides personalized product recommendations based on customer preferences, product information, and budget constraints.

Built using Python, OpenAI, and Streamlit, ShopSense demonstrates how conversational AI can enhance the online shopping experience.

## Live Demo

🚀 [Try ShopSense AI](https://shopsense-ai-shopping-assistant-kwrqswa7o2hg4oj74v3mh7.streamlit.app/)

Explore personalized product recommendations, conversational shopping, and budget-aware suggestions through the interactive demo.

## Key Features

- **Conversational AI:** Understands customer queries expressed in natural language.
- **Personalized Recommendations:** Suggests products based on customer needs and preferences.
- **Budget-Aware Recommendations:** Evaluates recommended products against the customer's budget.
- **Product Validation:** Checks AI-generated recommendations against the available product catalog.
- **Structured AI Responses:** Uses structured outputs for consistent recommendation processing.
- **Interactive Web Interface:** Provides a customer-facing shopping experience using Streamlit.

## Technology Stack

- **Python** — Core application development
- **OpenAI API (GPT-4.1-mini)** — Conversational AI and product recommendations
- **Pydantic** — Structured AI response validation
- **Streamlit** — Interactive web interface
- **JSON** — Product catalog storage
- **Git & GitHub** — Version control and project management

## Project Architecture

ShopSense AI follows a modular architecture that separates the user interface, AI recommendation logic, and product data.

- `streamlit_app.py` — Customer-facing web interface.
- `src/chatbot.py` — AI conversation handling, product recommendations, and validation logic.
- `data/products.json` — Structured product catalog.
- `app.py` — Python application entry point.
- `requirements.txt` — Project dependencies.

### Recommendation Workflow

1. Customer submits a shopping query.
2. OpenAI processes the conversation and generates structured recommendations.
3. The application validates recommended products against the catalog.
4. Budget validation checks the total recommendation cost against the customer's budget.
5. The application presents the recommendations through Streamlit.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/priyanka-pabla/shopsense-ai-shopping-assistant.git
cd shopsense-ai-shopping-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Never commit your actual API key to GitHub.

### 4. Run the application

```bash
streamlit run streamlit_app.py
```