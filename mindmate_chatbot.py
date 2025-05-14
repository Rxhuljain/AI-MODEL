import json
import os
import random
import re
import datetime
import requests
from collections import Counter

class MindMateBot:
    """
    An advanced AI health companion designed to be conversational and friendly
    Provides supportive conversations about health and wellbeing
    """
    
    def __init__(self, training_data_path):
        """
        Initialize the MindMateBot with enhanced training data
        
        Args:
            training_data_path: Path to the JSON file containing training data
        """
        self.training_data_path = training_data_path
        self.load_training_data()
        self.conversation_history = []
        self.current_topic = None
        self.mood_tracking = {}
        self.communication_style = "conversational"  # changed default to conversational
        self.session_start_time = datetime.datetime.now()
        self.topic_frequency = Counter()
        
        # Enhanced knowledge base access
        self.has_advanced_knowledge = True
        
        self.risk_factors = {
            "suicide_risk": 0,
            "isolation_level": 0,
            "substance_concern": 0,
            "mood_severity": 0,
            "work_stress": 0,
            "relationship_difficulty": 0
        }
        self.user_preferences = {
            "directness": 0.5,  # 0 = indirect, 1 = very direct
            "emotional_comfort": 0.5,  # 0 = uncomfortable, 1 = comfortable
            "help_seeking": 0.5,  # 0 = resistant, 1 = open
            "self_disclosure": 0.5  # 0 = minimal, 1 = detailed
        }
        
        # Knowledge domain specializations
        self.knowledge_domains = {
            "clinical_psychology": True,
            "health_topics": True,
            "wellness_approaches": True,
            "neuroscience": True,
            "psychology": True,
            "cultural_context": True,
            "evidence_based_health": True
        }
        
        # Adding conversation enhancers
        self.conversation_enhancers = {
            "acknowledgments": [
                "I appreciate you sharing that with me.",
                "Thank you for opening up about this.",
                "It takes courage to talk about these things.",
                "I'm glad you brought this up.",
                "Thanks for trusting me with this."
            ],
            "empathy_phrases": [
                "That sounds really challenging.",
                "I can imagine that's not easy to deal with.",
                "It makes sense that you'd feel that way.",
                "Many people have similar experiences.",
                "That's a lot to handle."
            ],
            "follow_up_questions": [
                "How has this been affecting your daily life?",
                "Have you talked to anyone else about this?",
                "When did you first notice this?",
                "What helps you cope when you feel this way?",
                "Is there anything specific that makes it better or worse?"
            ],
            "encouragements": [
                "You're taking positive steps by talking about this.",
                "Just discussing this shows real strength.",
                "Every small step matters in health and wellbeing.",
                "It's great that you're thinking about this.",
                "Your awareness about this is really important."
            ],
            "therapeutic_responses": [
                "Let's explore how this connects to your overall wellbeing.",
                "As your health companion, I'm here to support you through this.",
                "Many therapeutic approaches suggest that awareness is the first step.",
                "From a therapeutic perspective, how we talk about our health matters.",
                "This sounds like something worth reflecting on together."
            ]
        }
        
        # Initialize state file if it doesn't exist
        self.state_file = "bot_state.json"
        if os.path.exists(self.state_file):
            self.load_state()
        else:
            self.save_state()
            
    def load_training_data(self):
        """Load or create training data from a JSON file"""
        try:
            with open(self.training_data_path, 'r') as file:
                self.training_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, create default training data
            self.training_data = {
                "greetings": {
                    "patterns": ["hello", "hi", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening"],
                    "responses": [
                        "Hello! I'm MindMate, a companion designed specifically for men's mental wellbeing. What's on your mind today?",
                        "Hi there. I'm here to listen and chat without judgment. How are you feeling today?",
                        "Hey! I'm MindMate. I'm here to provide a space where you can express yourself freely. What would you like to talk about?"
                    ]
                },
                "stress": {
                    "patterns": ["stressed", "pressure", "overwhelmed", "too much", "can't handle", "burnout"],
                    "responses": [
                        "It sounds like you're dealing with a lot of stress. Many men experience this but don't always talk about it. What specific situations are causing you to feel this way?",
                        "Feeling overwhelmed is common, especially when we're juggling multiple responsibilities. What's contributing most to your stress right now?",
                        "I hear that you're feeling under pressure. Sometimes taking a step back to identify what's in your control can help. Would you like to explore some stress management techniques?"
                    ],
                    "follow_ups": [
                        "Have you tried any particular ways to manage this stress?",
                        "How has this stress been affecting other areas of your life?",
                        "On a scale of 1-10, how would you rate your current stress level?"
                    ]
                },
                "sleep": {
                    "patterns": ["can't sleep", "insomnia", "trouble sleeping", "awake at night", "sleep problems"],
                    "responses": [
                        "Sleep difficulties can really impact our mental well-being. What's your sleep pattern been like recently?",
                        "Many people struggle with sleep, especially during stressful periods. Have you noticed any patterns with your sleep troubles?",
                        "Sleep problems can both result from and contribute to mental health challenges. How long have you been experiencing these sleep issues?"
                    ],
                    "follow_ups": [
                        "Have you tried any sleep hygiene techniques, like limiting screen time before bed?",
                        "How is your sleep environment? Sometimes small changes can make a big difference.",
                        "Many find that having a consistent bedtime routine helps. What does your evening routine look like?"
                    ]
                },
                "relationships": {
                    "patterns": ["relationship", "partner", "girlfriend", "boyfriend", "wife", "husband", "marriage"],
                    "responses": [
                        "Relationships can bring both joy and challenges. What aspects of your relationship have been on your mind?",
                        "Many men find it difficult to discuss relationship concerns. I appreciate you bringing this up. What's going on with your relationship?",
                        "Navigating relationships takes work and good communication. What specific situation in your relationship would you like to explore?"
                    ],
                    "follow_ups": [
                        "Have you been able to discuss these feelings with your partner?",
                        "What would an ideal resolution to this situation look like for you?",
                        "How have relationship dynamics affected your overall well-being?"
                    ]
                },
                "work": {
                    "patterns": ["job", "career", "workplace", "boss", "coworker", "employment", "work"],
                    "responses": [
                        "Work can be a significant source of both fulfillment and stress. What's been happening in your work life?",
                        "Many men tie their identity closely to their work. How has your job been affecting your mental state lately?",
                        "Workplace challenges can spill over into other areas of life. What specific aspects of work have been difficult?"
                    ],
                    "follow_ups": [
                        "How does your current job align with your longer-term goals?",
                        "What parts of your work do you find most rewarding?",
                        "Have you been able to maintain boundaries between work and personal time?"
                    ]
                },
                "emotions": {
                    "patterns": ["feelings", "angry", "sad", "happy", "upset", "emotional", "mood", "depression", "anxiety"],
                    "responses": [
                        "Thank you for sharing how you're feeling. Many men find it difficult to express emotions. Can you tell me more about what triggered these feelings?",
                        "I appreciate you opening up about your emotions. That takes courage. When did you start feeling this way?",
                        "Emotions provide important information about our needs and experiences. How have you been managing these feelings?"
                    ],
                    "follow_ups": [
                        "How do these emotions show up physically in your body?",
                        "What helps you process these kinds of feelings when they arise?",
                        "Have you noticed any patterns around when these emotions are strongest?"
                    ]
                },
                "isolation": {
                    "patterns": ["lonely", "alone", "isolated", "no friends", "no one understands", "disconnected"],
                    "responses": [
                        "Feeling isolated is a common but difficult experience. How long have you been feeling this way?",
                        "Social connection is important for wellbeing, and it's meaningful that you're sharing these feelings. What has contributed to this sense of isolation?",
                        "Many men experience loneliness but don't always talk about it. What kind of connections would you like to have in your life?"
                    ],
                    "follow_ups": [
                        "Are there people in your life you feel you could reach out to?",
                        "What activities have helped you feel connected to others in the past?",
                        "Has there been a change in your social circumstances recently?"
                    ]
                },
                "default": {
                    "responses": [
                        "I'm here to listen and support you. Could you share more about what's on your mind?",
                        "Thank you for sharing that. How has this been affecting you?",
                        "I appreciate you opening up. Would you like to explore this topic further?"
                    ]
                }
            }
            # Create the file with default training data
            self.save_training_data()
    
    def save_training_data(self):
        """Save the current training data to the JSON file"""
        with open(self.training_data_path, 'w') as file:
            json.dump(self.training_data, file, indent=4)
    
    def load_state(self):
        """Load the conversation state from a JSON file"""
        try:
            with open(self.state_file, 'r') as file:
                state_data = json.load(file)
                # Get conversation history and migrate format if needed
                self.conversation_history = state_data.get('history', [])
                # Migrate old conversation format to new format if needed
                self._migrate_conversation_format()
                self.current_topic = state_data.get('current_topic', None)
                self.communication_style = state_data.get('communication_style', "conversational")
                self.mood_tracking = state_data.get('mood_tracking', {})
                self.topic_frequency = Counter(state_data.get('topic_frequency', {}))
                self.risk_factors = state_data.get('risk_factors', {
                    "suicide_risk": 0,
                    "isolation_level": 0,
                    "substance_concern": 0,
                    "mood_severity": 0,
                    "work_stress": 0,
                    "relationship_difficulty": 0
                })
                self.user_preferences = state_data.get('user_preferences', {
                    "directness": 0.5,
                    "emotional_comfort": 0.5,
                    "help_seeking": 0.5,
                    "self_disclosure": 0.5
                })
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, initialize with empty state
            self.conversation_history = []
            self.current_topic = None
            self.communication_style = "conversational"
            self.mood_tracking = {}
            self.topic_frequency = Counter()
            self.risk_factors = {
                "suicide_risk": 0,
                "isolation_level": 0,
                "substance_concern": 0,
                "mood_severity": 0,
                "work_stress": 0,
                "relationship_difficulty": 0
            }
            self.user_preferences = {
                "directness": 0.5,
                "emotional_comfort": 0.5,
                "help_seeking": 0.5,
                "self_disclosure": 0.5
            }
    
    def _migrate_conversation_format(self):
        """Migrate old conversation history format to new format if needed"""
        new_history = []
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for entry in self.conversation_history:
            # Check if this is the old format
            if isinstance(entry, dict) and ('user' in entry or 'bot' in entry):
                # Convert old format to new format
                if 'user' in entry:
                    new_history.append({
                        'role': 'user',
                        'message': entry['user'],
                        'timestamp': timestamp
                    })
                if 'bot' in entry:
                    new_history.append({
                        'role': 'bot',
                        'message': entry['bot'],
                        'timestamp': timestamp
                    })
            elif isinstance(entry, dict) and 'role' in entry:
                # Already in the new format
                new_history.append(entry)
        
        if new_history:  # Only update if we actually converted something
            self.conversation_history = new_history
    
    def save_state(self):
        """Save the current conversation state to a JSON file"""
        state_data = {
            'history': self.conversation_history,
            'current_topic': self.current_topic,
            'communication_style': self.communication_style,
            'mood_tracking': self.mood_tracking,
            'topic_frequency': dict(self.topic_frequency),
            'risk_factors': self.risk_factors,
            'user_preferences': self.user_preferences
        }
        with open(self.state_file, 'w') as file:
            json.dump(state_data, file, indent=4)
    
    def find_intent(self, message):
        """
        Determine the user's intent by matching their message against known patterns
        
        Args:
            message: The user's input message
            
        Returns:
            The identified intent (topic) or "default" if no match is found
        """
        message = message.lower()
        
        # Check each intent for matching patterns
        for intent, data in self.training_data.items():
            if intent == "default":
                continue
                
            # Check if any patterns for this intent match the user's message
            if "patterns" in data:
                for pattern in data["patterns"]:
                    if pattern.lower() in message:
                        # Update topic frequency
                        self.topic_frequency[intent] += 1
                        return intent
        
        # If no intent is matched, return default
        return "default"
    
    def adapt_communication_style(self, message):
        """
        Adapt communication style based on user's messages and patterns
        
        Args:
            message: The user's input message
            
        Returns:
            None, but updates self.communication_style
        """
        message = message.lower()
        
        # Check for direct, fact-oriented language
        fact_oriented_indicators = ["facts", "research", "statistics", "studies", "evidence", "information", "data", "logical", "science"]
        if any(indicator in message for indicator in fact_oriented_indicators):
            self.communication_style = "factual"
            # Update user preferences
            self.user_preferences["directness"] = min(1.0, self.user_preferences["directness"] + 0.1)
            return
        
        # Check for solution-seeking language
        solution_seeking_indicators = ["how to", "solution", "fix", "solve", "advice", "steps", "strategy", "what should I do", "help me", "suggestions"]
        if any(indicator in message for indicator in solution_seeking_indicators):
            self.communication_style = "solution_focused"
            # Update user preferences
            self.user_preferences["directness"] = min(1.0, self.user_preferences["directness"] + 0.1)
            self.user_preferences["help_seeking"] = min(1.0, self.user_preferences["help_seeking"] + 0.1)
            return
            
        # Check for emotional language
        emotional_indicators = ["feel", "feeling", "sad", "angry", "happy", "upset", "anxious", "depressed", "emotions", "hurt", "lonely", "scared"]
        if any(indicator in message for indicator in emotional_indicators):
            self.communication_style = "emotional"
            # Update user preferences
            self.user_preferences["emotional_comfort"] = min(1.0, self.user_preferences["emotional_comfort"] + 0.1)
            self.user_preferences["self_disclosure"] = min(1.0, self.user_preferences["self_disclosure"] + 0.1)
            return
            
        # Check for activity/action orientation
        action_indicators = ["do", "activity", "exercise", "practice", "try", "action", "plan", "goal", "commit", "routine"]
        if any(indicator in message for indicator in action_indicators):
            self.communication_style = "action_oriented"
            return
            
        # Check for help-seeking resistance
        resistance_indicators = ["don't need help", "fine", "nothing's wrong", "not a big deal", "shouldn't complain", "man up", "get over it"]
        if any(indicator in message for indicator in resistance_indicators):
            # Update user preferences
            self.user_preferences["help_seeking"] = max(0.0, self.user_preferences["help_seeking"] - 0.1)
            return
            
        # Check for minimal disclosure
        minimal_disclosure = len(message.split()) < 10 and not any(indicator in message for indicator in emotional_indicators)
        if minimal_disclosure:
            # Update user preferences
            self.user_preferences["self_disclosure"] = max(0.0, self.user_preferences["self_disclosure"] - 0.05)
    
    def get_response(self, intent, use_follow_up=False):
        """
        Get a response based on the identified intent and current communication style
        
        Args:
            intent: The identified user intent
            use_follow_up: Whether to use a follow-up question
            
        Returns:
            A response string
        """
        intent_data = self.training_data.get(intent, self.training_data["default"])
        
        # Get a random response for the intent
        responses = intent_data.get("responses", self.training_data["default"]["responses"])
        response = random.choice(responses)
        
        # Adapt the response based on communication style and user preferences
        response = self._adapt_response_to_user(response, intent)
        
        # Add a follow-up question if available and requested
        if use_follow_up and "follow_ups" in intent_data:
            follow_ups = intent_data["follow_ups"]
            response += " " + self._select_appropriate_follow_up(follow_ups, intent)
        
        # Add resource information if appropriate
        if self._should_offer_resources(intent):
            if "resources" in intent_data and intent_data["resources"]:
                response += "\n\nResource: " + random.choice(intent_data["resources"])
            
        return response
    
    def _select_appropriate_follow_up(self, follow_ups, intent):
        """
        Select the most appropriate follow-up question based on user preferences
        
        Args:
            follow_ups: List of available follow-up questions
            intent: The current intent
            
        Returns:
            Selected follow-up question
        """
        # If the user prefers directness, choose more direct follow-ups
        if self.user_preferences["directness"] > 0.7:
            # Filter for more direct questions
            direct_indicators = ["what specific", "how has", "what strategies", "what steps", "have you tried"]
            direct_follow_ups = [q for q in follow_ups if any(indicator in q.lower() for indicator in direct_indicators)]
            if direct_follow_ups:
                return random.choice(direct_follow_ups)
        
        # If the user is comfortable with emotion, choose more emotion-focused follow-ups
        if self.user_preferences["emotional_comfort"] > 0.7:
            # Filter for more emotional questions
            emotion_indicators = ["feel", "emotion", "affect", "impact", "experience"]
            emotional_follow_ups = [q for q in follow_ups if any(indicator in q.lower() for indicator in emotion_indicators)]
            if emotional_follow_ups:
                return random.choice(emotional_follow_ups)
        
        # If the user is resistant to help-seeking, choose more normalized follow-ups
        if self.user_preferences["help_seeking"] < 0.3:
            # Filter for more normalizing questions
            normalize_indicators = ["many men", "common", "others experience", "typical"]
            normalize_follow_ups = [q for q in follow_ups if any(indicator in q.lower() for indicator in normalize_indicators)]
            if normalize_follow_ups:
                return random.choice(normalize_follow_ups)
        
        # Default: choose a random follow-up
        return random.choice(follow_ups)
    
    def _adapt_response_to_user(self, response, intent):
        """
        Adapt the response based on the user's preferences and communication style
        
        Args:
            response: The base response text
            intent: The current conversational intent/topic
            
        Returns:
            Modified response text
        """
        # Adapt based on communication style first
        response = self._adapt_response_to_style(response, intent)
        
        # Then further adapt based on user preferences
        
        # For users who prefer directness
        if self.user_preferences["directness"] > 0.7 and "?" in response:
            # Make the question more direct
            response = re.sub(r'Could you (.*?)\?', r'What \1?', response)
            response = re.sub(r'Would you like to (.*?)\?', r'Let\'s \1.', response)
        
        # For users uncomfortable with emotional language
        if self.user_preferences["emotional_comfort"] < 0.3:
            # Reduce emotional language
            emotional_terms = ["feel", "emotion", "difficult", "challenging", "struggling"]
            for term in emotional_terms:
                response = re.sub(r'\b' + term + r'\w*\b', '', response)
                
            # Add more practical framing
            if not response.startswith("Let's look at") and not response.startswith("Consider"):
                response = "Let's look at this practically. " + response
        
        # For users resistant to help-seeking
        if self.user_preferences["help_seeking"] < 0.3:
            # Normalize the experience more
            normalizing_phrases = [
                "Many men have similar experiences. ",
                "This is actually quite common. ",
                "You're not alone in this. "
            ]
            if not any(phrase in response for phrase in normalizing_phrases):
                response = random.choice(normalizing_phrases) + response
        
        # For users with minimal self-disclosure
        if self.user_preferences["self_disclosure"] < 0.3:
            # Provide more structure and specific questions
            if "could you share" in response.lower() or "would you like to" in response.lower():
                specific_questions = {
                    "stress": "On a scale of 1-10, how would you rate your current stress level?",
                    "sleep": "How many hours do you typically sleep per night?",
                    "emotions": "When did you first notice these feelings?",
                    "work": "What specific aspect of work has been most challenging?",
                    "relationships": "How long has this relationship issue been occurring?"
                }
                if intent in specific_questions:
                    response = re.sub(r'Could you share more.*?(\?)', specific_questions[intent], response)
                    response = re.sub(r'Would you like to explore.*?(\?)', specific_questions[intent], response)
        
        return response
    
    def _adapt_response_to_style(self, response, intent):
        """
        Adapt the response based on the current communication style
        
        Args:
            response: The base response text
            intent: The current conversational intent/topic
            
        Returns:
            Modified response text
        """
        if self.communication_style == "factual":
            # Add more factual, research-based information
            factual_prefixes = [
                "Research suggests that ",
                "Studies have shown ",
                "According to mental health experts, ",
                "The data indicates that "
            ]
            if not any(prefix in response for prefix in factual_prefixes):
                response = random.choice(factual_prefixes) + response.lower()
                
        elif self.communication_style == "solution_focused":
            # Make response more direct and solution-oriented
            if "?" in response and not response.startswith("Would you like"):
                # Replace open-ended question with more direct suggestion
                response = re.sub(r'What.*\?', 'Let\'s identify specific steps to address this.', response)
                
        elif self.communication_style == "emotional":
            # Make response more validation-focused
            emotional_validators = [
                "It's completely understandable to feel that way. ",
                "Your feelings are valid. ",
                "Many men experience similar emotions. "
            ]
            if not any(validator in response for validator in emotional_validators):
                response = random.choice(emotional_validators) + response
                
        elif self.communication_style == "action_oriented":
            # Make response more activity and action-focused
            action_phrases = [
                "Let's focus on what you can do right now. ",
                "Taking action, even small steps, can help. ",
                "Let's think about practical next steps. "
            ]
            if not any(phrase in response for phrase in action_phrases):
                response = random.choice(action_phrases) + response
        
        return response
    
    def _should_offer_resources(self, intent):
        """
        Determine if resources should be offered based on context
        
        Args:
            intent: The current conversational intent/topic
            
        Returns:
            Boolean indicating whether to offer resources
        """
        # Always offer resources for high-risk topics
        high_risk_topics = ["suicide", "trauma", "substance_use", "grief"]
        if intent in high_risk_topics:
            return True
            
        # Offer resources if we've discussed this topic multiple times
        if self.topic_frequency[intent] >= 2:
            return True
            
        # Offer resources if significant risk factors are present
        if any(value >= 2 for key, value in self.risk_factors.items()):
            return True
            
        # Offer resources if the user seems open to help-seeking
        if self.user_preferences["help_seeking"] > 0.7:
            return random.random() < 0.7  # 70% chance
            
        # Default: 30% chance of offering resources
        return random.random() < 0.3
    
    def update_risk_assessment(self, message, intent):
        """
        Update risk assessment based on user messages
        
        Args:
            message: The user's input message
            intent: The identified intent
            
        Returns:
            None, but updates self.risk_factors
        """
        message = message.lower()
        
        # Suicide risk indicators
        suicide_indicators = ["suicide", "kill myself", "end my life", "better off dead", "no point", "can't go on"]
        if intent == "suicide" or any(indicator in message for indicator in suicide_indicators):
            self.risk_factors["suicide_risk"] = min(5, self.risk_factors["suicide_risk"] + 2)
        
        # Isolation risk indicators
        isolation_indicators = ["alone", "lonely", "no one cares", "by myself", "no friends", "isolated"]
        if intent == "isolation" or any(indicator in message for indicator in isolation_indicators):
            self.risk_factors["isolation_level"] = min(5, self.risk_factors["isolation_level"] + 1)
        
        # Substance use concern indicators
        substance_indicators = ["drinking a lot", "drunk", "high", "using", "wasted", "hungover", "addiction"]
        if intent == "substance_use" or any(indicator in message for indicator in substance_indicators):
            self.risk_factors["substance_concern"] = min(5, self.risk_factors["substance_concern"] + 1)
        
        # Mood severity indicators
        mood_indicators = ["severely", "extreme", "can't function", "hopeless", "desperate", "unbearable"]
        if intent == "emotions" and any(indicator in message for indicator in mood_indicators):
            self.risk_factors["mood_severity"] = min(5, self.risk_factors["mood_severity"] + 1)
            
        # Work stress indicators
        work_indicators = ["hate my job", "can't stand work", "going to quit", "fired", "laid off", "boss hates me"]
        if intent == "work" and any(indicator in message for indicator in work_indicators):
            self.risk_factors["work_stress"] = min(5, self.risk_factors["work_stress"] + 1)
            
        # Relationship difficulty indicators
        relationship_indicators = ["breakup", "divorce", "separation", "cheating", "fighting constantly", "abuse"]
        if intent == "relationships" and any(indicator in message for indicator in relationship_indicators):
            self.risk_factors["relationship_difficulty"] = min(5, self.risk_factors["relationship_difficulty"] + 1)
    
    def track_mood(self, message):
        """
        Track mood mentions for trend analysis
        
        Args:
            message: The user's input message
            
        Returns:
            None, but updates self.mood_tracking
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Initialize today's mood tracking if not present
        if today not in self.mood_tracking:
            self.mood_tracking[today] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }
        
        # Simple mood detection based on keywords
        message = message.lower()
        
        # Check for positive mood indicators
        positive_indicators = ["happy", "good", "great", "excellent", "better", "joy", "hopeful", "grateful", "motivated", "proud", "confident"]
        if any(indicator in message for indicator in positive_indicators):
            self.mood_tracking[today]["positive"] += 1
        
        # Check for negative mood indicators
        negative_indicators = ["sad", "bad", "terrible", "awful", "worse", "depressed", "anxious", "angry", "stressed", "frustrated", "miserable", "hopeless", "exhausted"]
        if any(indicator in message for indicator in negative_indicators):
            self.mood_tracking[today]["negative"] += 1
        
        # If neither positive nor negative indicators are found, increment neutral
        if not any(indicator in message for indicator in positive_indicators + negative_indicators):
            self.mood_tracking[today]["neutral"] += 1
    
    def check_for_crisis(self, message):
        """
        Check if message indicates a crisis situation requiring immediate response
        
        Args:
            message: The user's input message
            
        Returns:
            Boolean indicating whether a crisis was detected
        """
        crisis_indicators = [
            "suicide", "kill myself", "end my life", "die", "better off dead",
            "no point living", "can't go on", "about to hurt", "harm myself",
            "don't want to be alive", "everyone would be better without me"
        ]
        
        return any(indicator in message.lower() for indicator in crisis_indicators)
    
    def get_crisis_response(self):
        """
        Get appropriate crisis response with resources
        
        Returns:
            Crisis response string with resources
        """
        crisis_responses = [
            "I'm concerned about what you're sharing. Your life matters, and help is available. Please reach out to immediate support by calling 988 in the US for the 24/7 Suicide and Crisis Lifeline.",
            "What you're expressing sounds serious, and I want to make sure you get the right support. Please call 988 (US) to speak with a trained crisis counselor immediately. They're available 24/7.",
            "Thank you for trusting me with these thoughts. This is important, and it's crucial you speak with a professional right now. Please call 988 (US) or text HOME to 741741 to reach a crisis counselor."
        ]
        
        # Get crisis resources
        resources = self.training_data.get("suicide", {}).get("resources", [])
        resource_text = ""
        if resources:
            resource_text = "\n\nHere are some immediate resources:\n" + "\n".join(resources)
        
        return random.choice(crisis_responses) + resource_text
    
    def get_mood_summary(self):
        """
        Generate a summary of mood trends
        
        Returns:
            Mood summary string or None if insufficient data
        """
        if not self.mood_tracking:
            return None
            
        # Get the most recent 7 days of data (or fewer if not available)
        dates = sorted(self.mood_tracking.keys())
        recent_dates = dates[-7:] if len(dates) > 7 else dates
        
        # Calculate mood trends
        positive_trend = sum(self.mood_tracking[date]["positive"] for date in recent_dates)
        negative_trend = sum(self.mood_tracking[date]["negative"] for date in recent_dates)
        
        # Generate appropriate summary based on user preferences
        if positive_trend > negative_trend * 2:
            if self.user_preferences["emotional_comfort"] > 0.5:
                return "I've noticed your expressions have been predominantly positive lately. What's been going well for you?"
            else:
                return "You've mentioned several positive things recently. What specific actions or situations have contributed to this?"
                
        elif negative_trend > positive_trend * 2:
            if self.user_preferences["help_seeking"] > 0.5:
                return "I've noticed you've expressed more challenging emotions recently. Would it help to talk about what's been difficult?"
            else:
                return "Your messages suggest you've been facing some challenges lately. Have you identified any patterns or triggers worth exploring?"
                
        elif positive_trend > 0 and negative_trend > 0:
            if self.user_preferences["directness"] > 0.5:
                return "You've expressed a mix of positive and challenging experiences. What specific factors have influenced these ups and downs?"
            else:
                return "I've noticed a mix of different experiences in our conversations. How would you describe your overall wellbeing lately?"
        else:
            return None
    
    def update_user_preferences(self, message_length, response_to_question):
        """
        Update user preferences based on their messaging patterns
        
        Args:
            message_length: Length of user's message
            response_to_question: Whether they responded to a direct question
            
        Returns:
            None, updates self.user_preferences
        """
        # Update directness preference based on message length
        if message_length > 50:  # Longer, more detailed responses
            self.user_preferences["directness"] = max(0.0, self.user_preferences["directness"] - 0.05)
            self.user_preferences["self_disclosure"] = min(1.0, self.user_preferences["self_disclosure"] + 0.05)
        elif message_length < 15:  # Very brief responses
            self.user_preferences["directness"] = min(1.0, self.user_preferences["directness"] + 0.05)
            
        # Update help-seeking preference based on response to questions
        if response_to_question:
            self.user_preferences["help_seeking"] = min(1.0, self.user_preferences["help_seeking"] + 0.05)
        else:
            self.user_preferences["help_seeking"] = max(0.0, self.user_preferences["help_seeking"] - 0.05)
    
    def process_input(self, message):
        """
        Process user input and generate an appropriate response
        
        Args:
            message: The user's input message
            
        Returns:
            A response message from the bot
        """
        # Store user message in conversation history
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'role': 'user',
            'message': message,
            'timestamp': timestamp
        })
        
        # Adapt communication style based on user's message
        self.adapt_communication_style(message)
        
        # Check for crisis situation first
        if self.check_for_crisis(message):
            response = self.get_crisis_response()
            self.conversation_history.append({
                'role': 'bot',
                'message': response,
                'timestamp': timestamp
            })
            self.save_state()
            return response
        
        # Track user's mood
        self.track_mood(message)
        
        # Check if it's a question that might require internet information
        if self.needs_online_info(message):
            online_info = self.search_health_info(message)
            if online_info:
                response = self.format_online_info_response(message, online_info)
                self.conversation_history.append({
                    'role': 'bot',
                    'message': response,
                    'timestamp': timestamp
                })
                self.save_state()
                return response
        
        # Determine user's intent
        intent = self.find_intent(message)
        self.current_topic = intent
        self.topic_frequency[intent] += 1
        
        # Update risk assessment based on message content
        self.update_risk_assessment(message, intent)
        
        # Update user preferences based on interaction
        message_length = len(message.split())
        self.update_user_preferences(message_length, 'question' in message)
        
        # Generate appropriate response
        if self.is_knowledge_seeking_question(message):
            # For knowledge-seeking questions, provide more detailed information
            response = self.generate_enhanced_knowledge_response(message)
        elif intent in self.training_data:
            # For recognized intents, get appropriate response with follow-up
            # Determine if we should add a follow-up question based on conversation state
            if len(self.conversation_history) >= 3:
                # Check if conversation history has the expected format
                if isinstance(self.conversation_history[-3], dict) and 'role' in self.conversation_history[-3]:
                    # New format with 'role' key
                    use_follow_up = self.conversation_history[-3]['role'] == 'bot' and random.random() < 0.5
                elif isinstance(self.conversation_history[-3], dict) and 'bot' in self.conversation_history[-3]:
                    # Old format with 'bot' key
                    use_follow_up = random.random() < 0.5
                else:
                    use_follow_up = True
            else:
                # For new topics, always add a follow-up question
                use_follow_up = True
                
            response = self.get_enhanced_response(intent, message, use_follow_up)
        else:
            # For unrecognized intents, generate a general response
            response = self.generate_general_mental_health_response(message)
        
        # Add conversation enhancers to make it more natural
        response = self._add_conversation_enhancers(response, intent)
        
        # Store the bot's response in conversation history
        self.conversation_history.append({
            'role': 'bot',
            'message': response,
            'timestamp': timestamp
        })
        
        # Save the updated state
        self.save_state()
        
        return response
    
    def _add_conversation_enhancers(self, response, intent):
        """
        Make responses more conversational by adding natural language enhancers
        
        Args:
            response: The generated response
            intent: The identified intent
            
        Returns:
            Enhanced conversational response
        """
        # Don't modify responses that are already very conversational or short
        if len(response.split()) < 12 or response.count('?') > 1:
            return response
            
        # Check if response already includes some form of acknowledgment
        has_acknowledgment = any(ack.lower() in response.lower() 
                             for ack in ["thank", "appreciate", "glad", "good to hear"])
        
        # Only add acknowledgment at the beginning if it makes sense contextually
        if not has_acknowledgment and random.random() < 0.4:
            acknowledgment = random.choice(self.conversation_enhancers["acknowledgments"])
            response = acknowledgment + " " + response
            
        # Add follow-up question if the response doesn't already end with a question
        if not response.rstrip().endswith('?') and random.random() < 0.3:
            if intent in ["stress", "sleep", "relationships", "work", "emotions", "isolation"]:
                # Add relevant follow-up for specific topics
                follow_up = random.choice(self.conversation_enhancers["follow_up_questions"])
                response = response + " " + follow_up
                
        # Occasionally add an encouraging statement
        if random.random() < 0.2 and not any(phrase in response.lower() for phrase in ["great job", "well done", "good work"]):
            encouragement = random.choice(self.conversation_enhancers["encouragements"])
            if random.random() < 0.5:  # 50% at beginning, 50% at end
                response = encouragement + " " + response
            else:
                response = response + " " + encouragement
                
        # Sometimes add therapeutic framing
        if intent in ["emotions", "stress", "sleep", "isolation"] and random.random() < 0.3:
            therapeutic_phrase = random.choice(self.conversation_enhancers["therapeutic_responses"])
            if not response.strip().endswith("?"):
                response = response + " " + therapeutic_phrase
                
        return response
    
    def is_knowledge_seeking_question(self, message):
        """
        Determine if the message is seeking specific mental health knowledge
        
        Args:
            message: The user's message
            
        Returns:
            Boolean indicating if this is a knowledge-seeking question
        """
        knowledge_indicators = [
            "what is", "what are", "how does", "why do", "can you explain",
            "tell me about", "what causes", "symptoms of", "treatment for",
            "therapy for", "research on", "studies about", "statistics on",
            "facts about", "information on", "definition of", "meaning of"
        ]
        
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in knowledge_indicators)
    
    def generate_enhanced_knowledge_response(self, message):
        """
        Generate a comprehensive, knowledgeable response about mental health topics
        
        Args:
            message: The user's knowledge-seeking message
            
        Returns:
            Enhanced response with detailed mental health information
        """
        message_lower = message.lower()
        
        # Extract key mental health topics from the message
        mental_health_topics = [
            "depression", "anxiety", "ptsd", "trauma", "addiction", "substance use",
            "bipolar", "schizophrenia", "adhd", "ocd", "eating disorders", "insomnia",
            "stress", "burnout", "grief", "loneliness", "suicide", "self-harm", 
            "therapy", "medication", "cbt", "dbt", "psychodynamic", "mindfulness",
            "masculine norms", "help-seeking", "emotional regulation", "vulnerability"
        ]
        
        # Check which mental health topics are mentioned
        mentioned_topics = [topic for topic in mental_health_topics if topic in message_lower]
        
        # Default to a general mental health response if no specific topic is found
        if not mentioned_topics:
            return self.generate_general_mental_health_response(message)
        
        # Generate specialized response based on the identified topic
        primary_topic = mentioned_topics[0]  # Focus on the first mentioned topic
        
        # Male-specific mental health knowledge - expanded and improved with more detailed information
        male_specific_context = {
            "depression": "Depression in men often presents differently than in women, with symptoms like irritability, anger, substance use, and risk-taking behavior sometimes being more prominent than sadness. Physical manifestations such as fatigue, sleep disturbances, and unexplained pain may mask emotional symptoms. Men are less likely to seek help for depression due to stigma and masculine norms around self-reliance, contributing to underdiagnosis.\n\nBiological factors (hormonal fluctuations, genetic predisposition), psychological factors (cognitive patterns, unresolved trauma), and social factors (relationship difficulties, work stress, isolation) all interact to influence depression in men. Recent research suggests that inflammatory processes and gut microbiome health may also play significant roles in depression development and maintenance.",
            
            "anxiety": "Anxiety disorders in men may manifest as irritability, anger, or substance use rather than worry or fear that's more typically recognized. Men often cope with anxiety through avoidance behaviors, distraction, intense work focus, or self-medication with substances. Cultural expectations around masculinity can make it difficult for men to acknowledge anxiety symptoms, instead attributing physical manifestations to stress or medical conditions.\n\nPhysiologically, anxiety triggers the sympathetic nervous system's fight-or-flight response, causing increased heart rate, muscle tension, and hypervigilance. This state can become chronic when left unaddressed, contributing to long-term physical health problems including cardiovascular issues and immune system dysregulation.",
            
            "ptsd": "PTSD in men is frequently associated with combat exposure, physical assaults, accidents, childhood trauma, and witnessing violence. Men may be more likely to exhibit externalizing behaviors like aggression, substance use, or risk-taking when dealing with trauma, rather than more recognized symptoms like hypervigilance or flashbacks.\n\nNeurobiologically, trauma causes alterations in the amygdala (emotional processing), hippocampus (memory formation), and prefrontal cortex (executive function) that can persist for years. These changes affect stress response, emotional regulation, and information processing. Treatment approaches like trauma-focused CBT, EMDR, and somatic experiencing can help address both the psychological and neurobiological impacts of trauma.",
            
            "addiction": "Men have higher rates of substance use disorders than women and face different risk factors and barriers to treatment. Social norms around masculinity can normalize excessive drinking or substance use as acceptable coping mechanisms for men, while simultaneously stigmatizing help-seeking.\n\nGenetically, men with family histories of addiction show higher vulnerability, with specific gene variations affecting dopamine processing and reward sensitivity. Environmental factors like early exposure, trauma history, and social network influence interact with these genetic predispositions. Effective treatment usually requires addressing underlying issues like unresolved trauma, emotional regulation difficulties, or co-occurring mental health conditions rather than focusing solely on substance use.",
            
            "suicide": "Men die by suicide at 3-4 times the rate of women in most developed countries, despite having lower rates of suicidal thoughts and attempts. This 'gender paradox' results from men choosing more lethal methods, being less likely to seek help, having fewer social connections to notice warning signs, and displaying different warning signals that may not be recognized as suicide risk.\n\nPrevention strategies specifically effective for men include means restriction (reducing access to lethal methods), targeted messaging that frames help-seeking as a strength, connection-building programs, and training friends/family to recognize male-specific warning signs like increased anger, risk-taking, or sudden withdrawal.",
            
            "help-seeking": "Men seek professional mental health help at lower rates than women across most cultures and age groups. Barriers include stigma, masculine norms around self-reliance and emotional control, difficulty recognizing emotional distress, preference for self-management, and concerns about perceived weakness.\n\nEffective approaches to improve help-seeking include framing mental health care as a way to improve performance or functioning rather than addressing weakness, providing male-friendly access points like primary care integration or digital options, involving trusted social connections, and featuring positive male role models who have benefited from mental health support.",
            
            "therapy": "Effective therapy approaches for men often incorporate problem-solving components, clear goals, and respect for autonomy. Some men prefer action-oriented, skills-based approaches like CBT or may benefit from therapy modalities that acknowledge masculine socialization while building new capabilities.\n\nTherapeutic alliance is particularly important for male clients, with research showing better outcomes when therapists understand and respect men's socialization experiences rather than pathologizing masculine traits. Men may respond better to therapy that begins with practical problem-solving before gradually increasing emotional exploration, building therapeutic trust through demonstrated effectiveness.",
            
            "emotional regulation": "Emotional regulation skills are crucial for mental wellbeing and can be especially beneficial for men who may have received limited emotional vocabulary or expression tools through socialization. These skills include accurately identifying emotions, understanding their triggers and functions, and developing healthy response strategies.\n\nPhysiologically, emotional regulation involves the interaction between the amygdala (emotional reactions), prefrontal cortex (rational thinking), and autonomic nervous system. Men who develop greater awareness of bodily sensations associated with emotions often report improved regulation capabilities and reduced psychological distress. Specific techniques include progressive muscle relaxation, breath control, cognitive reframing, and mindfulness practices.",
            
            "vulnerability": "While often culturally discouraged in men, vulnerability is actually a strength that facilitates deeper connections, authentic self-expression, and psychological growth. Research by Brené Brown has shown that vulnerability is essential for emotional well-being across genders, though men may face greater cultural barriers to expressing it.\n\nMen who learn to distinguish between harmful exposure (which increases risk) and healthy vulnerability (which builds connection) often report improved relationship satisfaction and reduced psychological distress. Starting with trusted individuals and gradually expanding one's comfort zone with vulnerability can build this capacity over time. Many men find that frameworks like 'courage' or 'authenticity' make vulnerability more accessible than emotional language.",
            
            "medication": "Psychiatric medications can be an important component of treatment for various mental health conditions. For men, considerations include potential sexual side effects from some antidepressants, interactions with alcohol or other substances, and the importance of addressing concerns about perceived dependency.\n\nPhysiological differences between men and women can affect medication metabolism and effective dosing. Men metabolize some medications more quickly due to body mass, liver enzyme activity, and hormonal factors. Regular follow-up with healthcare providers is essential to monitor effectiveness and side effects, with some men preferring concrete measures like symptom tracking to evaluate medication benefits.",
            
            "exercise": "Physical activity shows robust evidence as both prevention and treatment for various mental health conditions, with particularly strong effects for depression and anxiety. For men, exercise can be an accessible entry point to mental health care that aligns with masculine norms around action and physical capability.\n\nNeurobiologically, exercise increases BDNF (brain-derived neurotrophic factor), supports neurogenesis, regulates stress hormones, and releases endorphins that improve mood. Both aerobic exercise and strength training show mental health benefits, with intensity, consistency, and enjoyment being more important factors than specific activity type. Group-based physical activities can address both mental health and social connection needs simultaneously.",
            
            "adhd": "Attention-Deficit/Hyperactivity Disorder often presents differently in men than women, with men more likely to show hyperactive-impulsive symptoms rather than primarily inattentive presentation. Many men receive diagnoses in adulthood after struggling with work performance, relationship difficulties, or substance use issues that stem from unrecognized ADHD.\n\nNeurobiologically, ADHD involves differences in dopamine processing, executive function networks, and frontal lobe activity. Treatment approaches combining medication (typically stimulants or non-stimulant alternatives), behavioral strategies, environmental modifications, and skills development show the strongest outcomes. Men with ADHD often benefit from understanding how the condition affects emotional regulation and impulse control, not just attention and focus."
        }
        
        # Generate comprehensive response based on the topic and male-specific knowledge
        if primary_topic in male_specific_context:
            specific_knowledge = male_specific_context[primary_topic]
            response = f"{specific_knowledge}\n\nThis information is particularly relevant for men's mental health because masculine norms and socialization can affect how symptoms present, are experienced, and how treatment might be approached."
        else:
            # For topics not in our specialized dictionary, provide a general but competent response
            response = self.generate_topic_specific_response(primary_topic)
            
        # Add evidence-based recommendations where appropriate
        if primary_topic not in ["suicide"]:  # Avoid giving simple recommendations for crisis topics
            response += "\n\nEvidence-based approaches that may help include: "
            if primary_topic in ["depression", "anxiety", "stress"]:
                response += "cognitive-behavioral therapy (CBT), regular physical exercise, mindfulness practices, and social connection. Studies show that men often respond well to approaches that combine cognitive restructuring with behavioral activation and concrete skill-building. Professional support from a therapist who understands men's specific needs can be particularly valuable."
            elif primary_topic in ["addiction", "substance use"]:
                response += "motivational interviewing, cognitive-behavioral therapy, community reinforcement approach, and in some cases, medication-assisted treatment. Support groups specifically designed for men can provide understanding, accountability, and practical strategies without requiring immediate emotional disclosure that some men find uncomfortable."
            elif primary_topic in ["ptsd", "trauma"]:
                response += "trauma-focused CBT, EMDR (Eye Movement Desensitization and Reprocessing), prolonged exposure therapy, and in some cases, medication. Finding a trauma-informed therapist with experience working with men can be important, as can body-based approaches that address the physiological aspects of trauma."
                
        return response
    
    def generate_topic_specific_response(self, topic):
        """Generate a knowledgeable response about a specific mental health topic"""
        # This would contain detailed information about various mental health topics
        # Enhanced with more comprehensive information
        topic_information = {
            "therapy": "Therapy approaches beneficial for men include cognitive-behavioral therapy (CBT), which focuses on identifying and changing unhelpful thought patterns; acceptance and commitment therapy (ACT), which emphasizes psychological flexibility and values-based action; and solution-focused brief therapy, which many men appreciate for its practical, goal-oriented approach.\n\nResearch indicates that the therapeutic relationship is as important as the specific modality for treatment outcomes. Men often benefit from therapists who understand masculine socialization without judgment, balance validation with challenge, and recognize that men may enter therapy with different expectations and communication styles than women. Some men find that starting with practical problem-solving before moving to deeper emotional work builds therapeutic trust.",
            
            "mindfulness": "Mindfulness practices can be particularly helpful for men who tend to intellectualize emotions rather than experiencing them directly. These practices develop greater awareness of emotional and physical states, reduce rumination, and improve stress management by training attention to the present moment without judgment.\n\nClinical research shows that regular mindfulness practice creates measurable changes in brain regions associated with emotional regulation, stress response, and self-awareness. For men specifically, approaches that frame mindfulness in terms of mental training or performance enhancement rather than spiritual practice often increase engagement. Brief, structured practices (like the 3-minute breathing space) may be more accessible entry points than longer meditation sessions.",
            
            "emotional regulation": "Emotional regulation skills are crucial for mental wellbeing and can be especially beneficial for men who may have received limited emotional vocabulary or expression tools through socialization. These skills include identifying emotions accurately, understanding their triggers and functions, and developing healthy response strategies.\n\nPhysiologically, emotional regulation involves the interaction between the amygdala (emotional reactions), prefrontal cortex (rational thinking), and autonomic nervous system. Men who develop greater awareness of bodily sensations associated with emotions often report improved regulation capabilities and reduced psychological distress. Specific techniques include progressive muscle relaxation, breath control, cognitive reframing, and mindfulness practices.",
            
            "vulnerability": "While often culturally discouraged in men, vulnerability is actually a strength that facilitates deeper connections, authentic self-expression, and psychological growth. Research by Brené Brown has shown that vulnerability is essential for emotional well-being across genders, though men may face greater cultural barriers to expressing it.\n\nMen who learn to distinguish between harmful exposure (which increases risk) and healthy vulnerability (which builds connection) often report improved relationship satisfaction and reduced psychological distress. Starting with trusted individuals and gradually expanding one's comfort zone with vulnerability can build this capacity over time. Many men find that frameworks like 'courage' or 'authenticity' make vulnerability more accessible than emotional language.",
            
            "medication": "Psychiatric medications can be an important component of treatment for various mental health conditions. For men, considerations include potential sexual side effects from some antidepressants, interactions with alcohol or other substances, and the importance of addressing concerns about perceived dependency.\n\nPhysiological differences between men and women can affect medication metabolism and effective dosing. Men metabolize some medications more quickly due to body mass, liver enzyme activity, and hormonal factors. Regular follow-up with healthcare providers is essential to monitor effectiveness and side effects, with some men preferring concrete measures like symptom tracking to evaluate medication benefits.",
            
            "exercise": "Physical activity shows robust evidence as both prevention and treatment for various mental health conditions, with particularly strong effects for depression and anxiety. For men, exercise can be an accessible entry point to mental health care that aligns with masculine norms around action and physical capability.\n\nNeurobiologically, exercise increases BDNF (brain-derived neurotrophic factor), supports neurogenesis, regulates stress hormones, and releases endorphins that improve mood. Both aerobic exercise and strength training show mental health benefits, with intensity, consistency, and enjoyment being more important factors than specific activity type. Group-based physical activities can address both mental health and social connection needs simultaneously.",
            
            "adhd": "Attention-Deficit/Hyperactivity Disorder often presents differently in men than women, with men more likely to show hyperactive-impulsive symptoms rather than primarily inattentive presentation. Many men receive diagnoses in adulthood after struggling with work performance, relationship difficulties, or substance use issues that stem from unrecognized ADHD.\n\nNeurobiologically, ADHD involves differences in dopamine processing, executive function networks, and frontal lobe activity. Treatment approaches combining medication (typically stimulants or non-stimulant alternatives), behavioral strategies, environmental modifications, and skills development show the strongest outcomes. Men with ADHD often benefit from understanding how the condition affects emotional regulation and impulse control, not just attention and focus."
        }
        
        if topic in topic_information:
            return topic_information[topic]
        else:
            # For topics we don't have specific information on - provide a more substantive generic response
            return f"The topic of {topic} is an important aspect of mental health with particular relevance for men. Men often experience unique challenges in this area due to societal expectations, physiological factors, and patterns of socialization that can affect how symptoms present and how treatment is approached.\n\nResearch indicates that men may benefit from approaches that acknowledge these gendered experiences while providing practical, evidence-based strategies for improvement. Understanding the interplay between biological factors (neurochemistry, genetics, hormones), psychological aspects (thoughts, emotions, behaviors), and social dimensions (relationships, cultural context, support systems) is essential for comprehensive mental health care."
    
    def generate_general_mental_health_response(self, message):
        """Generate a knowledgeable response to a general mental health question"""
        # Extract the question type to provide a more appropriate response - enhanced with more detailed information
        if "what is" in message.lower() or "what are" in message.lower():
            return "Mental health encompasses our emotional, psychological, and social wellbeing, affecting how we think, feel, act, handle stress, relate to others, and make choices. It exists on a continuum rather than as a simple presence or absence of disorders.\n\nMen's mental health has unique considerations due to socialization patterns, help-seeking behaviors, and biological factors. Men experience comparable rates of mental health conditions to women but are less likely to seek help, resulting in underdiagnosis. Men also experience higher rates of certain issues like substance use disorders and die by suicide at significantly higher rates than women in most countries.\n\nBiologically, factors like hormonal differences, brain structure variations, and genetic predispositions influence men's mental health presentations. Psychologically, cognitive patterns, emotional processing styles, and coping mechanisms often show gender differences. Socially, expectations around masculinity, relationship patterns, and support-seeking behaviors create distinct mental health contexts for men."
        
        elif "how" in message.lower():
            return "Men's mental health is influenced by multiple interacting factors including biological predispositions (genetics, neurochemistry, hormones), life experiences (particularly early development and trauma), social connections, economic circumstances, cultural expectations around masculinity, and access to healthcare.\n\nMental health exists on a spectrum, with various support options available from peer support and lifestyle modifications to therapy and medication. Research shows that men often respond best to approaches that acknowledge masculine socialization while building new skills for emotional awareness and expression.\n\nEffective strategies for supporting men's mental health include reducing stigma through education and representation, creating male-friendly access points to support, fostering social connection through activity-based groups, encouraging preventive health behaviors, and developing mental health literacy so men can better recognize and respond to difficulties early."
        
        else:
            return "Men's mental health involves unique considerations including different symptom presentations (often more externalized through behaviors rather than direct emotional expression), substantial barriers to seeking help, and the significant impact of masculine socialization on well-being.\n\nEvidence shows that mental health conditions like depression, anxiety, and PTSD may present differently in men, with symptoms like irritability, anger, risk-taking, and substance use sometimes being more prominent than the symptoms typically highlighted in diagnostic criteria. This can lead to missed diagnoses and delayed treatment.\n\nIntegrated approaches that address biological factors (through nutrition, exercise, medication when appropriate), psychological aspects (cognitive patterns, emotional awareness, behavior change), and social dimensions (meaningful connections, purpose, community) typically show the strongest outcomes for improving men's mental health."
        
    def get_enhanced_response(self, intent, message, use_follow_up=False):
        """
        Get a comprehensive response based on the identified intent with advanced knowledge
        
        Args:
            intent: The identified user intent
            message: Original user message
            use_follow_up: Whether to use a follow-up question
            
        Returns:
            Enhanced response string
        """
        intent_data = self.training_data.get(intent, self.training_data["default"])
        
        # Get a random response for the intent
        responses = intent_data.get("responses", self.training_data["default"]["responses"])
        response = random.choice(responses)
        
        # Adapt the response based on communication style and user preferences
        response = self._adapt_response_to_user(response, intent)
        
        # Add a follow-up question if available and requested
        if use_follow_up and "follow_ups" in intent_data:
            follow_ups = intent_data["follow_ups"]
            response += " " + self._select_appropriate_follow_up(follow_ups, intent)
        
        # Add resource information if appropriate
        if self._should_offer_resources(intent):
            if "resources" in intent_data and intent_data["resources"]:
                response += "\n\nResource: " + random.choice(intent_data["resources"])
        
        # Enhance the response with additional expert knowledge
        if intent != "default" and intent != "greetings":
            response = self._enhance_with_expert_knowledge(response, intent, message)
                
        return response
    
    def _enhance_with_expert_knowledge(self, response, intent, message):
        """
        Add expert knowledge to responses based on the topic
        
        Args:
            response: Original response
            intent: The conversation topic
            message: User's message
            
        Returns:
            Enhanced response with expert knowledge
        """
        # Expert knowledge by topic - significantly enhanced with more detailed information
        expert_additions = {
            "stress": "\n\nStudies from the American Psychological Association show that chronic stress affects men differently, impacting cardiovascular health, immune function, and cognitive processing. Men often experience stress through physiological symptoms like muscle tension, headaches, or digestive issues before recognizing the emotional component. Stress triggers higher testosterone decreases in men, which may affect mood, energy, and motivation.\n\nEffective stress management strategies specifically helpful for men include high-intensity exercise, spending time in nature, structured problem-solving, and mindfulness practices that focus on the present moment rather than rumination.",
            
            "sleep": "\n\nRecent research from the Sleep Foundation indicates that men's sleep is affected by unique factors including sleep apnea (which men experience at 2-3 times the rate of women), shift work, and hormonal patterns. Quality sleep directly impacts mental health by regulating emotion processing in the prefrontal cortex and amygdala.\n\nMen with sleep issues often benefit from maintaining consistent sleep-wake times, limiting screen exposure before bed, moderate evening exercise, and creating a sleep environment with cooler temperatures (65-68°F/18-20°C) which aligns with men's typically higher body temperatures.",
            
            "relationships": "\n\nRelationship dynamics have significant mental health implications for men. Dr. John Gottman's research shows that men in relationships may experience 'emotional flooding' more quickly during conflict, causing physiological overwhelm that impairs problem-solving abilities. Men who express appropriate vulnerability in relationships report greater satisfaction, closeness, and mental wellbeing.\n\nMany men benefit from understanding attachment styles and how early life experiences shape relationship patterns. Developing emotional vocabulary beyond the basics of 'fine' or 'angry' can significantly improve relationship satisfaction and reduce psychological distress.",
            
            "work": "\n\nOccupational identity is often more central to men's self-concept than women's, making work transitions or challenges particularly impactful on mental health. Research published in the Journal of Occupational Health Psychology demonstrates that work stress affects physical health through elevated inflammatory markers and cardiovascular indicators.\n\nMen who find meaning in their work beyond financial compensation report significantly better mental health outcomes. Creating clear boundaries between work and personal life is especially important for men who tend to derive much of their identity from professional achievement.",
            
            "emotions": "\n\nRecent neuroimaging studies reveal that men may process emotional stimuli differently on average, with some research showing distinct patterns of brain activation when experiencing emotions like sadness or empathy. Many men have been socialized to interpret emotional vulnerability as weakness, creating barriers to emotional awareness.\n\nMen often benefit from understanding that emotions provide valuable information about needs and values rather than being problems to solve. Learning to identify emotions in the body (through physical sensations) can be particularly helpful for men who have difficulty naming feelings directly.",
            
            "isolation": "\n\nRecent meta-analyses show social isolation has physiological effects comparable to smoking or obesity. Men typically maintain smaller social networks than women and may rely heavily on partners for emotional support, increasing vulnerability during relationship transitions or after retirement.\n\nMeaningful social connection for men often develops through shared activities and side-by-side engagement rather than face-to-face conversation. Activity-based groups centered around interests or skills development can be particularly effective at combating isolation without requiring immediate emotional disclosure.",
            
            "anger": "\n\nAnger often serves as a secondary emotion for men, masking more vulnerable feelings like hurt, fear, embarrassment, or shame. Research shows heightened anger responses in men can be tied to testosterone levels, past experiences, and social learning about acceptable emotional expression.\n\nProcessing anger effectively involves recognizing physiological warning signs (like tension, increased heart rate), identifying underlying emotions, and developing wider emotional vocabulary. Brief physical activities, controlled breathing techniques, and perspective-taking exercises can be particularly helpful for men in managing intense anger.",
            
            "substance_use": "\n\nGenetic and neurobiological factors contribute 40-60% of addiction vulnerability, with men showing different trajectories of substance use development and recovery. Men are more likely to use substances to cope with negative emotions they've been conditioned not to express directly.\n\nThe relationship between substance use and mental health conditions is bidirectional, with each potentially worsening the other. Men-specific recovery approaches that emphasize personal responsibility, practical problem-solving, and meaningful life purpose show stronger outcomes than generic programs.",
            
            "purpose": "\n\nExistential psychology research shows that a sense of purpose and meaning significantly improves mental health outcomes and resilience. Men often experience purpose shifts during major life transitions like fatherhood, career changes, or retirement.\n\nMen who find meaning through contribution to others, skill mastery, or connection to something larger than themselves report better mental health metrics and life satisfaction. Purpose-oriented activities that align with personal values can create lasting protective factors against depression and anxiety.",
            
            "fatherhood": "\n\nFatherhood creates measurable neurobiological changes, including shifts in oxytocin, vasopressin, and testosterone levels that support caregiving behavior. These hormonal changes facilitate bonding and can actually reduce stress reactivity in engaged fathers.\n\nResearch shows that involved fatherhood is associated with better mental health outcomes for both fathers and their children. Men who actively participate in childcare often develop enhanced emotional intelligence and relationship skills that benefit their overall mental wellbeing.",
            
            "identity": "\n\nMasculine identity is undergoing significant cultural shifts, creating both opportunities and challenges for men's mental health. Research shows that rigid adherence to traditional masculine norms like emotional stoicism, self-reliance, and dominance is associated with poorer mental health outcomes and reduced help-seeking.\n\nMen who develop more flexible approaches to masculine identity, incorporating both traditional strengths like courage and protection with openness to vulnerability and connection, show better psychological outcomes across multiple studies.",
            
            "trauma": "\n\nTrauma creates physiological changes in the nervous system, including alterations to the HPA axis that affect stress response. Men may be more likely to experience specific trauma responses like anger, emotional numbing, or risk-taking behaviors rather than more recognized symptoms like anxiety or intrusive thoughts.\n\nEvidence-based trauma treatments like EMDR, CPT, or sensorimotor approaches can be particularly effective for men when practitioners understand gender-specific presentation and recovery patterns. Physical activity, structured skill-building, and graduated exposure approaches often resonate with men's recovery preferences.",
            
            "grief": "\n\nMen's grief often manifests differently than cultural expectations, with more instrumental (action-oriented) rather than intuitive (emotion-expressing) patterns. Many men process grief through activity, problem-solving, or intellectual understanding rather than direct emotional expression.\n\nResearch indicates that men may experience delayed grief responses, sometimes emerging months or years after a loss when the immediate practical demands have subsided. Creating meaningful rituals, sharing memories through storytelling, and finding tangible ways to honor losses can be particularly helpful approaches."
        }
        
        # Add expert knowledge if available for this topic
        if intent in expert_additions:
            # Only add expert knowledge if the response is not too long already
            if len(response) < 500:  # Avoid overly long responses
                specialized_knowledge = expert_additions[intent]
                
                # Check if the message suggests the user wants in-depth information
                depth_indicators = ["why", "explain", "understand", "curious", "interested", "tell me more", "research", "know more", "details", "elaborate", "specific", "science", "studies"]
                if any(indicator in message.lower() for indicator in depth_indicators):
                    return response + specialized_knowledge
                    
                # Otherwise, 85% chance to add the expert knowledge (increased from 60%)
                if random.random() < 0.85:
                    return response + specialized_knowledge
        
        return response
    
    def needs_online_info(self, message):
        """
        Determine if the message requires online information.
        
        Args:
            message: The user's message
            
        Returns:
            Boolean indicating if the message needs online information
        """
        message = message.lower()
        
        # Check for explicit requests for internet information
        explicit_indicators = [
            "search", "look up", "internet", "online", "latest", "recent", 
            "research", "studies", "what does the internet say", "find information"
        ]
        
        if any(indicator in message for indicator in explicit_indicators):
            return True
            
        # Check for specific health questions that might benefit from up-to-date information
        health_question_patterns = [
            r"what (is|are) the (symptoms|signs|causes|treatments|side effects|risks) of",
            r"how (can|do|should) (I|you) (treat|manage|handle|deal with|cure)",
            r"is \w+ (a symptom|treatment|cure|effective) for",
            r"latest (research|studies|findings|treatments|guidelines) (on|for|about)",
            r"new (treatments|medications|therapies|approaches|studies) for"
        ]
        
        if any(re.search(pattern, message) for pattern in health_question_patterns):
            return True
            
        return False
        
    def search_health_info(self, query):
        """
        Search for health information online.
        
        Args:
            query: The search query
            
        Returns:
            Dictionary containing search results or None if failed
        """
        try:
            # Extract key health terms from the query
            health_terms = self._extract_health_terms(query)
            search_query = ' '.join(health_terms) if health_terms else query
            
            # Add 'health' to the query if it doesn't already contain health-related terms
            health_indicators = ["health", "medical", "symptoms", "treatment", "condition", "disease", "therapy"]
            if not any(indicator in search_query.lower() for indicator in health_indicators):
                search_query = f"health {search_query}"
                
            # Simple search API call - in a real implementation, this would use a proper API
            # This is a placeholder for demonstration purposes
            search_url = f"https://api.duckduckgo.com/?q={search_query}&format=json"
            response = requests.get(search_url)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    # DuckDuckGo API sometimes returns non-JSON responses
                    return {"AbstractText": "I found some information online, but it's better to consult with a healthcare professional for accurate guidance."}
            else:
                # Fallback to a simulated response
                return {
                    "AbstractText": f"Based on general health information, {self._generate_generic_health_response(query)}",
                    "simulated": True
                }
                
        except Exception as e:
            print(f"Error searching for health information: {e}")
            return None
            
    def _extract_health_terms(self, query):
        """Extract key health-related terms from the query."""
        # List of common health-related terms
        health_terms = [
            "symptoms", "treatment", "cure", "medication", "therapy", "disease",
            "condition", "syndrome", "virus", "bacterial", "infection", "chronic",
            "acute", "pain", "inflammation", "diet", "exercise", "nutrition",
            "mental health", "anxiety", "depression", "stress", "sleep", "fatigue",
            "headache", "migraine", "heart", "diabetes", "cancer", "arthritis",
            "allergy", "immune", "vitamin", "supplement", "prescription"
        ]
        
        # Extract health terms mentioned in the query
        terms = []
        query_lower = query.lower()
        for term in health_terms:
            if term in query_lower:
                terms.append(term)
                
        # Also extract any specific conditions or symptoms using regex
        condition_pattern = r"(suffering from|have|experiencing|diagnosed with) (\w+)"
        matches = re.findall(condition_pattern, query_lower)
        for match in matches:
            if match[1] not in ["a", "an", "the", "some", "any", "been"]:
                terms.append(match[1])
                
        return terms
        
    def format_online_info_response(self, query, search_results):
        """
        Format online search results into a conversational response.
        
        Args:
            query: Original user query
            search_results: Dictionary containing search results
            
        Returns:
            Formatted response string
        """
        # Check if we have any useful information
        if not search_results or "AbstractText" not in search_results or not search_results["AbstractText"]:
            return "I tried searching for information about that online, but couldn't find specific details. It might be better to consult with a healthcare professional for personalized advice. Is there something else you'd like to talk about regarding your health?"
            
        abstract = search_results["AbstractText"]
        
        # Format the response in a therapeutic and conversational way
        intro_phrases = [
            "Based on health information I found online, ",
            "According to available health resources, ",
            "From what I could find about this health topic, ",
            "I looked this up for you, and "
        ]
        
        # Add therapeutic framing and personalization
        response = f"{random.choice(intro_phrases)}{abstract}"
        
        # Add a disclaimer
        disclaimers = [
            " Remember that online information is general, and it's always best to consult with a healthcare professional for personalized advice.",
            " While this information may be helpful, only a healthcare provider can give you personalized medical advice based on your specific situation.",
            " I should note that I'm sharing general information, not personalized medical advice. A healthcare professional can give you guidance specific to your needs."
        ]
        
        # Add a follow-up question to maintain conversation
        follow_ups = [
            " How does this information relate to what you've been experiencing?",
            " Does this information help with what you were asking about?",
            " Would you like to discuss any specific part of this information further?",
            " Is there a particular aspect of this you're concerned about?"
        ]
        
        # Combine all parts
        if not "simulated" in search_results:
            response += random.choice(disclaimers)
        
        response += random.choice(follow_ups)
        
        return response
        
    def _generate_generic_health_response(self, query):
        """Generate a generic health response when online search fails."""
        # Extract potential health topics from the query
        health_topics = {
            "sleep": "adequate sleep (7-9 hours for adults) is essential for physical and mental health. Poor sleep can affect mood, cognition, and immune function.",
            "diet": "a balanced diet rich in fruits, vegetables, whole grains, and lean proteins supports overall health. Nutritional needs vary by individual.",
            "exercise": "regular physical activity provides numerous benefits including stress reduction, improved mood, better sleep, and reduced risk of chronic diseases.",
            "stress": "chronic stress can impact physical and mental health. Stress management techniques like mindfulness, deep breathing, and physical activity can help.",
            "anxiety": "anxiety is a common experience that becomes concerning when it's persistent and interferes with daily life. Therapeutic approaches and lifestyle changes can help manage anxiety.",
            "depression": "depression is a complex condition affecting mood, thinking, and daily functioning. Professional support, therapy, and sometimes medication can be effective treatments.",
            "pain": "pain can have many causes and should be evaluated by a healthcare provider, especially if it's severe or persistent.",
            "headache": "headaches have various triggers including stress, dehydration, or underlying health conditions. Persistent or severe headaches should be evaluated by a healthcare provider.",
            "nutrition": "proper nutrition involves consuming adequate nutrients from a variety of food sources to support bodily functions and overall health."
        }
        
        # Look for matching topics in the query
        query_lower = query.lower()
        for topic, info in health_topics.items():
            if topic in query_lower:
                return info
                
        # Default response if no specific topic is identified
        return "it's important to take a holistic approach to health, considering physical, mental, and social wellbeing. Regular check-ups with healthcare providers, balanced nutrition, adequate sleep, physical activity, and stress management are general foundations of good health."