import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score

# Title and description
st.title("AI-Powered Data Analysis & Prediction App")
st.write("""
Upload your dataset, and this app will perform:
1. Data analysis and insights
2. Predictive modeling
""")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the data
    data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Dataset")
    st.dataframe(data)

    # Display data summary
    st.write("### Dataset Summary")
    st.write(data.describe())

    # Check for missing values
    st.write("### Missing Values")
    st.write(data.isnull().sum())

    # Feature selection
    st.write("### Select Features for Prediction")
    target_column = st.selectbox("Select the target column (to predict)", data.columns)
    feature_columns = st.multiselect("Select feature columns", data.columns.drop(target_column))

    if target_column and len(feature_columns) > 0:
        X = data[feature_columns]
        y = data[target_column]

        # Handle missing values (simple imputation)
        X = X.fillna(X.mean())
        y = y.fillna(y.mode()[0])

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Select model type
        st.write("### Select a Prediction Model")
        model_type = st.radio("Choose a model", ("Linear Regression (for numeric targets)", 
                                                 "Random Forest Classifier (for categorical targets)"))

        if model_type == "Linear Regression (for numeric targets)":
            if pd.api.types.is_numeric_dtype(y):
                model = LinearRegression()
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                mse = mean_squared_error(y_test, predictions)
                st.write(f"Mean Squared Error: {mse}")
                st.write("### Predictions")
                st.write(predictions)
            else:
                st.error("Target column must be numeric for Linear Regression.")
        
        elif model_type == "Random Forest Classifier (for categorical targets)":
            if not pd.api.types.is_numeric_dtype(y):
                model = RandomForestClassifier(random_state=42)
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                st.write(f"Accuracy: {accuracy}")
                st.write("### Predictions")
                st.write(predictions)
            else:
                st.error("Target column must be categorical for Random Forest Classifier.")