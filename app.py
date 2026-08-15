import streamlit as st
import joblib
from groq import Groq 

# Load the trained model files
model = joblib.load("models/health_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
symptoms = joblib.load("models/symptoms.pkl")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page settings
# Sidebar
with st.sidebar:
    st.title("🏥 AI Health Assistant")
    st.write("### About")
    st.write(
        "This application uses machine learning to predict "
        "a possible disease based on selected symptoms."
    )

    st.divider()

    st.write("### ⚠️ Important")
    st.write(
        "This tool is for educational purposes only. "
        "It does not replace professional medical advice."
    )

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI-Powered Health Assistant")
st.write("Select your symptoms to get a predicted disease.")

# Symptom selection
st.subheader("🩺 Symptom Checker")
st.write("Select the symptoms you are experiencing:")

selected_symptoms = st.multiselect(
    "Symptoms",
    symptoms,
    placeholder="Choose one or more symptoms..."
)

if selected_symptoms:
    st.info(f"✅ {len(selected_symptoms)} symptom(s) selected")


# Prediction button
if st.button("🔍 Predict Disease", type="primary", use_container_width=True):

    if not selected_symptoms:
        st.warning("Please select at least one symptom.")

    else:
        # Create input data
        input_data = [0] * len(symptoms)

        for symptom in selected_symptoms:
            index = symptoms.index(symptom)
            input_data[index] = 1

        # Make prediction
        prediction = model.predict([input_data])

        # Convert prediction to disease name
        disease = label_encoder.inverse_transform(prediction)[0]

        # Get prediction confidence
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba([input_data])[0]
            confidence = max(probabilities) * 100
        else:
            confidence = None

        # Prediction result
        st.subheader("🔎 Prediction Result")

        st.success(f"Predicted Disease: **{disease}**")

        if confidence is not None:
            st.metric(
                "Prediction Confidence",
                f"{confidence:.2f}%"
            )
            st.progress(min(confidence / 100, 1.0))

        st.info(
            "⚠️ This prediction is for educational purposes only "
            "and should not replace professional medical advice."
        )

        # Preventive recommendations
        recommendations = {
            "Fungal infection": [
                "Keep the affected area clean and dry.",
                "Avoid sharing towels, clothes, or personal items.",
                "Consult a healthcare professional if symptoms persist."
            ],
            "Allergy": [
                "Try to avoid known allergens.",
                "Keep your surroundings clean and dust-free.",
                "Seek medical advice if symptoms become severe."
            ],
            "GERD": [
                "Avoid very large or late meals.",
                "Limit foods that trigger your symptoms.",
                "Avoid lying down immediately after eating.",
                "Consult a healthcare professional if symptoms persist."
            ]
        }

        st.subheader("🛡️ Preventive Guidance")

        if disease in recommendations:
            for advice in recommendations[disease]:
                st.write("• " + advice)
        else:
            st.write(
                "Please consult a healthcare professional for "
                "appropriate preventive advice."
            )

# AI Health Chatbot
st.divider()

st.subheader("🤖 AI Health Assistant")
st.write("Ask a general health question. This chatbot provides educational information only.")

user_question = st.text_input(
    "What would you like to know?",
    placeholder="Example: What are common allergy symptoms?"
)

if st.button("💬 Ask AI"):

    if not user_question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful health education assistant. "
                            "Give clear, simple, general health information. "
                            "Do not diagnose users or replace a doctor. "
                            "If a user describes serious or urgent symptoms, "
                            "recommend seeking immediate professional medical help."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )

            answer = response.choices[0].message.content

            st.write("### 💡 AI Response")
            st.write(answer)

        except Exception as e:
            st.error("The AI assistant could not respond right now.")
            st.caption(str(e))