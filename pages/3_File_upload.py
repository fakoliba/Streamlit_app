import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from scipy.stats import chi2_contingency
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# Title and description
st.title("CSV File Analysis App")
st.markdown("""
**This Streamlit app is designed for analyzing CSV files. It allows users to upload a CSV file and perform various data analysis and visualization tasks. The main features of the app include:**

**File Upload:** Users can upload a CSV file for analysis.

**Data Analysis:**

- **Display the raw data from the uploaded CSV file.**
- **Show the shape of the data (number of rows and columns).**
- **Display the data types of each column.**
- **Provide summary statistics for the data.**

**Missing Value Analysis:**

- **Display the number of missing values in each column.**

**Data Cleanup:**

- **Option to drop rows with missing values.**
- **Option to fill missing values with the mean of the column.**
- **Option to drop selected columns from the dataset.**

**Data Visualization:**

- **Plot the distribution of a selected numeric column.**
- **Plot scatter plots for selected columns.**
- **Plot box plots for selected columns.**

**Correlation Heatmaps:**

- **Show correlation heatmaps for selected numeric columns.**
- **Show correlation heatmaps for selected categorical columns based on frequency distributions.**

**Recommendations Section:**

- **Generate recommendations based on clusters.**
- **Perform K-Means clustering on selected columns.**
- **Visualize the clusters.**
- **Provide cluster-based recommendations, summarizing the characteristics of each cluster based on the selected columns.**

**The app provides an interactive and user-friendly interface for performing basic data analysis, visualization, and generating insights from CSV files.**
""")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.write(df)

    # Data Analysis
    st.subheader("Data Analysis")
    st.write("Shape of the data:", df.shape[0], 'Rows', 'and', df.shape[1],'Columns')
    st.write("Data Types:", df.dtypes)
    st.write("Summary Statistics:")
    st.write(df.describe())

    # Missing Values
    st.subheader("Missing Value Analysis")
    st.write("Number of missing values in each column:")
    st.write(df.isnull().sum())

    # Data Cleanup
    st.subheader("Data Cleanup")
    if st.checkbox("Drop rows with missing values"):
        df = df.dropna()
        st.write("Rows with missing values dropped. Updated Data:")
        st.write(df)

    if st.checkbox("Fill missing values with column mean"):
        df = df.fillna(df.mean())
        st.write("Missing values filled with column mean. Updated Data:")
        st.write(df)

    if st.checkbox("Drop columns"):
        columns_to_drop = st.multiselect("Select columns to drop", df.columns)
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            st.write("Selected columns dropped. Updated Data:")
            st.write(df)

    # Visualizations
    st.subheader("Data Visualization")
    if st.checkbox("Plot Column Distribution"):
        column = st.selectbox("Select a column", df.select_dtypes(include=['float64', 'int64']).columns)
        plt.hist(df[column], bins=20, color='blue', edgecolor='black')
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        st.pyplot(plt)

    if st.checkbox("Plot Scatter Plot"):
        col1 = st.selectbox("Select X-axis column", df.columns)
        col2 = st.selectbox("Select Y-axis column", df.columns)
        plt.scatter(df[col1], df[col2], alpha=0.7)
        plt.title(f'{col1} vs {col2}')
        plt.xlabel(col1)
        plt.ylabel(col2)
        st.pyplot(plt)

    if st.checkbox("Plot Box Plot"):
        column = st.selectbox("Select a column for Box Plot", df.select_dtypes(include=['float64', 'int64']).columns)
        plt.boxplot(df[column], vert=False)
        plt.title(f'Box Plot of {column}')
        plt.xlabel(column)
        st.pyplot(plt)

    # Correlation Heatmaps
    st.subheader("Correlation Heatmap")
    if st.checkbox("Show Correlation Heatmap"):
        # Numeric correlations
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if not numeric_cols.empty:
            st.write("Select numeric columns to include in the correlation:")
            selected_numeric_cols = st.multiselect("Numeric Columns", numeric_cols, default=numeric_cols)
            if selected_numeric_cols:
                corr_numeric = df[selected_numeric_cols].corr()
                st.write("Correlation for Selected Numeric Columns:")
                st.write(corr_numeric)

                fig, ax = plt.subplots()
                sns.heatmap(corr_numeric, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
                plt.title("Numeric Correlation Heatmap")
                st.pyplot(fig)
            else:
                st.write("No numeric columns selected for correlation.")

        # Categorical correlations
        categorical_cols = df.select_dtypes(exclude=['float64', 'int64']).columns
        if len(categorical_cols) > 0:
            st.write("Select categorical columns to include in the correlation:")
            selected_categorical_cols = st.multiselect("Categorical Columns", categorical_cols, default=categorical_cols)
            if selected_categorical_cols:
                categorical_data = df[selected_categorical_cols]
                cat_corr = pd.DataFrame(index=selected_categorical_cols, columns=selected_categorical_cols)

                for col1 in selected_categorical_cols:
                    for col2 in selected_categorical_cols:
                        if col1 == col2:
                            cat_corr.loc[col1, col2] = 1.0
                        else:
                            # Measure "correlation" by comparing shared frequency distributions
                            crosstab = pd.crosstab(categorical_data[col1], categorical_data[col2])
                            chi2 = chi2_contingency(crosstab)[0]
                            n = crosstab.sum().sum()
                            phi2 = chi2 / n
                            r, k = crosstab.shape
                            corr_value = np.sqrt(phi2 / min(k-1, r-1))
                            cat_corr.loc[col1, col2] = corr_value

                st.write("Correlation for Selected Categorical Columns:")
                st.write(cat_corr)
                fig, ax = plt.subplots()
                sns.heatmap(cat_corr.astype(float), annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
                plt.title("Categorical Correlation Heatmap (Based on Frequency)")
                st.pyplot(fig)
            else:
                st.write("No categorical columns selected for correlation.")

    # Recommendations Section
    st.subheader("Recommendations")
    if st.checkbox("Generate Recommendations"):
        # Example: Generate recommendations based on clusters
        st.write("Generating recommendations based on clusters...")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        selected_columns = st.multiselect("Select columns for clustering", numeric_cols, default=numeric_cols)
        
        if len(selected_columns) >= 2:
            st.write("Performing K-Means Clustering...")
            k = st.slider("Select number of clusters (k)", min_value=2, max_value=10, value=3)
            model = KMeans(n_clusters=k, random_state=42)
            clusters = model.fit_predict(df[selected_columns].dropna())
            df["Cluster"] = clusters
            st.write("Clustered Data:")
            st.write(df)

            # Visualize clusters
            st.write("Cluster Visualization")
            plt.figure(figsize=(10, 6))
            for cluster in range(k):
                cluster_data = df[df["Cluster"] == cluster]
                plt.scatter(cluster_data[selected_columns[0]], cluster_data[selected_columns[1]], label=f"Cluster {cluster}")
            plt.legend()
            plt.xlabel(selected_columns[0])
            plt.ylabel(selected_columns[1])
            plt.title("K-Means Clustering")
            st.pyplot(plt)

            # Recommendations
            st.subheader("Cluster-Based Recommendations")
            st.write("Here are some recommendations based on the clusters:")
            for cluster in range(k):
                st.write(f"**Cluster {cluster}:**")
                st.write(f"Mean values:\n{df[df['Cluster'] == cluster][selected_columns].mean()}")
                st.write(f"Summary:\nCluster {cluster} has the following characteristics based on the selected columns:")
                for col in selected_columns:
                    mean_value = df[df['Cluster'] == cluster][col].mean()
                    st.write(f"- The average {col} is {mean_value:.2f}")
                st.write("\n")