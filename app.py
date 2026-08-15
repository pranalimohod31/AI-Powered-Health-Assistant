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

        if disease in recommendations:
            st.subheader("🛡️ Preventive Guidance")

            for advice in recommendations[disease]:
                st.write("• " + advice)

        else:
            st.subheader("🛡️ Preventive Guidance")
                    # Disease information
        disease_info = {
            "Fungal infection": "A fungal infection is caused by fungi and can affect the skin or other parts of the body.",
            "Allergy": "An allergy happens when the immune system reacts to a substance that is usually harmless.",
            "GERD": "GERD is a condition where stomach contents frequently flow back into the esophagus."
        }

        st.subheader("📖 About the Predicted Disease")

        if disease in disease_info:
            st.write(disease_info[disease])
        else:
            st.write(
                "Information about this condition is not currently available. "
                "Please consult a qualified healthcare professional."
            )

