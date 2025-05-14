import json

# Paste your JSON data between the triple quotes
INTENTS_DATA = """
{"intents": [
    {"tag": "greeting",
     "patterns": ["Hi", "Hey", "Is anyone there?","Hi there", "Hello", "Hey there", "Howdy", "Hola", "Bonjour","Hay", "Sasa", "Good Evening", "Good afternoon"],
     "responses": ["Hello there. Tell me how are you feeling today?", "Hi there. What brings you here today?", "Hi there. How are you feeling today?", "Great to see you. How do you feel currently?", "Hello there. Glad to see you're back. What's going on in your world right now?"]
    }
    # Paste the rest of your JSON data here
]}
"""

# Parse the input data
data = json.loads(INTENTS_DATA)

# Create the MindMate format
mindmate_data = {}

# Convert each intent
for intent in data["intents"]:
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

# Save to new file
with open('mindmate_converted_data.json', 'w') as f:
    json.dump(mindmate_data, f, indent=4)

print("Conversion complete! Data saved to mindmate_converted_data.json")

# Optional: Integration with existing data
try:
    with open('training_data.json', 'r') as f:
        existing_data = json.load(f)
    
    # Merge the data
    for key, value in mindmate_data.items():
        existing_data[key] = value
    
    # Save the merged data
    with open('training_data_updated.json', 'w') as f:
        json.dump(existing_data, f, indent=4)
    
    print("Integration with existing data complete! Data saved to training_data_updated.json")
except Exception as e:
    print(f"Could not integrate with existing data: {e}") 