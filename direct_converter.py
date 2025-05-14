import json

# Your intents data directly in the script
intents_data = {
  "intents": [
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
    },
    {"tag": "thanks",
     "patterns": ["Thanks", "Thank you", "That's helpful", "Thanks for the help", "Than you very much"],
     "responses": ["Happy to help!", "Any time!", "My pleasure", "You're most welcome!"]
    },
    {"tag": "no-response",
        "patterns": [""],
        "responses": ["Sorry, I didn't understand you.", "Please go on.", "Not sure I understand that.", "Please don't hesitate to talk to me."]
    },
    {"tag": "neutral-response",
        "patterns": ["nothing much","nothing really","nothing"],
        "responses": ["Oh I see. Do you want to talk about something?"]
    },
    {"tag": "about",
     "patterns": ["Who are you?", "What are you?", "Who you are?", "Tell me more about yourself.", "What is your name?", "What should I call you?", "What's your name?", "Tell me about yourself" ],
     "responses": ["I'm MindMate, your Personal Therapeutic AI Assistant focused on men's mental health. How are you feeling today?", "I'm MindMate, an AI Assistant designed to help with men's mental health concerns. Tell me about yourself.", "I'm MindMate. I'm a conversational agent designed to assist with mental health support for men. How are you feeling today?", "You can call me MindMate.", "I'm MindMate!", "Call me MindMate"]
    },
    {"tag": "what is depression?",
     "patterns": ["what is depression?"],
     "responses": ["Depression is a common and serious medical illness that negatively affects how you feel, the way you think and how you act. Fortunately, it is also treatable. Depression causes feelings of sadness and/or a loss of interest in activities you once enjoyed. It can lead to a variety of emotional and physical problems and can decrease your ability to function at work and at home."]
    },
    {"tag": "skill",
     "patterns": ["What can you do?"],
     "responses": ["I can provide tailored advice regarding anxiety, depression, stress, and other mental health challenges specific to men's experiences. I can answer questions related to mental health and engage in supportive conversations. Remember though, I'm not a substitute for professional healthcare. Please seek professional help if you need more support than I can provide."]
    }
    # You can add more intents here
  ]
}

# Create the MindMate format
mindmate_data = {}

# Convert each intent
for intent in intents_data["intents"]:
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

# Try to integrate with existing data
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

print("\nTo add more intents: Edit this script, add more items in the 'intents_data' variable, and run it again.") 