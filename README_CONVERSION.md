# MindMate Intents Conversion Guide

This guide explains how to convert your intents data to the MindMate format.

## Files Included

- `mindmate_data_converter.py` - The main conversion script
- `user_intents.json` - A sample file with some of your intents (you can add all your intents to this file)
- `final_solution.md` - Detailed technical explanation of the conversion process

## How to Convert Your Intents

### Option 1: Quick Start

1. Run the conversion script:
   ```
   python mindmate_data_converter.py
   ```

2. This will convert the included sample `user_intents.json` and produce:
   - `mindmate_converted_data.json` - The converted data
   - `training_data_updated.json` - Your converted data merged with the existing training data

### Option 2: Convert All Your Intents

1. Edit `user_intents.json` to include all your intents
2. Run the conversion script:
   ```
   python mindmate_data_converter.py
   ```

### Option 3: Manual Integration

If you prefer to manually integrate specific intents:

1. Convert your data using the script
2. Open `mindmate_converted_data.json` and `training_data.json`
3. Copy the intents you want from the converted file to the training data
4. Save the updated training data

## Format Differences

### Your Current Format:
```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hi", "Hello"],
      "responses": ["Hello there. How are you feeling today?"]
    }
  ]
}
```

### MindMate Format:
```json
{
  "greeting": {
    "patterns": ["Hi", "Hello"],
    "responses": ["Hello there. How are you feeling today?"],
    "follow_ups": ["How long have you been feeling this way?"],
    "resources": ["I can provide more information on this topic if you'd like."]
  }
}
```

## Important Notes

1. The script automatically adds generic follow-ups and resources to each intent
2. You may want to customize these for mental health-specific topics
3. The conversion uses the intent tag (converted to lowercase with underscores) as the key
4. Any existing intents with the same key will be replaced in the merged file

## Using the Converted Data

After conversion, you can:

1. Replace your entire `training_data.json` with `training_data_updated.json`
2. Or manually copy specific intents into your existing training data
3. Restart your MindMate chatbot to use the updated training data 