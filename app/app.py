
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Water Potability Prediction",
    page_icon="💧",
    layout="wide"
)

# -------------------------------
# Load ML Model
# -------------------------------
MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "water_potability_final_model.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# -------------------------------
# Main Page
# -------------------------------
st.title("💧 Water Potability Prediction System")

st.markdown("""
### Machine Learning-Based Water Quality Analysis

Enter the physicochemical properties of a water sample below.
The trained machine learning model will predict whether the sample
is potentially potable or non-potable.
""")

st.divider()

# -------------------------------
# Input Section
# -------------------------------
st.subheader("Enter Water Quality Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1
    )

    hardness = st.number_input(
        "Hardness",
        min_value=0.0,
        value=200.0,
        step=1.0
    )

    solids = st.number_input(
        "Solids (ppm)",
        min_value=0.0,
        value=15000.0,
        step=100.0
    )

with col2:
    chloramines = st.number_input(
        "Chloramines",
        min_value=0.0,
        value=7.0,
        step=0.1
    )

    sulfate = st.number_input(
        "Sulfate",
        min_value=0.0,
        value=300.0,
        step=1.0
    )

    conductivity = st.number_input(
        "Conductivity",
        min_value=0.0,
        value=400.0,
        step=1.0
    )

with col3:
    organic_carbon = st.number_input(
        "Organic Carbon",
        min_value=0.0,
        value=10.0,
        step=0.1
    )

    trihalomethanes = st.number_input(
        "Trihalomethanes",
        min_value=0.0,
        value=70.0,
        step=0.1
    )

    turbidity = st.number_input(
        "Turbidity",
        min_value=0.0,
        value=3.0,
        step=0.1
    )

st.divider()

# -------------------------------
# Prediction Section
# -------------------------------
if st.button("🔍 Predict Water Potability", use_container_width=True):

    input_data = pd.DataFrame([{
        "ph": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": chloramines,
        "Sulfate": sulfate,
        "Conductivity": conductivity,
        "Organic_carbon": organic_carbon,
        "Trihalomethanes": trihalomethanes,
        "Turbidity": turbidity
    }])

    prediction = model.predict(input_data)[0]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("✅ Prediction: POTABLE")
        st.markdown("The model predicts that this water sample may be potable.")
    else:
        st.error("⚠️ Prediction: NON-POTABLE")
        st.markdown("The model predicts that this water sample may be non-potable.")

    # Probability if model supports it
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]

        st.write("### Model Prediction Probabilities")

        probability_df = pd.DataFrame({
            "Category": ["Non-Potable", "Potable"],
            "Probability": probabilities
        })

        st.bar_chart(
            probability_df.set_index("Category")
        )

        st.write(
            f"**Non-Potable:** {probabilities[0]*100:.2f}%"
        )

        st.write(
            f"**Potable:** {probabilities[1]*100:.2f}%"
        )

# -------------------------------
# Disclaimer
# -------------------------------
st.divider()

st.warning("""
**Disclaimer:** This project is an educational machine learning prototype.
Predictions are based on the dataset and the trained model.
They are not a certified drinking-water safety assessment.
Always use laboratory testing and applicable official standards
to determine whether water is safe to drink.
""")

st.caption("Water Potability Prediction | Machine Learning Project")
