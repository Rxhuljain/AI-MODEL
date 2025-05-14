import json

# Create a sample of the provided data to demonstrate format
sample_data = {
    "intents": [
        {"tag": "greeting", 
         "patterns": ["Hi", "Hey", "Is anyone there?","Hi there", "Hello"],
         "responses": ["Hello there. Tell me how are you feeling today?", "Hi there. What brings you here today?"]
        },
        {"tag": "goodbye",
         "patterns": ["Bye", "See you later", "Goodbye"],
         "responses": ["See you later.", "Have a nice day.", "Bye! Come back again."]
        }
    ]
}

# Convert to MindMate format
mindmate_data = {}
for intent in sample_data["intents"]:
    tag = intent["tag"].lower().replace(" ", "_").replace("?", "").replace("!", "")
    patterns = intent["patterns"]
    responses = intent["responses"]
    
    mindmate_data[tag] = {
        "patterns": patterns,
        "responses": responses,
        "follow_ups": [
            "How long have you been feeling this way?",
            "Would you like to explore this topic more deeply?",
            "Have you discussed this with anyone else in your life?"
        ],
        "resources": [
            "I can provide more information on this topic if you'd like."
        ]
    }

# Save the converted data
with open("mindmate_converted_sample.json", "w") as f:
    json.dump(mindmate_data, f, indent=4)

print("""
INSTRUCTIONS:

1. Copy your intents JSON data
2. Edit this script to replace the 'sample_data' with your own data
3. Run: python convert_to_mindmate.py
4. The output will be in mindmate_converted_data.json
5. You can then integrate this with your existing training_data.json
""")

# The structure of the mindmate_format is:
"""
{
    "topic_name": {
        "patterns": ["pattern1", "pattern2"],
        "responses": ["response1", "response2"],
        "follow_ups": ["follow_up1", "follow_up2"],
        "resources": ["resource1", "resource2"]
    }
}
""" 