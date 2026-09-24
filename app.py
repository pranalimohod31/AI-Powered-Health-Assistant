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
# LOAD MODEL
# =========================================================

try:
    model = joblib.load("models/health_model.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")
    symptoms = joblib.load("models/symptoms.pkl")

except Exception as e:
    st.error("❌ Model files could not be loaded.")
    st.caption(f"Details: {e}")
    st.stop()

# =========================================================
# GROQ CLIENT
# =========================================================

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    client = None

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN APP ---------- */

    .stApp {
        background:
            radial-gradient(circle at top left, #e0f7f4 0%, transparent 35%),
            radial-gradient(circle at bottom right, #dbeafe 0%, transparent 35%),
            #f8fafc;
        color: #172033;
    }

    /* ---------- TEXT ---------- */

    .stApp p,
    .stApp span,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #172033;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #0f766e,
            #0d9488,
            #14b8a6
        );
        padding: 45px 35px;
        border-radius: 28px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 12px 35px rgba(15,118,110,0.20);
    }

    .hero h1,
    .hero p {
        color: white !important;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
    }

    /* ---------- OPTION CARDS ---------- */

    .option-card {
        background: rgba(255,255,255,0.95);
        padding: 25px;
        border-radius: 22px;
        min-height: 210px;
        box-shadow: 0 7px 25px rgba(15,23,42,0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-bottom: 20px;
    }

    .option-card h2,
    .option-card h3,
    .option-card p {
        color: #172033 !important;
    }

    .option-card:hover {
        transform: translateY(-3px);
    }

    .option-icon {
        font-size: 45px;
    }

    /* ---------- INFO CARDS ---------- */

    .info-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #0f766e;
        box-shadow: 0 5px 20px rgba(0,0,0,0.06);
        margin: 15px 0;
    }

    .info-card h3,
    .info-card p {
        color: #172033 !important;
    }

    /* ---------- RESULT ---------- */

    .result-card {
        background: #ecfdf5;
        border: 2px solid #5eead4;
        padding: 30px;
        border-radius: 24px;
        text-align: center;
        margin: 25px 0;
        box-shadow: 0 8px 25px rgba(15,118,110,0.10);
    }

    .result-card h1,
    .result-card h2,
    .result-card p {
        color: #0f766e !important;
    }

    /* ---------- EMERGENCY ---------- */

    .emergency-card {
        background: #fff1f2;
        border: 2px solid #fb7185;
        padding: 25px;
        border-radius: 22px;
        margin: 20px 0;
    }

    .emergency-card h2,
    .emergency-card p,
    .emergency-card li {
        color: #881337 !important;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #f0fdfa,
            #f8fafc
        );
    }

    section[data-testid="stSidebar"] * {
        color: #172033;
    }

    /* ---------- INPUTS ---------- */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: white !important;
        border-color: #cbd5e1 !important;
    }

    div[data-baseweb="select"] input,
    div[data-baseweb="input"] input,
    textarea {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }

    div[data-baseweb="select"] span {
        color: #172033 !important;
    }

    ul[role="listbox"],
    ul[role="listbox"] li {
        background-color: white !important;
        color: #172033 !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 13px;
        font-weight: 700;
        min-height: 45px;
    }

    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        padding: 30px;
        color: #64748b;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <div style="font-size:65px;">🏥</div>
            <h2>AI Health Assistant</h2>
            <p>Smart • Simple • Educational</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Explore")

    pages = [
        "🏠 Home",
        "🩺 Symptom Checker",
        "❤️ Health Risk",
        "💊 Medicine Info",
        "🥗 Diet & Wellness",
        "🧠 Mental Wellness",
        "🤖 AI Health Chat",
        "📊 Health Dashboard",
        "🚨 Emergency Guide",
        "ℹ️ About"
    ]

    selected_page = st.radio(
        "Choose a service",
        pages,
        label_visibility="collapsed"
    )

    st.session_state.page = selected_page

    st.divider()

    st.warning(
        "⚠️ This application provides educational "
        "information only and does not replace "
        "professional medical advice."
    )

# =========================================================
# HOME
# =========================================================

if st.session_state.page == "🏠 Home":

    st.markdown(
        """
        <div class="hero">
            <h1>🏥 AI Health Assistant</h1>
            <p>
                Your intelligent health education companion
                powered by Machine Learning and Artificial Intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 👋 Welcome!")

    st.write(
        "Choose a health service below to get started. "
        "The platform combines machine learning, AI-powered "
        "conversation and educational health resources."
    )

    st.markdown("## ✨ What would you like help with?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="option-card">
                <div class="option-icon">🩺</div>
                <h3>Symptom Checker</h3>
                <p>
                    Select your symptoms and get a possible
                    condition prediction from the ML model.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Symptom Checker",
            key="home_symptom",
            use_container_width=True
        ):
            st.session_state.page = "🩺 Symptom Checker"
            st.rerun()

    with c2:
        st.markdown(
            """
            <div class="option-card">
                <div class="option-icon">❤️</div>
                <h3>Health Risk</h3>
                <p>
                    Explore lifestyle and general health
                    risk factors through educational questions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Health Risk",
            key="home_risk",
            use_container_width=True
        ):
            st.session_state.page = "❤️ Health Risk"
            st.rerun()

    with c3:
        st.markdown(
            """
            <div class="option-card">
                <div class="option-icon">🤖</div>
                <h3>AI Health Chat</h3>
                <p>
                    Ask general health questions and receive
                    simple educational information.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Chat with AI",
            key="home_chat",
            use_container_width=True
        ):
            st.session_state.page = "🤖 AI Health Chat"
            st.rerun()

    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown(
            """
            <div class="option-card">
                <div class="option-icon">💊</div>
                <h3>Medicine Info</h3>
                <p>
                    Learn general educational information
                    about commonly used medicines.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore Medicines",
            key="home_medicine",
            use_container_width=True
        ):
            st.session_state.page = "💊 Medicine Info"
            st.rerun()

    with c5:
        st.markdown(
            """
            <div class="option-card">
                <div class="option-icon">🥗</div>
                <h3>Diet & Wellness</h3>
                <p>
                    Explore basic nutrition, hydration,
                    exercise and lifestyle guidance.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore Wellness",
            key="home_diet",
            use_container_width=True
        ):
            st.session_state.page = "🥗 Diet & Wellness"
            st.rerun()

    with c6:
        st.markdown(
            """
            <div class="option-card">
                <div class="option-icon">🧠</div>
                <h3>Mental Wellness</h3>
                <p>
                    Explore simple stress-management and
                    relaxation resources.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore Wellness",
            key="home_mental",
            use_container_width=True
        ):
            st.session_state.page = "🧠 Mental Wellness"
            st.rerun()

    st.divider()

    st.markdown("## 🔐 Privacy & Safety")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.info("🔒 **Privacy**\n\nAvoid entering sensitive personal information.")

    with p2:
        st.info("🧠 **Educational AI**\n\nAI responses are informational, not diagnoses.")

    with p3:
        st.info("👨‍⚕️ **Professional Care**\n\nConsult healthcare professionals for medical concerns.")

# =========================================================
# SYMPTOM CHECKER
# =========================================================

elif st.session_state.page == "🩺 Symptom Checker":

    st.markdown(
        """
        <div class="hero">
            <h1>🩺 Smart Symptom Checker</h1>
            <p>
                Use our trained machine learning model
                to explore possible health conditions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Select the symptoms you are currently experiencing. "
        "The result is an educational ML prediction and not a diagnosis."
    )

    selected_symptoms = st.multiselect(
        "🔎 Choose your symptoms",
        symptoms,
        placeholder="Search and select symptoms..."
    )

    if selected_symptoms:

        st.markdown("### 📋 Selected Symptoms")

        cols = st.columns(4)

        for i, symptom in enumerate(selected_symptoms):

            with cols[i % 4]:
                st.success(f"✓ {symptom}")

        st.info(
            f"🩺 {len(selected_symptoms)} symptom(s) selected."
        )

    if st.button(
        "🔍 PREDICT POSSIBLE CONDITION",
        type="primary",
        use_container_width=True
    ):

        if not selected_symptoms:

            st.warning(
                "⚠️ Please select at least one symptom first."
            )

        else:

            try:

                input_data = [0] * len(symptoms)

                for symptom in selected_symptoms:

                    index = symptoms.index(symptom)
                    input_data[index] = 1

                prediction = model.predict([input_data])

                disease = label_encoder.inverse_transform(
                    prediction
                )[0]

                confidence = None

                if hasattr(model, "predict_proba"):

                    probabilities = model.predict_proba(
                        [input_data]
                    )[0]

                    confidence = max(probabilities) * 100

                # Save history

                st.session_state.prediction_history.append(
                    {
                        "Condition": disease,
                        "Symptoms": len(selected_symptoms),
                        "Confidence": (
                            f"{confidence:.2f}%"
                            if confidence is not None
                            else "N/A"
                        )
                    }
                )

                st.markdown(
                    f"""
                    <div class="result-card">
                        <h2>🔎 Possible Condition</h2>
                        <h1>{disease}</h1>
                        <p>
                            Based on the symptoms selected.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if confidence is not None:

                    st.markdown("### 📊 Model Confidence")

                    st.progress(
                        min(confidence / 100, 1.0)
                    )

                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}%"
                    )

                # Guidance database

                recommendations = {

                    "Fungal infection": [
                        "Keep the affected area clean and dry.",
                        "Avoid sharing towels or personal items.",
                        "Wear clean and breathable clothing.",
                        "Consult a healthcare professional if symptoms persist."
                    ],

                    "Allergy": [
                        "Try to identify and avoid known allergens.",
                        "Keep your surroundings clean.",
                        "Avoid substances that trigger symptoms.",
                        "Seek medical advice if symptoms become severe."
                    ],

                    "GERD": [
                        "Avoid very large or late meals.",
                        "Limit foods that trigger symptoms.",
                        "Avoid lying down immediately after eating.",
                        "Consult a healthcare professional if symptoms continue."
                    ]
                }

                st.markdown("## 🛡️ Preventive Guidance")

                if disease in recommendations:

                    for advice in recommendations[disease]:
                        st.write(f"✅ {advice}")

                else:

                    st.info(
                        "General preventive information is not available "
                        "for this condition in the current database."
                    )

                st.warning(
                    """
                    ⚠️ **Important Health Notice**

                    This result is generated by a machine learning
                    model for educational purposes only.

                    **It is not a medical diagnosis and should not
                    be used to make treatment decisions.**

                    Please consult a qualified healthcare professional
                    for proper evaluation.
                    """
                )

            except Exception as e:

                st.error("❌ Prediction failed.")
                st.caption(f"Details: {e}")

# =========================================================
# HEALTH RISK
# =========================================================

elif st.session_state.page == "❤️ Health Risk":

    st.markdown(
        """
        <div class="hero">
            <h1>❤️ Health Risk Assessment</h1>
            <p>
                Explore general lifestyle and wellness risk factors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "This section provides educational lifestyle feedback. "
        "It does not calculate a clinical diagnosis or medical risk score."
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    activity = st.selectbox(
        "🏃 Physical activity",
        [
            "Very active",
            "Moderately active",
            "Occasionally active",
            "Mostly inactive"
        ]
    )

    sleep = st.selectbox(
        "😴 Average sleep",
        [
            "7–9 hours",
            "5–6 hours",
            "Less than 5 hours",
            "More than 9 hours"
        ]
    )

    water = st.selectbox(
        "💧 Daily hydration",
        [
            "Usually adequate",
            "Sometimes inadequate",
            "Often inadequate"
        ]
    )

    smoking = st.selectbox(
        "🚭 Smoking",
        [
            "No",
            "Occasionally",
            "Regularly"
        ]
    )

    if st.button(
        "📊 ASSESS LIFESTYLE",
        type="primary",
        use_container_width=True
    ):

        points = 0

        if activity == "Mostly inactive":
            points += 2
        elif activity == "Occasionally active":
            points += 1

        if sleep in ["5–6 hours", "Less than 5 hours"]:
            points += 1

        if water == "Often inadequate":
            points += 1

        if smoking == "Regularly":
            points += 2
        elif smoking == "Occasionally":
            points += 1

        if points <= 1:
            message = "Your selected lifestyle factors look relatively balanced."
        elif points <= 3:
            message = "Some lifestyle areas may benefit from improvement."
        else:
            message = "Several lifestyle areas may benefit from attention."

        st.markdown(
            f"""
            <div class="result-card">
                <h2>🌱 Lifestyle Feedback</h2>
                <h2>{message}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 💡 General Wellness Tips")

        st.write("✅ Aim for regular physical activity.")
        st.write("✅ Maintain a consistent sleep schedule.")
        st.write("✅ Stay adequately hydrated.")
        st.write("✅ Avoid tobacco products.")
        st.write("✅ Seek professional advice for persistent concerns.")

# =========================================================
# MEDICINE INFO
# =========================================================

elif st.session_state.page == "💊 Medicine Info":

    st.markdown(
        """
        <div class="hero">
            <h1>💊 Medicine Information</h1>
            <p>
                Explore general educational information about medicines.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "⚠️ This section does not recommend medicines or dosages. "
        "Always follow advice from a qualified healthcare professional."
    )

    medicine_data = {

        "Paracetamol": {
            "use": "Commonly used for pain and fever.",
            "precaution": "Excessive use can cause serious liver injury."
        },

        "Ibuprofen": {
            "use": "Commonly used for pain, inflammation and fever.",
            "precaution": "May not be suitable for everyone, including some people with stomach, kidney or cardiovascular conditions."
        },

        "Cetirizine": {
            "use": "An antihistamine commonly used for allergy symptoms.",
            "precaution": "May cause drowsiness in some people."
        },

        "Omeprazole": {
            "use": "Reduces stomach acid and is commonly used for acid-related conditions.",
            "precaution": "Persistent symptoms should be evaluated by a healthcare professional."
        }
    }

    medicine = st.selectbox(
        "🔎 Select a medicine",
        list(medicine_data.keys())
    )

    if medicine:

        data = medicine_data[medicine]

        st.markdown(
            f"""
            <div class="info-card">
                <h3>💊 {medicine}</h3>
                <p><b>General use:</b> {data["use"]}</p>
                <p><b>Important:</b> {data["precaution"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# DIET & WELLNESS
# =========================================================

elif st.session_state.page == "🥗 Diet & Wellness":

    st.markdown(
        """
        <div class="hero">
            <h1>🥗 Diet & Wellness</h1>
            <p>
                Explore simple healthy lifestyle guidance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    goal = st.selectbox(
        "🎯 What is your wellness goal?",
        [
            "General wellness",
            "Healthy eating",
            "Better hydration",
            "More physical activity",
            "Better sleep"
        ]
    )

    advice = {

        "General wellness": [
            "Eat a varied and balanced diet.",
            "Stay physically active.",
            "Get adequate sleep.",
            "Stay hydrated."
        ],

        "Healthy eating": [
            "Include fruits and vegetables.",
            "Choose a variety of whole foods.",
            "Limit highly processed foods.",
            "Pay attention to portion sizes."
        ],

        "Better hydration": [
            "Drink fluids regularly throughout the day.",
            "Increase fluids when appropriate for heat or activity.",
            "Water is generally a good everyday beverage."
        ],

        "More physical activity": [
            "Start with manageable activity.",
            "Take regular movement breaks.",
            "Choose activities you enjoy.",
            "Increase activity gradually."
        ],

        "Better sleep": [
            "Maintain a regular sleep schedule.",
            "Create a relaxing bedtime routine.",
            "Limit stimulating activities before bedtime.",
            "Keep your sleeping environment comfortable."
        ]
    }

    st.markdown(f"### 🌱 Suggestions for {goal}")

    for item in advice[goal]:
        st.success(f"✓ {item}")

# =========================================================
# MENTAL WELLNESS
# =========================================================

elif st.session_state.page == "🧠 Mental Wellness":

    st.markdown(
        """
        <div class="hero">
            <h1>🧠 Mental Wellness</h1>
            <p>
                Simple tools for relaxation, reflection and
                everyday stress management.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    mood = st.select_slider(
        "How are you feeling today?",
        options=[
            "Very low",
            "Low",
            "Okay",
            "Good",
            "Very good"
        ]
    )

    st.write(f"Current selection: **{mood}**")

    st.markdown("### 🌿 Quick Relaxation Exercise")

    if st.button(
        "🧘 Start Breathing Exercise",
        use_container_width=True
    ):

        st.success(
            "Breathe in slowly for 4 seconds → "
            "hold for 4 seconds → "
            "breathe out slowly for 6 seconds. "
            "Repeat several times."
        )

    st.markdown("### 💡 Everyday Wellness Ideas")

    st.write("🌱 Take a short break from screens.")
    st.write("🚶 Go for a short walk.")
    st.write("🎵 Listen to calming music.")
    st.write("💬 Talk to someone you trust.")
    st.write("😴 Maintain a regular sleep routine.")

    st.info(
        "If you are experiencing severe emotional distress "
        "or feel that you may be in immediate danger, seek "
        "urgent professional or emergency support."
    )

# =========================================================
# AI HEALTH CHAT
# =========================================================

elif st.session_state.page == "🤖 AI Health Chat":

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 AI Health Chat</h1>
            <p>
                Ask general health education questions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "The AI provides general educational information. "
        "It does not diagnose conditions or prescribe treatment."
    )

    question = st.text_area(
        "💬 Your question",
        placeholder=(
            "Example: What are common symptoms of allergies?"
        ),
        height=120
    )

    if st.button(
        "💬 ASK AI ASSISTANT",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        elif client is None:

            st.error(
                "Groq API key is not configured. "
                "Please check your Streamlit secrets."
            )

        else:

            with st.spinner(
                "🤖 AI Assistant is preparing your answer..."
            ):

                try:

                    response = client.chat.completions.create(

                        model="llama-3.1-8b-instant",

                        messages=[

                            {
                                "role": "system",
                                "content": (
                                    "You are a health education assistant. "
                                    "Provide clear, simple and cautious "
                                    "general health information. "
                                    "Do not diagnose users. "
                                    "Do not prescribe medication or dosage. "
                                    "Do not claim certainty. "
                                    "For emergency symptoms, recommend "
                                    "immediate professional medical help."
                                )
                            },

                            {
                                "role": "user",
                                "content": question
                            }
                        ],

                        temperature=0.3,
                        max_tokens=600
                    )

                    answer = response.choices[0].message.content

                    st.markdown("### 💡 AI Response")

                    st.markdown(
                        f"""
                        <div class="info-card">
                            {answer}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption(
                        "ℹ️ AI-generated information is for educational purposes only."
                    )

                except Exception as e:

                    st.error(
                        "❌ The AI assistant could not respond."
                    )

                    st.caption(
                        f"Details: {e}"
                    )

# =========================================================
# HEALTH DASHBOARD
# =========================================================

elif st.session_state.page == "📊 Health Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>📊 Health Dashboard</h1>
            <p>
                Review your activity within this session.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    total_checks = len(
        st.session_state.prediction_history
    )

    st.metric(
        "🩺 Symptom Checks",
        total_checks
    )

    if total_checks > 0:

        st.markdown("### 📋 Recent Predictions")

        for item in reversed(
            st.session_state.prediction_history
        ):

            st.markdown(
                f"""
                <div class="info-card">
                    <h3>🔎 {item["Condition"]}</h3>
                    <p>
                        Symptoms selected: {item["Symptoms"]}
                    </p>
                    <p>
                        Model confidence: {item["Confidence"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No symptom-check history is available yet. "
            "Use the Symptom Checker to begin."
        )

# =========================================================
# EMERGENCY GUIDE
# =========================================================

elif st.session_state.page == "🚨 Emergency Guide":

    st.markdown(
        """
        <div class="hero">
            <h1>🚨 Emergency Guide</h1>
            <p>
                Recognize situations that may require urgent medical attention.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="emergency-card">

        <h2>🚨 Seek Emergency Medical Help</h2>

        <p>Urgent medical assessment may be needed for symptoms such as:</p>

        <ul>
            <li>Severe difficulty breathing</li>
            <li>Severe or persistent chest pain</li>
            <li>Sudden loss of consciousness</li>
            <li>Signs of a stroke such as sudden weakness or difficulty speaking</li>
            <li>Severe bleeding</li>
            <li>Severe allergic reaction with breathing difficulty or swelling</li>
        </ul>

        <p>
        If you believe you are experiencing a medical emergency,
        contact your local emergency service or seek immediate
        medical attention.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.error(
        "⚠️ Do not rely on this application during a medical emergency."
    )

# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "ℹ️ About":

    st.markdown(
        """
        <div class="hero">
            <h1>ℹ️ About the Project</h1>
            <p>
                AI-Powered Health Assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🎯 Project Objective")

    st.write(
        "The AI Health Assistant is an educational application "
        "that combines machine learning and generative AI to "
        "provide users with accessible health information."
    )

    st.markdown("## 🧠 Technologies Used")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info("🐍 Python")

    with c2:
        st.info("🧠 Machine Learning")

    with c3:
        st.info("🤖 Groq AI")

    with c4:
        st.info("🌐 Streamlit")

    st.markdown("## 🔬 Main Components")

    st.write("• Machine Learning disease prediction")
    st.write("• Symptom-based analysis")
    st.write("• Generative AI health chatbot")
    st.write("• Educational health resources")
    st.write("• Lifestyle guidance")
    st.write("• Session-based prediction history")

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        <b>🏥 AI-Powered Health Assistant</b>

        <br><br>

        Machine Learning • Artificial Intelligence • Health Education

        <br><br>

        ⚠️ Educational project — not a substitute for professional medical advice.

        <br><br>

        © 2026 AI Health Assistant

    </div>
    """,
    unsafe_allow_html=True
)


