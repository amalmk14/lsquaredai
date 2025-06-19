import os  
import google.generativeai as genai  
from dotenv import load_dotenv  

load_dotenv()

# Configure the Gemini API with the key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_ai_story(name, details):
    # Create a prompt using the character's name and other details
    prompt = f"Write a short and creative story in 4-5 sentences about a character named {name}. Details: {details}"

    try:
        # Load the Gemini model 
        model = genai.GenerativeModel("gemini-1.5-flash") 

        # Send the prompt to Gemini and get the AI-generated content
        response = model.generate_content(prompt)

        # Return the text of the story
        return response.text
        
    except Exception as e:
        # In case of errors 
        print("Gemini error:", e)
        return "Server busy or quota exceeded. Please try again in a few minutes."
