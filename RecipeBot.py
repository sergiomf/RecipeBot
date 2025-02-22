import os
import streamlit as st
import json
import re
import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold


# Access the variables
project_id = os.getenv("VERTEX_PROJECT_ID")

# Initialize Vertex AI
vertexai.init(project=project_id, location="us-central1")

# Initialize model
def initialize_chat():
    model = GenerativeModel("gemini-1.5-flash-002")
    return model.start_chat()

# Define generation configuration and safety settings
generation_config = {
    "max_output_tokens": 2048,
    "temperature": 1,
    "top_p": 1,
}

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Configure Streamlit page
st.set_page_config(
    page_title="MacroGenie - Your Macronutrient & Recipe Assistant",
    page_icon="🍲",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #fff8e7; font-family: 'Poppins', sans-serif; }
    .title { color: #e76f51; font-size: 44px; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .subtitle { color: #2a9d8f; font-size: 20px; text-align: center; margin-bottom: 20px; }
    .footer { color: #264653; font-size: 14px; text-align: center; margin-top: 30px; }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown('<div class="title">🍲 MacroGenie</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover tasty macronutrient breakdowns and personalized recipes!</div>', unsafe_allow_html=True)

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = initialize_chat()
if "preferences" not in st.session_state:
    st.session_state.preferences = {}

# Step 1: Get user input
food_name = st.text_input(
    'Enter the name of the food you want to look up:',
    placeholder="e.g., Farofa com coca cola",
    help="Enter a dish to get its macronutrient breakdown and a personalized recipe."
)

if food_name:
    # Step 2: Ask follow-up questions
    st.markdown("### 🌱 Tell us about your preferences!")
    diet_preference = st.selectbox(
        "Do you follow any dietary restrictions?",
        ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"]
    )
    allergies = st.multiselect(
        "Do you have any food allergies?",
        ["None", "Dairy", "Nuts", "Gluten", "Shellfish", "Eggs", "Soy"]
    )
    cooking_time = st.slider(
        "How much time do you have for cooking? (in minutes)",
        min_value=5, max_value=120, value=30, step=5
    )

    # Store responses in session state
    st.session_state.preferences["diet"] = diet_preference
    st.session_state.preferences["allergies"] = allergies
    st.session_state.preferences["cooking_time"] = cooking_time

    # Step 3: Generate Macronutrient Breakdown
    with st.spinner('🍳 Analyzing macronutrient content...'):
        prompt = f"""
        Given the following dietary preference: {diet_preference}
        and allergies: {', '.join(allergies) if allergies else 'None'},
        provide a list of ingredients for {food_name}.
        Adjust the ingredient list to meet these preferences and put them in the macro nutrient categories.

        The output should be exactly in the following form:

        Carbohydrates:  
        Protein:
        Fat: 
        """
        response = st.session_state.chat.send_message(
            [prompt],
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    # Extract and parse the response correctly
    response_text = response.candidates[0].content.text.strip()

    # Function to extract macronutrients from AI response
    def extract_macros(response_text, category):
        match = re.search(rf"{category}: (.*?)(?:\n\n|$)", response_text, re.DOTALL)
        if match:
            ingredients = match.group(1).strip()
            ingredients_list = [item.strip() for item in re.split(r",|\n", ingredients) if item.strip()]
            return ingredients_list
        return ["N/A"]

    # Extracting values properly
    carbs_list = extract_macros(response_text, "Carbohydrates")
    protein_list = extract_macros(response_text, "Protein")
    fat_list = extract_macros(response_text, "Fat")

    # Display Macronutrient Breakdown
    st.markdown(f"## 🍽️ Macronutrient Breakdown for **{food_name}**")

    st.markdown("### 🥖 Carbohydrates")
    st.markdown("• " + "\n• ".join(carbs_list), unsafe_allow_html=True)

    st.markdown("### 🍗 Protein")
    st.markdown("• " + "\n• ".join(protein_list), unsafe_allow_html=True)

    st.markdown("### 🧈 Fat")
    st.markdown("• " + "\n• ".join(fat_list), unsafe_allow_html=True)

    # Step 4: Generate Personalized Recipe
    with st.spinner('🍲 Generating personalized recipe...'):
        recipe_prompt = f"""
        Generate a recipe for {food_name} using ONLY the following macronutrients: 
        Carbohydrates: {', '.join(carbs_list)}, 
        Protein: {', '.join(protein_list)}, 
        Fat: {', '.join(fat_list)}.
        
        The recipe should be:
        - {diet_preference}-friendly
        - Free from {', '.join(allergies) if allergies else 'no allergens'}
        - Cookable in {cooking_time} minutes or less.
        
        Follow this format:
        Ingredients:

        Instructions:
        """
        res = st.session_state.chat.send_message(
            [recipe_prompt],
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    # Extract and format the recipe
    recipe_text = res.candidates[0].content.text.strip()
    recipe_parts = recipe_text.split("Instructions:")

    ingredients = recipe_parts[0].replace("Ingredients:", "").replace("*", "\n").strip() if "Ingredients:" in recipe_text else "N/A"
    instructions = re.sub(r"(?<=\.)\s+(?=\d+\.)", "\n", recipe_parts[1].strip()) if len(recipe_parts) > 1 else "N/A"

    # Display Personalized Recipe
    st.markdown("### 📖 Personalized Recipe")
    st.markdown("#### 🛒 Ingredients")
    st.markdown(f"<div style='background-color:#fef6e4; padding:10px; border-left: 5px solid #f4a261;'>{ingredients}</div>", unsafe_allow_html=True)

    st.markdown("#### 🥄 Instructions")
    st.markdown(f"<div style='background-color:#fef6e4; padding:10px; border-left: 5px solid #2a9d8f;'>{instructions}</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Developed with ❤️ by MacroGenie Team</div>', unsafe_allow_html=True)
