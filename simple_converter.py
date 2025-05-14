import json

# Load your intents data (from file or hardcoded sample)
try:
    with open('user_intents.json', 'r') as f:
        data = json.load(f)
except:
    data = {
        "intents": [
            {"tag": "greeting", "patterns": ["Hi"], "responses": ["Hello"]}
        ]
    }

# Create the MindMate format
mindmate_data = {}
for intent in data["intents"]:
    tag = intent["tag"].lower().replace(" ", "_").replace("?", "").replace("!", "")
    mindmate_data[tag] = {
        "patterns": intent["patterns"],
        "responses": intent["responses"],
        "follow_ups": ["How are you feeling?"],
        "resources": ["I can provide more information."]
    }

# Save to new file
with open('converted.json', 'w') as f:
    json.dump(mindmate_data, f, indent=2)

print("Converted data saved to converted.json") 