# Deploying MindMate Chatbot

This guide provides instructions for deploying the MindMate health companion chatbot on various free cloud platforms.

## Recent Updates

- Fixed an issue where MindMate would add random conversational elements when responding to specific questions like "helpline numbers" or "what is X". The chatbot now detects question patterns and provides direct answers without added conversation fillers.

## Option 1: Command Line Interface

The simplest way to use MindMate is through the command-line interface:

```bash
python3 mindmate_cli.py
```

This will start the chatbot directly in your terminal with a simple, interactive text interface. No web browser or internet connection required after the initial code download.

## Option 2: Web Interface (Local)

To run the web interface locally:

```bash
pip install flask
python3 mindmate_api.py
```

Then open your web browser and navigate to: http://localhost:5000

## Option 3: Deploy to Replit (Free Cloud)

Replit offers a free tier that works well for hosting MindMate:

1. Create a free account at [replit.com](https://replit.com)
2. Create a new Python repl
3. Upload all MindMate files to the repl
4. In the Shell tab, run:
   ```
   pip install flask
   ```
5. Set the run command to `python3 mindmate_api.py`
6. Click the "Run" button
7. Replit will provide a URL where your chatbot is hosted

## Option 4: Deploy to Render (Free Cloud)

1. Create a free account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository containing the MindMate code
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `python mindmate_api.py`
6. Set environment variable: `PORT=10000`
7. Deploy the service
8. Render will provide a URL where your chatbot is hosted

## Option 5: Deploy to Hugging Face Spaces (Free GPU)

Hugging Face Spaces provides free GPU hosting:

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Create a new Space with the "Gradio" SDK
3. Upload your MindMate code to the Space
4. Create a `requirements.txt` file with these dependencies:
   ```
   flask
   requests
   ```
5. Create a `Dockerfile` with the following content:
   ```
   FROM python:3.9
   
   WORKDIR /app
   
   COPY . .
   
   RUN pip install -r requirements.txt
   
   EXPOSE 7860
   
   CMD ["python", "mindmate_api.py"]
   ```
6. Enable "Public" visibility under the Space settings
7. Hugging Face will build and deploy your Space with the provided URL

## Option 6: Deploy to Google Colab (Free GPU)

Google Colab provides free GPU resources:

1. Create a new Google Colab notebook
2. Upload your MindMate code to the Colab environment
3. Add and run the following cells:

```python
# Install necessary packages
!pip install flask pyngrok

# Upload files
from google.colab import files
uploaded = files.upload()  # Upload training_data.json or any other required files

# Create public URL for the Flask app
from pyngrok import ngrok
ngrok.set_auth_token("YOUR_NGROK_TOKEN")  # Optional, get a free token from ngrok.com
public_url = ngrok.connect(port=5000)
print(f"Public URL: {public_url}")

# Run the Flask app
!python mindmate_api.py
```

## Requirements File

Create a `requirements.txt` file with the following contents for cloud deployments:

```
flask==2.0.1
requests==2.26.0
```

## Note on Free Hosting Limitations

Most free cloud hosting platforms have limitations:

- Limited compute resources
- Apps may sleep after periods of inactivity
- Monthly limits on usage or uptime
- No persistence of conversation history between sessions

For more reliable hosting, consider upgrading to paid tiers or self-hosting on your own server. 