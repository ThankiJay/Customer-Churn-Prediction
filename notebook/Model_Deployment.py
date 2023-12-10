# Import libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import joblib
from PIL import Image
from notebook.preprocessing import preprocess

# Load the model from disk
model = joblib.load(r"./notebook/model.sav")

def main():
    # Setting Application title
    st.title('Telco Customer Churn Prediction App')

    # Setting Application description
    st.markdown("""
     :dart:  This Streamlit software is designed to anticipate customer turnover in a telecom use case.
    The program is capable of both realtime and batch data prediction.
    """)
    st.markdown("<h3></h3>", unsafe_allow_html=True)

    # Setting Application sidebar default
    image = Image.open('App.jpg')
    add_selectbox = st.sidebar.selectbox("How would you like to predict?", ("Online", "Batch"))
    st.sidebar.info('This app is created to predict Customer Churn')
    st.sidebar.image(image)

    if add_selectbox == "Online":
        st.info("Input data below")

        # Collecting user inputs for each feature
        gender = st.selectbox('Gender:', ('Male', 'Female'))
        senior_citizen = st.selectbox('Senior Citizen:', ('Yes', 'No'))
        partner = st.selectbox('Partner:', ('Yes', 'No'))
        dependents = st.selectbox('Dependents:', ('Yes', 'No'))
        tenure = st.slider('Tenure (months):', 0, 72, 1)
        phone_service = st.selectbox('Phone Service:', ('Yes', 'No'))
        multiple_lines = st.selectbox('Multiple Lines:', ('Yes', 'No', 'No phone service'))
        internet_service_dsl = st.selectbox('Internet Service (DSL):', ('Yes', 'No'))
        internet_service_fiber_optic = st.selectbox('Internet Service (Fiber Optic):', ('Yes', 'No'))
        internet_service_no = st.selectbox('No Internet Service:', ('Yes', 'No'))
        online_security = st.selectbox('Online Security:', ('Yes', 'No', 'No internet service'))
        online_backup = st.selectbox('Online Backup:', ('Yes', 'No', 'No internet service'))
        device_protection = st.selectbox('Device Protection:', ('Yes', 'No', 'No internet service'))
        tech_support = st.selectbox('Tech Support:', ('Yes', 'No', 'No internet service'))
        streaming_tv = st.selectbox('Streaming TV:', ('Yes', 'No', 'No internet service'))
        streaming_movies = st.selectbox('Streaming Movies:', ('Yes', 'No', 'No internet service'))
        contract_monthly = st.selectbox('Contract (Monthly):', ('Yes', 'No'))
        contract_one_year = st.selectbox('Contract (One Year):', ('Yes', 'No'))
        contract_two_year = st.selectbox('Contract (Two Year):', ('Yes', 'No'))
        paperless_billing = st.selectbox('Paperless Billing:', ('Yes', 'No'))
        payment_method_bank_transfer = st.selectbox('Payment Method (Bank Transfer):', ('Yes', 'No'))
        payment_method_credit_card = st.selectbox('Payment Method (Credit Card):', ('Yes', 'No'))
        payment_method_electronic_check = st.selectbox('Payment Method (Electronic Check):', ('Yes', 'No'))
        payment_method_mailed_check = st.selectbox('Payment Method (Mailed Check):', ('Yes', 'No'))
        monthly_charges = st.number_input('Monthly Charges:', min_value=0.0, max_value=200.0, value=0.0, step=0.01)
        total_charges = st.number_input('Total Charges:', min_value=0.0, max_value=10000.0, value=0.0, step=0.01)

        # Creating a dictionary of the inputs
        data = {
            'gender': gender,
            'SeniorCitizen': senior_citizen,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'IntrntSrvc_DSL': internet_service_dsl,
            'IntrntSrvc_FiberOptic': internet_service_fiber_optic,
            'IntrntSrvc_No': internet_service_no,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract_Monthly': contract_monthly,
            'Contract_OneYear': contract_one_year,
            'Contract_TwoYear': contract_two_year,
            'PaperlessBilling': paperless_billing,
            'PayMthd_BankTransfer': payment_method_bank_transfer,
            'PayMthd_CreditCard': payment_method_credit_card,
            'PayMthd_ElectronicCheck': payment_method_electronic_check,
            'PayMthd_MailedCheck': payment_method_mailed_check,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }

        features_df = pd.DataFrame.from_dict([data])
        st.write('Overview of input is shown below')
        st.dataframe(features_df)

        # Preprocess inputs
        preprocess_df = preprocess(features_df, 'Online')

        prediction = model.predict(preprocess_df)

        if st.button('Predict'):
            if prediction == 1:
                st.warning('Yes, the customer will terminate the service.')
            else:
                st.success('No, the customer is happy with Telco Services.')
    else:
        st.subheader("Dataset upload")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            # Get overview of data
            st.write(data.head())
            st.markdown("<h3></h3>", unsafe_allow_html=True)

            # Preprocess inputs
            preprocess_df = preprocess(data, "Batch")

            if st.button('Predict'):
                # Get batch prediction
                prediction = model.predict(preprocess_df)
                prediction_df = pd.DataFrame(prediction, columns=["Predictions"])

                # Replace numerical predictions with text
                prediction_df['Predictions'] = prediction_df['Predictions'].replace({1: 'Yes', 0: 'No'})

                # Count the number of each prediction for the pie chart
                prediction_counts = prediction_df['Predictions'].value_counts()

                # Define colors for the pie chart
                colors = ['red','green']

                # Create a pie chart
                fig = px.pie(prediction_counts, values=prediction_counts.values, names=prediction_counts.index,
                            title='Customer Churn Predictions', color_discrete_map=colors)

                # Display the pie chart
                st.plotly_chart(fig)

                st.markdown("<h3></h3>", unsafe_allow_html=True)
                st.subheader('Prediction')
                st.write(prediction_df)

if __name__ == '__main__':
        main()