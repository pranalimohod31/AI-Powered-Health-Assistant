import streamlit as st
import joblib

# Load the trained model files
model = joblib.load("models/health_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
symptoms = joblib.load("models/symptoms.pkl")

# Page settings
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI-Powered Health Assistant")
st.write("Select your symptoms to get a predicted disease.")

# Symptom selection
selected_symptoms = st.multiselect(
    "Select your symptoms:",
    symptoms
)

# Prediction button
if st.button("🔍 Predict Disease"):

    if not selected_symptoms:
        st.warning("Please select at least one symptom.")

    else:
        # Create input with all symptoms set to 0
        input_data = [0] * len(symptoms)

        # Set selected symptoms to 1
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

        st.success(f"Predicted Disease: **{disease}**")

        if confidence is not None:
            st.metric("Prediction Confidence", f"{confidence:.2f}%")

        st.info(
            "⚠️ This prediction is for educational purposes only "
            "and should not replace professional medical advice."
        )

        st.info(
            "⚠️ This prediction is for educational purposes only "
            "and should not replace professional medical advice."
        )