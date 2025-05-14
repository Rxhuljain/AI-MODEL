from flask import Flask, request, jsonify, render_template
from mindmate_chatbot import MindMateBot
import random
import os

app = Flask(__name__)

# Load the chatbot
bot = MindMateBot("training_data.json")

# Helper function to make responses more conversational
def make_more_conversational(response, message):
    # List of query indicators that suggest the user is asking a specific question
    query_indicators = ["can you", "how do", "what is", "where is", "when is", "who is", 
                        "why is", "help me", "tell me", "number", "helpline", "contact",
                        "?", "how can", "what are", "where can", "how to"]
    
    # Check if the message contains query indicators
    is_specific_query = any(indicator in message.lower() for indicator in query_indicators)
    
    # If it's a specific query, return the response without conversational elements
    if is_specific_query:
        return response
    
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

# Check for crisis keywords
def check_for_crisis(message):
    crisis_keywords = ["suicide", "kill myself", "end my life", "don't want to live", "better off dead"]
    return any(keyword in message.lower() for keyword in crisis_keywords)

# API endpoint for chat
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"response": "Please enter a message."})
    
    # Check for crisis keywords
    if check_for_crisis(message):
        bot_response = bot.get_crisis_response()
    else:
        # Process the user message
        bot_response = bot.process_input(message)
        
        # Make responses more conversational
        bot_response = make_more_conversational(bot_response, message)
    
    return jsonify({"response": bot_response})

# Serve a simple HTML interface
@app.route('/')
def index():
    return render_template('index.html')

# Create a template directory and index.html file if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')
    
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>MindMate - Health Companion</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 20px 0;
            background-color: #1F77B4;
            color: white;
            margin-bottom: 20px;
        }
        h1 {
            margin: 0;
        }
        .chat-container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            max-height: 500px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
        }
        .user-message {
            background-color: #1F77B4;
            color: white;
            margin-left: auto;
            border-radius: 18px 18px 0 18px;
        }
        .bot-message {
            background-color: #E8E8E8;
            border-radius: 18px 18px 18px 0;
        }
        .input-container {
            display: flex;
            margin-top: 20px;
        }
        input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #1F77B4;
            color: white;
            border: none;
            border-radius: 4px;
            margin-left: 10px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1a6698;
        }
        .disclaimer {
            margin-top: 20px;
            padding: 10px 15px;
            background-color: #FFF3CD;
            border-left: 5px solid #FFD700;
            font-size: 0.9rem;
        }
        footer {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            font-size: 0.8rem;
            color: #666;
        }
    </style>
</head>
<body>
    <header>
        <h1>MindMate</h1>
        <p>Your friendly AI health companion and therapeutic friend</p>
    </header>
    
    <div class="container">
        <div class="chat-container" id="chat-container">
            <div class="message bot-message">
                Hi there! I'm MindMate, your friendly health companion and therapeutic friend. How are you feeling today?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your message here..." />
            <button id="send-button">Send</button>
        </div>
        
        <div class="disclaimer">
            <strong>Important:</strong> I'm an AI companion designed to provide supportive conversations about your health and wellbeing.
            While I can offer a friendly chat and information, I'm not a licensed healthcare professional. If you're experiencing a health crisis or need
            professional help, please contact a healthcare provider.
        </div>
        
        <footer>
            <p>MindMate is designed with privacy in mind. Your conversations are processed locally and not stored or shared with third parties.</p>
            <p>© 2023 MindMate - Your friendly health companion and therapeutic friend</p>
        </footer>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatContainer = document.getElementById('chat-container');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            
            // Send message when user clicks send button
            sendButton.addEventListener('click', sendMessage);
            
            // Send message when user presses Enter
            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            function sendMessage() {
                const message = userInput.value.trim();
                if (message === '') return;
                
                // Add user message to chat
                addMessage(message, 'user');
                
                // Clear input field
                userInput.value = '';
                
                // Send message to API
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    // Add bot response to chat
                    addMessage(data.response, 'bot');
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('Sorry, there was an error processing your message. Please try again.', 'bot');
                });
            }
            
            function addMessage(message, sender) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                messageElement.textContent = message;
                
                chatContainer.appendChild(messageElement);
                
                // Scroll to bottom of chat
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        });
    </script>
</body>
</html>
        ''')

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 