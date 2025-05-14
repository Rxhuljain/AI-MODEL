# Converting Intents to MindMate Format

To convert your intents data to the MindMate format, follow these steps:

## Step 1: Understanding the Format Differences

**Your Intent Format:**
```json
{
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["Hi", "Hey", "Hello"],
            "responses": ["Hello there. How are you feeling today?"]
        }
    ]
}
```

**MindMate Format:**
```json
{
    "greeting": {
        "patterns": ["Hi", "Hey", "Hello"],
        "responses": ["Hello there. How are you feeling today?"],
        "follow_ups": ["How long have you been feeling this way?"],
        "resources": ["I can provide more information on this topic if you'd like."]
    }
}
```

## Step 2: Conversion Process

1. Create a new file called `convert.py` with the following code:

```python
import json

# Load your intents data
with open('your_intents.json', 'r') as f:
    data = json.load(f)

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
```

2. Save your intents data as `your_intents.json`
3. Run the script: `python convert.py`
4. The converted data will be in `mindmate_converted_data.json`

## Step 3: Integrating with Existing Training Data

To integrate with the existing MindMate training data:

```python
import json

# Load your converted data
with open('mindmate_converted_data.json', 'r') as f:
    converted_data = json.load(f)

# Load the existing MindMate training data
with open('training_data.json', 'r') as f:
    mindmate_data = json.load(f)

# Merge the data
# This will overwrite any existing intents with the same keys
for key, value in converted_data.items():
    mindmate_data[key] = value

# Save the merged data
with open('training_data_updated.json', 'w') as f:
    json.dump(mindmate_data, f, indent=4)

print("Integration complete! Data saved to training_data_updated.json")
```

## Sample Result

Here's how some of your intents will look in the MindMate format:

```json
{
    "greeting": {
        "patterns": ["Hi", "Hey", "Is anyone there?", "Hi there", "Hello", "Hey there", "Howdy", "Hola", "Bonjour", "Hay", "Sasa", "Good Evening", "Good afternoon"],
        "responses": ["Hello there. Tell me how are you feeling today?", "Hi there. What brings you here today?", "Hi there. How are you feeling today?", "Great to see you. How do you feel currently?", "Hello there. Glad to see you're back. What's going on in your world right now?"],
        "follow_ups": ["How long have you been feeling this way?", "Would you like to explore this topic more deeply?", "Have you discussed this with anyone else in your life?"],
        "resources": ["I can provide more information on this topic if you'd like."]
    },
    "goodbye": {
        "patterns": ["Bye", "See you later", "Goodbye", "Au revoir", "Sayonara", "ok bye", "Bye then", "Fare thee well"],
        "responses": ["See you later.", "Have a nice day.", "Bye! Come back again.", "I'll see you soon."],
        "follow_ups": ["How long have you been feeling this way?", "Would you like to explore this topic more deeply?", "Have you discussed this with anyone else in your life?"],
        "resources": ["I can provide more information on this topic if you'd like."]
    }
}
```

## Additional Notes

1. The MindMate format uses the intent tag as the key for each entry
2. You may want to customize the default follow-ups and resources for each intent
3. For mental health-specific intents like "depression" or "anxiety", consider adding more specific resources
4. The script converts spaces to underscores and removes question marks and exclamation marks from tags 