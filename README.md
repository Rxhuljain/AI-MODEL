# MindMate: Friendly Health & Wellness Companion

MindMate is a conversational AI companion designed for health and wellness discussions. It provides supportive conversations and information about various health topics in a friendly, accessible way.

## Features

- **Conversational & Friendly**: Natural dialog that feels like chatting with a supportive friend
- **Health & Wellness Focus**: Discusses various health topics, mental wellbeing, and lifestyle factors
- **Adaptive Communication**: Adjusts conversation style based on user preferences and interaction patterns
- **Supportive Responses**: Offers acknowledgment, empathy, and encouragement during conversations
- **Risk Assessment**: Monitors for crisis indicators and provides appropriate resources when needed

## Running MindMate

MindMate uses a web interface built with Gradio for an intuitive, user-friendly experience.

### Installation and Setup

1. Install the required packages:
```bash
pip install gradio requests
```

2. Run the application:
```bash
python3 mindmate_api.py
```

3. Open the URL shown in the terminal (usually http://127.0.0.1:7860) in your web browser

## How it Works

MindMate combines multiple components:

1. **Conversational Engine**: Creates a natural dialog flow with acknowledgments, follow-up questions, and empathetic responses
2. **Comprehensive Knowledge Base**: Contains information on various health and wellness topics
3. **Adaptive Conversation Style**: Adjusts to user preferences and conversational context

## Conversation Features

MindMate uses several techniques to create a more natural conversational experience:

- **Personalized Greetings**: Welcomes users with friendly, personalized messages
- **Acknowledgment Phrases**: Shows understanding and appreciation for what users share
- **Follow-up Questions**: Keeps the conversation flowing naturally
- **Empathetic Responses**: Recognizes emotional context and responds appropriately
- **Encouraging Statements**: Offers positive reinforcement and support

## Important Notes

- MindMate is not a replacement for professional healthcare
- For health concerns, always consult with qualified healthcare providers
- For crisis situations, contact appropriate emergency services or crisis helplines

## Development

The project consists of several key files:

- `mindmate_chatbot.py`: Core conversational engine with health knowledge
- `training_data.json`: Training data with patterns, responses, and resources
- `app.py`: Gradio web interface

## License

This project is licensed under the MIT License. 