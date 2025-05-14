#!/usr/bin/env python3
from mindmate_chatbot import MindMateBot
import random
import time
import os
import sys

# Text colors for terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print slowly, to simulate typing
def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

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
    
    # Otherwise, add conversation fillers and personalization
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

# Main CLI application
def main():
    clear_screen()
    
    # ASCII art logo
    print(Colors.BLUE + """
 __  __ _           _ __  __       _       
|  \/  (_)_ __   __| |  \/  | __ _| |_ ___ 
| |\/| | | '_ \ / _` | |\/| |/ _` | __/ _ \\
| |  | | | | | | (_| | |  | | (_| | ||  __/
|_|  |_|_|_| |_|\__,_|_|  |_|\__,_|\__\___|
    """ + Colors.ENDC)
    
    print(Colors.BOLD + "\nWelcome to MindMate CLI - Your Friendly Health Companion" + Colors.ENDC)
    print("Type 'exit', 'quit', or 'bye' to end the conversation.")
    print("Type 'clear' to clear the screen.\n")
    
    print(Colors.YELLOW + "DISCLAIMER: I'm an AI companion designed to provide supportive conversations about your health and wellbeing.")
    print("While I can offer a friendly chat and information, I'm not a licensed healthcare professional.")
    print("If you're experiencing a health crisis, please contact a healthcare provider." + Colors.ENDC + "\n")
    
    # Initialize the chatbot
    print("Initializing MindMate...")
    bot = MindMateBot("training_data.json")
    print("MindMate is ready to chat!\n")
    
    # Initial greeting
    greeting = "Hi there! I'm MindMate, your friendly health companion and therapeutic friend. How are you feeling today?"
    print(Colors.GREEN + "MindMate: " + Colors.ENDC, end="")
    print_slow(greeting)
    print()
    
    # Main conversation loop
    while True:
        # Get user input
        user_input = input(Colors.BLUE + "You: " + Colors.ENDC)
        print()
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print(Colors.GREEN + "MindMate: " + Colors.ENDC, end="")
            print_slow("Thank you for chatting with me. Take care of yourself, and remember I'm here whenever you need support.")
            break
            
        # Check for clear command
        if user_input.lower() == 'clear':
            clear_screen()
            continue
        
        # Check for empty input
        if not user_input.strip():
            continue
        
        # Generate response
        if check_for_crisis(user_input):
            response = bot.get_crisis_response()
        else:
            # Process the user message
            response = bot.process_input(user_input)
            
            # Make responses more conversational
            response = make_more_conversational(response, user_input)
        
        # Print bot response
        print(Colors.GREEN + "MindMate: " + Colors.ENDC, end="")
        print_slow(response)
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThank you for using MindMate. Goodbye!")
        sys.exit(0) 