"""Gradio interface for a locally hosted Ollama model."""

import os

import gradio as gr

from ollama_client import generate


def chat_with_agent(prompt: str) -> str:
    """Turn recoverable errors into readable UI messages."""
    try:
        return generate(prompt)
    except (RuntimeError, ValueError) as exc:
        return f"Error: {exc}"


iface = gr.Interface(
    fn=chat_with_agent,
    inputs=gr.Textbox(lines=4, placeholder="Ask me anything..."),
    outputs=gr.Textbox(label="Ollama response"),
    title="Local AI Chatbot",
    description="Local Mistral inference through Ollama. No cloud API required.",
)

if __name__ == "__main__":
    iface.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
    )
