import streamlit as st
import textwrap
import joblib
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide"
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
# CSS
# =========================================================

st.markdown(
    textwrap.dedent("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #f8fbff, #eef7f6);
        color: #172033;
    }

    /* Global text contrast */
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #172033;
    }

    /* Keep icons/emoji visually natural */
    .main-title h1,
    .main-title p,
    .main-title {
        color: #ffffff !important;
    }

    /* Streamlit inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important;
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

    /* Dropdown menu */
    ul[role="listbox"],
    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #172033 !important;
    }

    /* White cards need dark text */
    .card,
    .feature {
        color: #172033 !important;
    }

    .card *,
    .feature * {
        color: #172033 !important;
    }

    /* Result card keeps its heading readable */
    .result h1,
    .result h2,
    .result p {
        color: #0f766e !important;
    }

    /* Sidebar readability */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
    }

    section[data-testid="stSidebar"] * {
        color: #172033;
    }

    /* Buttons */
    .stButton > button {
        font-weight: 700;
        border-radius: 12px;
    }

    .main-title {
        background: linear-gradient(135deg, #0f766e, #14b8a6);
        padding: 40px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    .main-title h1 {
        font-size: 45px;
        margin-bottom: 10px;
    }

    .main-title p {
        font-size: 18px;
    }

    .card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }

    .result {
        background: #ecfdf5;
        border: 2px solid #5eead4;
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        text-align: center;
    }

    .result h2 {
        color: #0f766e;
    }

    .warning {
        background: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }

    .feature {
        background: white;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        min-height: 150px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.06);
    }

    </style>
    """),
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        textwrap.dedent("""
        <div style="text-align:center;">
            <div style="font-size:60px;">🏥</div>
            <h2>AI Health Assistant</h2>
            <p>Smart • Simple • Educational</p>
        </div>
        """),
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.info(
        """
        🩺 **Symptom Checker**

        Select your symptoms and get a possible condition prediction.
        """
    )

    st.info(
        """
        🤖 **AI Health Chat**

        Ask general health-related questions.
        """
    )

    st.divider()

    st.warning(
        "This application is for educational purposes only. "
        "It does not provide a medical diagnosis."
    )

# =========================================================
# HERO
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="main-title">
        <h1>🏥 AI Health Assistant</h1>
        <p>
            Explore possible health conditions using machine learning
            and get simple educational health information.
        </p>
    </div>
    """),
    unsafe_allow_html=True
)

# =========================================================
# FEATURES
# =========================================================

st.markdown("## ✨ What can this assistant do?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        textwrap.dedent("""
        <div class="feature">
            <h2>🩺</h2>
            <h3>Symptom Checker</h3>
            <p>
                Select symptoms and use the trained ML model
                to predict a possible condition.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        textwrap.dedent("""
        <div class="feature">
            <h2>📊</h2>
            <h3>Prediction</h3>
            <p>
                View the predicted condition and model confidence
                when available.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        textwrap.dedent("""
        <div class="feature">
            <h2>🤖</h2>
            <h3>AI Health Chat</h3>
            <p>
                Ask general health questions and receive
                educational information.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

# =========================================================
# SYMPTOM CHECKER
# =========================================================

st.divider()

st.markdown("## 🩺 Smart Symptom Checker")

st.write(
    "Select all the symptoms that you are experiencing."
)

selected_symptoms = st.multiselect(
    "🔎 Choose symptoms",
    symptoms,
    placeholder="Search and select symptoms..."
)

# =========================================================
# SELECTED SYMPTOMS
# =========================================================

if selected_symptoms:

    st.markdown("### 📋 Selected Symptoms")

    cols = st.columns(4)

    for i, symptom in enumerate(selected_symptoms):

        with cols[i % 4]:

            st.success(f"✓ {symptom}")

    st.info(
        f"🩺 {len(selected_symptoms)} symptom(s) selected."
    )

# =========================================================
# PREDICTION BUTTON
# =========================================================

st.markdown("")

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

            # Create input vector
            input_data = [0] * len(symptoms)

            for symptom in selected_symptoms:

                index = symptoms.index(symptom)

                input_data[index] = 1

            # Make prediction
            prediction = model.predict([input_data])

            disease = label_encoder.inverse_transform(
                prediction
            )[0]

            # Calculate confidence
            confidence = None

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(
                    [input_data]
                )[0]

                confidence = max(probabilities) * 100

            # =================================================
            # RESULT
            # =================================================

            st.markdown(
                f"""
                <div class="result">
                    <h2>🔎 Possible Condition</h2>
                    <h1>{disease}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success(
                f"🩺 The machine learning model predicts: **{disease}**"
            )

            # =================================================
            # CONFIDENCE
            # =================================================

            if confidence is not None:

                st.markdown("### 📊 Model Confidence")

                st.progress(
                    min(confidence / 100, 1.0)
                )

                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )

                if confidence >= 80:

                    st.success(
                        "High model confidence"
                    )

                elif confidence >= 50:

                    st.warning(
                        "Moderate model confidence"
                    )

                else:

                    st.info(
                        "Low model confidence"
                    )

            # =================================================
            # RECOMMENDATIONS
            # =================================================

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

            # =================================================
            # DISCLAIMER
            # =================================================

            st.markdown(
                
                <div class="warning">
                    <h3>⚠️ Important Health Notice</h3>

                    <p>
                    This prediction is generated by a machine learning
                    model and is provided only for educational and
                    informational purposes.
                    </p>

                    <p>
                    It is not a medical diagnosis. Please consult
                    a qualified healthcare professional for proper
                    evaluation and treatment.
                    </p>
                </div>
                
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error("❌ Prediction failed.")

            st.caption(f"Details: {e}")

# =========================================================
# HOW IT WORKS
# =========================================================

st.divider()

st.markdown("## ⚙️ How It Works")

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        textwrap.dedent("""
        <div class="feature">
            <h2>1️⃣</h2>
            <h3>Select Symptoms</h3>
            <p>
                The user selects symptoms from the available
                symptom database.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        textwrap.dedent("""
        <div class="feature">
            <h2>2️⃣</h2>
            <h3>Machine Learning</h3>
            <p>
                The selected symptoms are converted into
                numerical input for the trained model.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        textwrap.dedent("""
        <div class="feature">
            <h2>3️⃣</h2>
            <h3>Prediction</h3>
            <p>
                The model generates a possible condition
                based on the selected symptoms.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

# =========================================================
# AI CHATBOT
# =========================================================

st.divider()

st.markdown("## 🤖 AI Health Assistant")

st.write(
    "Ask a general health-related question."
)

user_question = st.text_input(
    "💬 Your question",
    placeholder="Example: What are common symptoms of allergies?"
)

if st.button(
    "💬 Ask AI Assistant",
    use_container_width=True
):

    if not user_question.strip():

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
                                "You are a helpful health education assistant. "
                                "Give clear and simple general health information. "
                                "Do not diagnose users. "
                                "Do not prescribe medication. "
                                "If serious or emergency symptoms are described, "
                                "recommend immediate professional medical help."
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

                st.markdown("### 💡 AI Response")

                st.write(answer)

                st.caption(
                    "ℹ️ AI-generated information is for educational purposes only."
                )

            except Exception as e:

                st.error(
                    "❌ The AI assistant could not respond."
                )

                st.caption(f"Details: {e}")

# =========================================================
# EMERGENCY SECTION
# =========================================================

st.divider()

st.markdown(
    textwrap.dedent(
    <div class="warning">

        <h3>🚨 Emergency Medical Help</h3>

        <p>
        If someone is experiencing potentially life-threatening
        symptoms such as severe difficulty breathing, chest pain,
        loss of consciousness, severe bleeding, or sudden weakness,
        seek emergency medical assistance immediately.
        </p>

        <p>
        Do not rely on this application for emergency decisions.
        </p>

    </div>
    ),
    unsafe_allow_html=True
)

# =========================================================
# HEALTH TIPS
# =========================================================

st.markdown("## 🌱 Everyday Health Tips")

tips = [
    ("💧", "Stay Hydrated", "Drink sufficient water throughout the day."),
    ("🥗", "Eat Balanced Meals", "Include nutritious foods and vegetables."),
    ("😴", "Sleep Well", "Maintain a regular and healthy sleep routine."),
    ("🏃", "Stay Active", "Include regular physical activity in your routine.")
]

cols = st.columns(4)

for col, tip in zip(cols, tips):

    with col:

        st.markdown(
            textwrap.dedent(f"""
            <div class="feature">
                <h2>{tip[0]}</h2>
                <h3>{tip[1]}</h3>
                <p>{tip[2]}</p>
            </div>
            """),
            unsafe_allow_html=True
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    textwrap.dedent("""
    <div style="text-align:center; padding:20px; color:#64748b;">
        <b>🏥 AI-Powered Health Assistant</b>
        <br><br>
        Machine Learning • Artificial Intelligence • Health Education
        <br><br>
        © 2026 AI Health Assistant | Educational Project
    </div>
    """),
    unsafe_allow_html=True
)
