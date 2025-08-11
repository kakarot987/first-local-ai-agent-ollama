# 🧠 Local AI Chatbot with Gradio + Ollama + Mistral

This project is a lightweight, privacy-first chatbot interface powered by the Mistral language model running locally via Ollama, with a sleek frontend built using Gradio. Everything runs on your machine — no cloud calls, no data sharing.

It’s designed for developers and AI enthusiasts who want fast, secure, and offline access to powerful language models.

## 🚀 Features

This chatbot offers fully local execution, meaning no internet is required after setup. It’s powered by the Mistral model via Ollama, and features a simple and intuitive Gradio UI. You’ll experience fast response times with zero latency from external APIs.

## 🛠️ Requirements

To get started, you’ll need Python 3.8 or higher, Ollama installed and running locally, and the Mistral model pulled via Ollama. You can do that by running:

```bash
ollama pull mistral
Then install the required Python packages:

bash
pip install gradio requests
📦 Installation
Clone the repository:

bash
git clone https://github.com/your-username/local-ai-chatbot.git
cd local-ai-chatbot
Install dependencies:

bash
pip install -r requirements.txt
Ensure Ollama is running:

bash
ollama run mistral
Launch the app:

bash
python app.py
💡 How It Works
The user enters a prompt in the Gradio UI. That prompt is sent to a Python function, which calls Ollama’s local API. Ollama uses the Mistral model to generate a response, which is then returned and displayed in the UI.

Architecture Flow
User → Gradio UI → Python Function → Ollama API → Mistral Model → Response → Gradio UI

📂 File Structure
The project is simple and minimal:

app.py: Main application script

README.md: Project documentation

requirements.txt: Python dependencies

🧪 Example Prompt
Try asking: "Explain how transformers work in simple terms."

You’ll get a response like: "Transformers are neural networks that use attention mechanisms to understand relationships between words in a sentence..."

🧱 Built With
Gradio for the UI

Ollama for local model serving

Mistral as the language model

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.