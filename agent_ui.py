import requests
import gradio as gr

OLLAMA_URL = "http://localhost:11434/api/generate"

def chat_with_agent(prompt):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()
    return result.get("response", "").strip()

# Create Gradio interface
iface = gr.Interface(
    fn=chat_with_agent,
    inputs=gr.Textbox(lines=4, placeholder="Ask me anything..."),
    outputs="text",
    title="🧠 Local AI Agent",
    description="Powered by Mistral via Ollama. Runs entirely on your machine."
)

iface.launch()
