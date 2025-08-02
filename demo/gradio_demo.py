import requests
import gradio as gr
import json

API_URL = "http://localhost:8000/chat"
WELCOME_MSG = ("🌏 Welcome! I’m your AI travel assistant. "
               "Ask me about any city for tips, weather, time, or fun facts!")


def travel_chat(user_message, history):
    """
    Sends the user message to the API and returns the chat history with pretty formatting.
    """
    payload = {"message": user_message}
    try:
        resp = requests.post(API_URL, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Pretty-format the result for display
        thinking = data.get("thinking", "")
        function_calls = data.get("function_calls", [])
        response = data.get("response", "")
        reply = ""
        if thinking:
            reply += f"**🤔 Thinking:**\n{thinking}\n\n"
        if function_calls:
            reply += "**🛠️ Tool Calls:**\n"
            for fc in function_calls:
                reply += f"- `{fc['tool']}` with {json.dumps(fc['parameters'])}\n"
            reply += "\n"
        if response:
            reply += f"**📢 Response:**\n{response}"
        else:
            reply += "_No response generated._"
    except Exception as e:
        reply = f"❌ API Error: {e}"
    history = history or []
    history.append((user_message, reply))
    return history, history, ""


def clear_history():
    """Resets chat history to initial welcome message."""
    return [(None, WELCOME_MSG)], [(None, WELCOME_MSG)]


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌏 AI Travel Assistant Chat")
    chatbot = gr.Chatbot(
        value=[(None, WELCOME_MSG)],
        label="Travel Chat",
        type="tuples",
    )
    msg = gr.Textbox(placeholder="Ask me about any city...", label="Your Message")
    clear = gr.Button("Clear")
    state = gr.State([(None, WELCOME_MSG)])

    msg.submit(travel_chat, [msg, state], [chatbot, state, msg])
    clear.click(clear_history, [], [chatbot, state])

demo.launch()
