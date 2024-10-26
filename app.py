import streamlit as st
from groq import Groq
import os
# Initialize Groq client
client = Groq(api_key=os.getenv("groq"))

# Function to generate recipes using LLaMA 3 from Groq
def generate_recipe_stream(ingredients):
    # Generate the API request to the Groq LLaMA 3 model
    prompt = f"Generate a recipe using the following ingredients: {', '.join(ingredients)}. Also, suggest alternatives for any rare or missing ingredients."
    
    # API parameters
    completion = client.chat.completions.create(
        model="llama3-8b-8192",  # You can replace with the appropriate LLaMA model
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # Collect streaming response
    generated_text = ""
    for chunk in completion:
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            generated_text += delta_content
            yield generated_text  # Stream response chunk by chunk

# Streamlit App
st.title("AI-Powered Recipe Generator 🍳 (Powered by Groq LLaMA 3)")

def hide_streamlit_style():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

hide_streamlit_style()

# User input for ingredients
ingredients_input = st.text_input("Enter the ingredients you have (comma-separated):", "eggs, flour, sugar, butter")

# Convert input to a list of ingredients
ingredients = [item.strip() for item in ingredients_input.split(",")]

# Create a placeholder for displaying the recipe as it's being generated
recipe_placeholder = st.empty()

# Generate recipe based on the ingredients
if st.button("Generate Recipe"):
    # Stream the response in real-time
    for streamed_text in generate_recipe_stream(ingredients):
        recipe_placeholder.write(f"### Here's your recipe:\n\n{streamed_text}")


