import os
from google import genai

class MedicalChatbot:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.client = None
        if self.api_key and self.api_key.strip() != "":
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to init Gemini client: {e}")

    def is_ready(self):
        return self.client is not None

    def generate_response(self, prompt, context_data):
        if not self.is_ready():
            return "Please provide a valid Gemini API key in the sidebar to talk with the AI assistant."

        system_instruction = (
            "You are a compassionate, professional AI medical assistant specializing in dermatology."
            "The user has uploaded a skin image and our system predicted: "
            f"Disease: {context_data.get('disease_key', 'Unknown')} ({context_data.get('name', '')})\n"
            f"Severity: {context_data.get('severity', 'Unknown')}\n"
            f"Precautions: {', '.join(context_data.get('precautions', []))}\n"
            "Answer the user's questions strictly based on this context. "
            "Keep answers concise, and always remind them to consult a human doctor."
        )

        full_prompt = f"System Context: {system_instruction}\n\nUser Question: {prompt}\n\nYour Answer:"

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
