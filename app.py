import joblib
import streamlit as st
import numpy as np
import warnings


warnings.filterwarnings('ignore')

try:
    model = joblib.load("linear_regression_power_model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()


def usage_category(power):
    if power < 1:
        return "Low Usage", "Energy usage is efficient. Maintain current consumption habits."
    elif power < 2:
        return "Medium Usage", "Try turning off unused appliances to reduce electricity consumption."
    else:
        return "High Usage", "High electricity usage detected. Reduce heavy appliance use."


st.title("Electricity Consumption Prediction App")
st.write("Predict next-hour electricity usage based on previous consumption.")

col1, col2, col3 = st.columns(3)

with col1:
    lag_1 = st.number_input(
        "Previous hour power (lag_1)", 
        min_value=0.0, 
        max_value=10.0,
        value=1.2,
        step=0.1,
        format="%.2f"
    )

with col2:
    lag_2 = st.number_input(
        "2 hours before power (lag_2)", 
        min_value=0.0, 
        max_value=10.0,
        value=1.0,
        step=0.1,
        format="%.2f"
    )

with col3:
    lag_3 = st.number_input(
        "3 hours before power (lag_3)", 
        min_value=0.0, 
        max_value=10.0,
        value=0.8,
        step=0.1,
        format="%.2f"
    )


if st.button("Predict", type="primary"):
    try:
        
        input_data = np.array([[float(lag_1), float(lag_2), float(lag_3)]])
        
        
        prediction = model.predict(input_data)[0]
        
     
        category, suggestion = usage_category(prediction)
        
       
        st.subheader("Prediction Result")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Predicted Power", f"{prediction:.3f} kW")
        with col2:
            st.metric("Usage Category", category)
        with col3:
            st.metric("Status", "Calculated")
        
        st.info(f"💡 **Suggestion:** {suggestion}")
        
    except Exception as e:
        st.error(f"Prediction error: {e}")