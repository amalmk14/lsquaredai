import os  
import google.generativeai as genai  
from dotenv import load_dotenv  
from llm import *

load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_ai_story(name, details):
    # Create a prompt using the character's name and other details
    prompt = f"Write a short and creative story in 4-5 sentences about a character named {name}. Details: {details}"

    try:
        # model = genai.GenerativeModel("gemini-1.5-flash") 

        response = model.generate_content(prompt)

        return response.text
        
    except Exception as e:
        print("Gemini error:", e)
        return "Server busy or quota exceeded. Please try again in a few minutes."
