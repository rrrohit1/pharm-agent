import os
import gradio as gr
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL")

# Initialize client (non-Vertex mode)
client = genai.Client(api_key=API_KEY)


def call_gemini(prompt: str) -> str:
    if not API_KEY:
        return "Error: GEMINI_API_KEY not set."

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 512,
            }
        )
        return response.text

    except Exception as e:
        return f"Request error: {e}"


def respond(message, chat_history):
    user_msg = message.strip()
    if not user_msg:
        return chat_history, ""

    chat_history = chat_history or []

    assistant = call_gemini(user_msg)

    chat_history.append(
        gr.ChatMessage(role="user", content=user_msg)
    )
    chat_history.append(
        gr.ChatMessage(role="assistant", content=assistant)
    )

    return chat_history, ""


with gr.Blocks() as demo:
    gr.Markdown("# Gemini Chat (Local API)")
    chatbot = gr.Chatbot(label="Conversation")

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your message and press Enter")
        send = gr.Button("Send")


    txt.submit(respond, [txt, chatbot], [chatbot, txt])
    send.click(respond, [txt, chatbot], [chatbot, txt])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)