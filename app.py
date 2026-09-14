```python
import streamlit as st
import joblib
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD MODEL FILES
# =========================================================

model = joblib.load("models/health_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
symptoms = joblib.load("models/symptoms.pkl")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Main background */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(37, 211, 172, 0.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(79, 70, 229, 0.10), transparent 30%),
        linear-gradient(135deg, #f8fbff 0%, #eef7f6 100%);
}

/* Remove top padding */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f766e 0%,
        #115e59 45%,
        #134e4a 100%
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.18);
    color: white;
    border-radius: 12px;
}

/* Hero */

.hero {
    padding: 45px 50px;
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            rgba(15,118,110,0.98),
            rgba(13,148,136,0.95),
            rgba(20,184,166,0.90)
        );
    color: white;
    box-shadow: 0 20px 50px rgba(15,118,110,0.20);
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "🩺";
    position: absolute;
    right: 50px;
    top: 25px;
    font-size: 120px;
    opacity: 0.10;
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 12px;
    color: white;
}

.hero p {
    font-size: 18px;
    line-height: 1.7;
    max-width: 850px;
    color: rgba(255,255,255,0.92);
}

/* Badge */

.badge {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 30px;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.25);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 18px;
}

/* Section title */

.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #134e4a;
    margin-top: 25px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 20px;
}

/* Cards */

.card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(226,232,240,0.8);
    border-radius: 22px;
    padding: 28px;
    box-shadow: 0 10px 35px rgba(15,23,42,0.07);
    margin-bottom: 22px;
}

.card:hover {
    box-shadow: 0 15px 40px rgba(15,23,42,0.10);
}

/* Feature cards */

.feature-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    border: 1px solid #e2e8f0;
    min-height: 175px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.feature-icon {
    font-size: 35px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #134e4a;
    margin-bottom: 8px;
}

.feature-text {
    font-size: 14px;
    line-height: 1.6;
    color: #64748b;
}

/* Prediction */

.prediction-card {
    background: linear-gradient(
        135deg,
        #ecfdf5,
        #f0fdfa
    );
    border: 2px solid #99f6e4;
    border-radius: 24px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0 12px 35px rgba(13,148,136,0.12);
}

.prediction-label {
    font-size: 13px;
    color: #0f766e;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.prediction-disease {
    font-size: 34px;
    font-weight: 800;
    color: #134e4a;
    margin-top: 8px;
}

/* Metric cards */

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    text-align: center;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #0f766e;
}

.metric-label {
    font-size: 13px;
    color: #64748b;
    margin-top: 5px;
}

/* Warning */

.warning-card {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-left: 5px solid #f97316;
    border-radius: 16px;
    padding: 20px;
    margin: 20px 0;
}

.warning-card h4 {
    color: #9a3412;
    margin-bottom: 8px;
}

.warning-card p {
    color: #7c2d12;
    font-size: 14px;
    line-height: 1.6;
}

/* Info card */

.info-card {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 5px solid #3b82f6;
    border-radius: 16px;
    padding: 20px;
}

/* Chatbot */

.chat-card {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #f5f3ff
    );
    border: 1px solid #c7d2fe;
    border-radius: 24px;
    padding: 30px;
    margin-top: 20px;
}

/* Buttons */

.stButton > button {
    border-radius: 14px;
    min-height: 48px;
    font-weight: 700;
    border: none;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* Multiselect */

.stMultiSelect > div > div {
    border-radius: 14px !important;
    border: 1px solid #cbd5e1 !important;
}

/* Text input */

.stTextInput input {
    border-radius: 14px !important;
    padding: 15px !important;
    border: 1px solid #cbd5e1 !important;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    padding: 35px 10px 10px;
    font-size: 13px;
}

.footer strong {
    color: #0f766e;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:10px;">
        <div style="font-size:55px;">🏥</div>
        <h2 style="margin-bottom:0;">AI Health Assistant</h2>
        <p style="opacity:0.85;">Smart • Simple • Educational</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.markdown("""
    <div style="
        background:rgba(255,255,255,0.10);
        padding:14px;
        border-radius:12px;
        margin-bottom:8px;">
        🩺 <b>Symptom Checker</b><br>
        <small>Select symptoms and get an ML prediction.</small>
    </div>

    <div style="
        background:rgba(255,255,255,0.10);
        padding:14px;
        border-radius:12px;
        margin-bottom:8px;">
        🤖 <b>AI Health Chat</b><br>
        <small>Ask general health-related questions.</small>
    </div>

    <div style="
        background:rgba(255,255,255,0.10);
        padding:14px;
        border-radius:12px;">
        🛡️ <b>Health Guidance</b><br>
        <small>View general preventive information.</small>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### ⚠️ Medical Disclaimer")

    st.caption(
        "This application is designed for educational purposes. "
        "Predictions should not be considered a medical diagnosis."
    )

    st.divider()

    st.markdown(
        "<center>Made with ❤️ using<br><b>Python • ML • Streamlit • Groq</b></center>",
        unsafe_allow_html=True
    )

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

    <div class="badge">✨ AI-POWERED HEALTH TECHNOLOGY</div>

    <h1>AI Health Assistant</h1>

    <p>
        Explore possible health conditions based on selected symptoms
        using a machine learning model, and get simple educational
        health information through our AI assistant.
    </p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# QUICK STATS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">🧠 ML</div>
        <div class="metric-label">Machine Learning Powered</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">🩺</div>
        <div class="metric-label">Symptom Based Analysis</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">🤖 AI</div>
        <div class="metric-label">Health Information Assistant</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">🔒</div>
        <div class="metric-label">Educational Use</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FEATURES
# =========================================================

st.markdown(
    '<div class="section-title">✨ What can this assistant do?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">A simple interface designed to make health information easier to explore.</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🩺</div>
        <div class="feature-title">Symptom Checker</div>
        <div class="feature-text">
            Select symptoms from the available list and use the
            trained machine learning model to generate a possible
            disease prediction.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Prediction Confidence</div>
        <div class="feature-text">
            When supported by the model, the application displays
            a confidence score to help explain the prediction.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Health Chat</div>
        <div class="feature-text">
            Ask general health questions and receive simple,
            educational information from an AI assistant.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SYMPTOM CHECKER
# =========================================================

st.markdown(
    '<div class="section-title">🩺 Smart Symptom Checker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Tell us what symptoms you are experiencing.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">
    <h3 style="color:#134e4a;">🔍 Select Your Symptoms</h3>
    <p style="color:#64748b;">
        Choose all symptoms that best describe your current condition.
        Selecting more relevant symptoms may help the model produce a prediction.
    </p>
</div>
""", unsafe_allow_html=True)

selected_symptoms = st.multiselect(
    "Symptoms you are experiencing",
    symptoms,
    placeholder="🔎 Search and select symptoms..."
)

# =========================================================
# SELECTED SYMPTOMS
# =========================================================

if selected_symptoms:

    st.markdown("### 📋 Your Selected Symptoms")

    symptom_columns = st.columns(4)

    for i, symptom in enumerate(selected_symptoms):
        with symptom_columns[i % 4]:
            st.markdown(
                f"""
                <div style="
                    background:#ecfdf5;
                    border:1px solid #a7f3d0;
                    border-radius:12px;
                    padding:10px 14px;
                    margin-bottom:10px;
                    color:#065f46;
                    font-size:13px;
                    font-weight:600;">
                    ✓ {symptom}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.info(f"🩺 **{len(selected_symptoms)} symptom(s)** selected.")

# =========================================================
# PREDICTION
# =========================================================

predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])

with predict_col2:

    if st.button(
        "🔍  PREDICT POSSIBLE CONDITION",
        type="primary",
        use_container_width=True
    ):

        if not selected_symptoms:

            st.warning(
                "⚠️ Please select at least one symptom before starting the prediction."
            )

        else:

            # Create model input

            input_data = [0] * len(symptoms)

            for symptom in selected_symptoms:

                index = symptoms.index(symptom)

                input_data[index] = 1

            # Prediction

            prediction = model.predict([input_data])

            disease = label_encoder.inverse_transform(prediction)[0]

            # Confidence

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba([input_data])[0]

                confidence = max(probabilities) * 100

            else:

                confidence = None

            # =================================================
            # RESULT
            # =================================================

            st.markdown("""
            <div class="prediction-card">
                <div class="prediction-label">
                    🔎 MACHINE LEARNING RESULT
                </div>
                <div class="prediction-disease">
                    Possible Condition
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.success(
                f"🩺 Based on the selected symptoms, the model predicts: **{disease}**"
            )

            if confidence is not None:

                c1, c2 = st.columns([1, 2])

                with c1:

                    st.metric(
                        "Model Confidence",
                        f"{confidence:.2f}%"
                    )

                with c2:

                    st.write("### 📊 Confidence Level")

                    st.progress(
                        min(confidence / 100, 1.0)
                    )

                    if confidence >= 80:
                        st.success("High model confidence")

                    elif confidence >= 50:
                        st.warning("Moderate model confidence")

                    else:
                        st.info("Low model confidence")

            # =================================================
            # DISCLAIMER
            # =================================================

            st.markdown("""
            <div class="warning-card">

                <h4>⚠️ Important Health Notice</h4>

                <p>
                    This prediction is generated by a machine learning model
                    and is provided strictly for educational and informational
                    purposes. It is not a medical diagnosis.
                    Please consult a qualified healthcare professional for
                    proper evaluation and treatment.
                </p>

            </div>
            """, unsafe_allow_html=True)

            # =================================================
            # PREVENTIVE RECOMMENDATIONS
            # =================================================

            recommendations = {

                "Fungal infection": [
                    "Keep the affected area clean and dry.",
                    "Avoid sharing towels, clothing, or personal items.",
                    "Wear clean and breathable clothing.",
                    "Consult a healthcare professional if symptoms persist."
                ],

                "Allergy": [
                    "Try to identify and avoid known allergens.",
                    "Keep your surroundings clean and dust-free.",
                    "Avoid exposure to substances that trigger symptoms.",
                    "Seek medical advice if symptoms become severe."
                ],

                "GERD": [
                    "Avoid very large or late meals.",
                    "Limit foods that trigger your symptoms.",
                    "Avoid lying down immediately after eating.",
                    "Maintain healthy eating habits.",
                    "Consult a healthcare professional if symptoms continue."
                ]

            }

            st.markdown(
                '<div class="section-title">🛡️ Preventive Guidance</div>',
                unsafe_allow_html=True
            )

            if disease in recommendations:

                advice_columns = st.columns(2)

                for i, advice in enumerate(recommendations[disease]):

                    with advice_columns[i % 2]:

                        st.markdown(
                            f"""
                            <div class="feature-card">
                                <div class="feature-icon">✅</div>
                                <div class="feature-text">
                                    {advice}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.info(
                    "General preventive information is not available for "
                    "this condition in the current database. Please consult "
                    "a qualified healthcare professional."
                )

# =========================================================
# HOW IT WORKS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">⚙️ How It Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">The application follows a simple three-step process.</div>',
    unsafe_allow_html=True
)

h1, h2, h3 = st.columns(3)

with h1:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">1️⃣</div>

        <div class="feature-title">
            Select Symptoms
        </div>

        <div class="feature-text">
            The user selects one or more symptoms from the
            symptom database.
        </div>

    </div>
    """, unsafe_allow_html=True)

with h2:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">2️⃣</div>

        <div class="feature-title">
            Machine Learning
        </div>

        <div class="feature-text">
            The selected symptoms are converted into numerical
            input and passed to the trained ML model.
        </div>

    </div>
    """, unsafe_allow_html=True)

with h3:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">3️⃣</div>

        <div class="feature-title">
            Prediction
        </div>

        <div class="feature-text">
            The model produces a possible disease prediction
            that is displayed to the user.
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# AI CHATBOT
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">🤖 AI Health Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Have a general health question? Ask the AI assistant.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="chat-card">

    <h3 style="color:#3730a3;">
        💬 Ask your health question
    </h3>

    <p style="color:#6366f1;">
        Get simple, general educational information about health,
        symptoms, wellness, and common conditions.
    </p>

</div>
""", unsafe_allow_html=True)

user_question = st.text_input(
    "Your question",
    placeholder="💡 Example: What are common symptoms of allergies?"
)

# Example questions

st.write("**💡 Try asking:**")

q1, q2, q3 = st.columns(3)

with q1:
    st.caption("What are common allergy symptoms?")

with q2:
    st.caption("How can I stay hydrated?")

with q3:
    st.caption("What causes headaches?")

if st.button(
    "💬 Ask AI Assistant",
    type="primary",
    use_container_width=True
):

    if not user_question.strip():

        st.warning(
            "Please enter a health-related question first."
        )

    else:

        with st.spinner("🤖 AI Assistant is preparing your answer..."):

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

                                "Do not prescribe medication. "

                                "If a user describes serious or urgent symptoms, "

                                "recommend seeking immediate professional medical help. "

                                "Use simple language suitable for general users."

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

                st.markdown("""
                <div class="card">

                    <h3 style="color:#3730a3;">
                        💡 AI Response
                    </h3>

                </div>
                """, unsafe_allow_html=True)

                st.write(answer)

                st.caption(
                    "ℹ️ AI-generated information is for educational purposes only."
                )

            except Exception as e:

                st.error(
                    "The AI assistant could not respond right now."
                )

                st.caption(str(e))

# =========================================================
# EMERGENCY SECTION
# =========================================================

st.divider()

st.markdown("""
<div class="warning-card">

    <h4>🚨 When should you seek emergency medical help?</h4>

    <p>
        If you or someone around you is experiencing potentially
        life-threatening symptoms such as severe difficulty breathing,
        chest pain, loss of consciousness, severe bleeding, sudden
        weakness, or other serious symptoms, seek emergency medical
        assistance immediately.
    </p>

    <p>
        Do not rely on this application for emergency decisions.
    </p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# HEALTH TIPS
# =========================================================

st.markdown(
    '<div class="section-title">🌱 Everyday Health Tips</div>',
    unsafe_allow_html=True
)

t1, t2, t3, t4 = st.columns(4)

tips = [
    ("💧", "Stay Hydrated", "Drink sufficient water throughout the day."),
    ("🥗", "Eat Balanced Meals", "Include nutritious foods and vegetables."),
    ("😴", "Sleep Well", "Maintain a regular and healthy sleep routine."),
    ("🏃", "Stay Active", "Include regular physical activity in your routine.")
]

for col, tip in zip([t1, t2, t3, t4], tips):

    with col:

        st.markdown(
            f"""
            <div class="feature-card">

                <div class="feature-icon">
                    {tip[0]}
                </div>

                <div class="feature-title">
                    {tip[1]}
                </div>

                <div class="feature-text">
                    {tip[2]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# FINAL DISCLAIMER
# =========================================================

st.divider()

st.markdown("""
<div class="info-card">

    <h4 style="color:#1d4ed8;">
        ℹ️ About This Application
    </h4>

    <p style="color:#1e40af; line-height:1.7;">
        AI Health Assistant is an educational machine-learning project
        that demonstrates how artificial intelligence can be used to
        analyze symptom information and provide general health-related
        information.
    </p>

    <p style="color:#1e40af; line-height:1.7;">
        The application does not replace doctors, hospitals, medical
        tests, or professional healthcare services.
    </p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    <strong>🏥 AI-Powered Health Assistant</strong><br><br>

    Machine Learning • Artificial Intelligence • Health Education

    <br><br>

    © 2026 AI Health Assistant | Educational Project

</div>
""", unsafe_allow_html=True)
```
