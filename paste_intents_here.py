import json

# Paste your intents data between the triple quotes below:
intents_json = """
{"intents": [
    {"tag": "greeting",
     "patterns": ["Hi", "Hey", "Is anyone there?","Hi there", "Hello", "Hey there", "Howdy", "Hola", "Bonjour","Hay", "Sasa", "Good Evening", "Good afternoon"],
     "responses": ["Hello there. Tell me how are you feeling today?", "Hi there. What brings you here today?", "Hi there. How are you feeling today?", "Great to see you. How do you feel currently?", "Hello there. Glad to see you're back. What's going on in your world right now?"]
    },
    {"tag": "morning",
        "patterns": ["Good morning"],
        "responses": ["Good morning. I hope you had a good night's sleep. How are you feeling today? "]
    },
    {"tag": "afternoon",
        "patterns": ["Good afternoon"],
        "responses": ["Good afternoon. How is your day going?"]
    },
    {"tag": "evening",
        "patterns": ["Good evening"],
        "responses": ["Good evening. How has your day been?"]
    },
    {"tag": "night",
        "patterns": ["Good night"],
        "responses": ["Good night. Get some proper sleep", "Good night. Sweet dreams."]
    },
    {"tag": "goodbye",
     "patterns": ["Bye", "See you later", "Goodbye", "Au revoir", "Sayonara", "ok bye", "Bye then", "Fare thee well"],
     "responses": ["See you later.", "Have a nice day.", "Bye! Come back again.", "I'll see you soon."]
    }
]
}
"""

# Parse the intents data
intents_data = json.loads(intents_json)

# Create a structure for MindMate's training data format
mindmate_data = {}

# Convert the format
for intent in intents_data["intents"]:
    tag = intent["tag"].lower().replace(" ", "_").replace("?", "").replace("!", "")
    patterns = intent["patterns"]
    responses = intent["responses"]
    
    mindmate_data[tag] = {
        "patterns": patterns,
        "responses": responses
    }

# Add some default follow-ups and resources for each category
for key in mindmate_data.keys():
    if "follow_ups" not in mindmate_data[key]:
        mindmate_data[key]["follow_ups"] = [
            "How long have you been feeling this way?",
            "Would you like to explore this topic more deeply?",
            "Have you discussed this with anyone else in your life?"
        ]
    
    if "resources" not in mindmate_data[key]:
        mindmate_data[key]["resources"] = [
            "I can provide more information on this topic if you'd like."
        ]

# Save the converted data
with open("mindmate_converted_data.json", "w") as f:
    json.dump(mindmate_data, f, indent=4)

print("Conversion complete! Data saved to mindmate_converted_data.json") 