import json

print("Starting MindMate data conversion...")

# Create empty dictionary for the MindMate format
mindmate_data = {}

try:
    # Try to read from a file first
    try:
        with open('user_intents.json', 'r') as f:
            data = json.load(f)
            print("Found and loaded user_intents.json")
    except:
        # If file doesn't exist, use the data from the script
        print("No user_intents.json found, using default data")
        data = {
            "intents": [
                {"tag": "greeting",
                 "patterns": ["Hi", "Hey", "Is anyone there?","Hi there", "Hello"],
                 "responses": ["Hello there. Tell me how are you feeling today?", "Hi there. What brings you here today?"]
                },
                {"tag": "goodbye",
                 "patterns": ["Bye", "See you later", "Goodbye"],
                 "responses": ["See you later.", "Have a nice day.", "Bye! Come back again."]
                }
                # The user would paste their full data here
            ]
        }
    
    # Convert the data
    print(f"Converting {len(data['intents'])} intents to MindMate format...")
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
    
    # Save the converted data
    with open('mindmate_converted_data.json', 'w') as f:
        json.dump(mindmate_data, f, indent=4)
    print(f"Conversion complete! {len(mindmate_data)} topics saved to mindmate_converted_data.json")
    
    # Try to integrate with existing data
    try:
        with open('training_data.json', 'r') as f:
            existing_data = json.load(f)
        
        orig_count = len(existing_data)
        # Merge the data
        for key, value in mindmate_data.items():
            existing_data[key] = value
        
        # Save the merged data
        with open('training_data_updated.json', 'w') as f:
            json.dump(existing_data, f, indent=4)
        
        new_count = len(existing_data)
        print(f"Integration complete! Added {new_count - orig_count} new topics, updated {len(mindmate_data) - (new_count - orig_count)} existing topics.")
        print("Data saved to training_data_updated.json")
    except Exception as e:
        print(f"Could not integrate with existing data: {e}")

except Exception as e:
    print(f"An error occurred during conversion: {e}")

print("\nINSTRUCTIONS:")
print("1. To use your own data, create a file named 'user_intents.json' with your intents data")
print("2. Run this script: python mindmate_data_converter.py")
print("3. Check the output files: mindmate_converted_data.json and training_data_updated.json")
print("4. Use the updated training data with your MindMate chatbot") 