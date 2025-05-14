import gradio as gr
import os
import json
from mindmate_chatbot import MindMateBot
import random
import time

# Styling constants
PRIMARY_COLOR = "#1F77B4"  # Strong blue, professional look
SECONDARY_COLOR = "#F5F5F5"  # Light gray for backgrounds
TEXT_COLOR = "#2C3E50"  # Dark blue-gray for text

# Create custom CSS
custom_css = f"""
.container {{
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: {SECONDARY_COLOR};
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}}

.header {{
    text-align: center;
    margin-bottom: 20px;
    color: {TEXT_COLOR};
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 5px;
}}

.chat-container {{
    background-color: white;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
}}

.message-user {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border-radius: 18px 18px 0 18px;
    padding: 10px 15px;
    margin: 5px 0;
    max-width: 80%;
    float: right;
    clear: both;
}}

.message-bot {{
    background-color: #E8E8E8;
    color: {TEXT_COLOR};
    border-radius: 18px 18px 18px 0;
    padding: 10px 15px;
    margin: 5px 0;
    max-width: 80%;
    float: left;
    clear: both;
}}

.input-area {{
    background-color: white;
    border-radius: 8px;
    padding: 10px;
}}

.footer {{
    text-align: center;
    font-size: 0.8rem;
    color: gray;
    margin-top: 20px;
}}

.disclaimer {{
    background-color: #FFF3CD;
    border-left: 5px solid #FFD700;
    padding: 10px 15px;
    margin: 15px 0;
    font-size: 0.9rem;
}}
"""

# Load or initialize the chatbot
bot = MindMateBot("training_data.json")

# Check for crisis keywords
def check_for_crisis(message):
    crisis_keywords = ["suicide", "kill myself", "end my life", "don't want to live", "better off dead"]
    return any(keyword in message.lower() for keyword in crisis_keywords)

# Helper function to make responses more conversational
def make_more_conversational(response, message):
    # Add conversation fillers and personalization
    conversational_openers = [
        "",  # sometimes keep it simple
        "I hear you. ",
        "I understand. ",
        "That's interesting. ",
        "Thanks for sharing that. ",
        "I appreciate your openness. "
    ]
    
    conversational_closers = [
        "",
        " How does that sound?",
        " What do you think about that?",
        " Does that make sense?",
        " Would you like to tell me more?",
        " How are you feeling about this?"
    ]
    
    therapeutic_phrases = [
        "As your health companion, I want to understand better. ",
        "From a therapeutic perspective, ",
        "It sounds like you're experiencing ",
        "Many people feel similar things. ",
        "Let's explore this together. "
    ]
    
    # Don't add conversational elements to already conversational responses
    if len(response.split()) > 12 and not any(phrase in response.lower() for phrase in ["how are you", "how do you feel", "what do you think"]):
        # 30% chance to add a therapeutic phrase if message seems emotional or health-related
        health_keywords = ["pain", "feeling", "doctor", "sick", "hurt", "tired", "stress", "anxiety", "depression"]
        if any(keyword in message.lower() for keyword in health_keywords) and random.random() < 0.3:
            response = random.choice(therapeutic_phrases) + response
        else:
            response = random.choice(conversational_openers) + response
        
        # Only add a closer if the response doesn't already end with a question
        if not response.rstrip().endswith("?"):
            # 40% chance to add a conversational closer
            if random.random() < 0.4:
                response = response.rstrip() + random.choice(conversational_closers)
    
    return response

# Chat function that processes messages and returns bot responses
def chat(message, history):
    if message == "":
        return history
    
    # Check for crisis keywords
    if check_for_crisis(message):
        bot_response = bot.get_crisis_response()
    else:
        # Process the user message
        bot_response = bot.process_input(message)
        
        # Make responses more conversational
        bot_response = make_more_conversational(bot_response, message)
    
    # Add the message and response to history
    history = history + [(message, bot_response)]
    return history

# Create blocks for custom layout
with gr.Blocks(css=custom_css) as demo:
    # Header section
    with gr.Row():
        with gr.Column():
            gr.HTML("""
            <div class="header">
                <h1>MindMate</h1>
                <p>Your friendly AI health companion and therapeutic friend</p>
            </div>
            """)

    # Main chat interface
    with gr.Row():
        with gr.Column():
            # Simple chatbot implementation
            chatbot = gr.Chatbot(
                value=[
                    (None, "Hi there! I'm MindMate, your friendly health companion and therapeutic friend. How are you feeling today?")
                ],
                height=500,
                elem_id="chat-box"
            )
            
            # Message input
            msg = gr.Textbox(
                placeholder="Type your message here...",
                lines=2,
                label="",
                elem_id="input-box"
            )
            
            # Clear button
            clear = gr.Button("Clear conversation")
            
            # Set up the event handlers
            msg.submit(chat, [msg, chatbot], chatbot).then(
                lambda: "", None, msg
            )
            
            clear.click(lambda: [], None, chatbot)

            # Disclaimer
            gr.HTML("""
            <div class="disclaimer">
                <strong>Important:</strong> I'm an AI companion designed to provide supportive conversations about your health and wellbeing.
                While I can offer a friendly chat and information, I'm not a licensed healthcare professional. If you're experiencing a health crisis or need
                professional help, please contact a healthcare provider.
            </div>
            """)

    # Footer
    with gr.Row():
        with gr.Column():
            gr.HTML("""
            <div class="footer">
                <p>MindMate is designed with privacy in mind. Your conversations are processed locally and not stored or shared with third parties.</p>
                <p>© 2023 MindMate - Your friendly health companion and therapeutic friend</p>
            </div>
            """)

# Launch the app
if __name__ == "__main__":
    demo.queue().launch()