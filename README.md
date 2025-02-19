# 🍲 AI-Powered Recipe Assistant

An interactive AI-powered web app that generates **macronutrient breakdowns and personalized recipes** based on user dietary preferences and allergies. Built with **Streamlit** and **Google Cloud Vertex AI**.

## 🚀 Features
- **Macronutrient Analysis:** Breaks down food into Carbohydrates, Protein, and Fat.
- **Personalized Recipes:** Adapts to dietary preferences (Vegan, Keto, etc.).
- **Allergy Awareness:** Excludes ingredients based on user allergies.
- **Cooking Time Customization:** Adjusts recipes based on available cooking time.
- **Fully Standalone:** No external script dependencies.

## 📌 Installation

### 1️⃣ **Clone the Repository**
```bash
https://github.com/roya90/RecipeBot.git
cd RecipeBot
```

### 2️⃣ **Set Up Conda Environment**
Make sure you have **Conda** installed. Then, create a new environment and install the necessary packages.

#### **Create a new Conda environment**
```bash
conda create --name recipe-ai python=3.9 -y
```

#### **Activate the environment**
```bash
conda activate recipe-ai
```

#### **Install required dependencies**
```bash
pip install streamlit google-cloud-aiplatform 
```

### 3️⃣ **Set Up Google Cloud Vertex AI**
1. Create a **Google Cloud Project**.
2. Enable **Vertex AI API**.
3. Set up authentication with:
   ```bash
   gcloud auth application-default login
   ```
4. Set environment variables for your **Google Cloud Project**:
   ```bash

   export VERTEX_PROJECT_ID="your-project-id"
   ```
   *(Or store these in a `.env` file.)*

### 4️⃣ **Run the App**
```bash
streamlit run RecipeBot.py
```

## 📦 Dependencies
- **Streamlit** → For UI interaction
- **Google Cloud Vertex AI** → For AI-powered text generation
- **Regular Expressions (re)** → For structured response parsing

## 🔧 Configuration
Modify `generation_config` and `safety_settings` in the script to adjust AI behavior.

## 🎯 Future Improvements
- **Add memory persistence** to remember user preferences.
- **Integrate a food database API** for verified macronutrient values.

---

## 📜 License
This project is licensed under the **MIT License**.

## 💡 Contributing
Feel free to fork this repo and submit a **pull request**! 🚀
