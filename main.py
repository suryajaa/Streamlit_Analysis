import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file and clean data
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.dropna(inplace=True)  # Handling missing values
    return df

# EDA - Show basic info and statistics
def explore_data(df):
    st.subheader("Data Overview")
    st.write(df.head())
    st.write("**Data Info:**")
    st.write(df.info())
    st.write("**Descriptive Statistics:**")
    st.write(df.describe())

# Key Insights Visualizations
def visualize_insights(df):
    st.subheader("Key Insights")

    # Example Insight 1: Distribution of a Key Column
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if numeric_columns:
        selected_col = st.selectbox("Select a numeric column for distribution", numeric_columns)
        plt.figure(figsize=(8, 4))
        sns.histplot(df[selected_col], kde=True, bins=20)
        st.pyplot(plt)
        st.markdown(f"**Insight:** Distribution of `{selected_col}` reveals the data's spread and possible outliers.")

        # New Insight: Box Plot for Outlier Detection
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[selected_col])
        st.pyplot(plt)
        st.markdown(f"**Insight:** Box plot of `{selected_col}` highlights potential outliers and data distribution.")

    # Example Insight 2: Correlation Heatmap
    if len(numeric_columns) > 1:
        plt.figure(figsize=(10, 6))
        sns.heatmap(df[numeric_columns].corr(), annot=True, cmap='coolwarm')
        st.pyplot(plt)
        st.markdown("**Insight:** Correlation heatmap identifies strong dependencies between features.")

    # Example Insight 3: Trend Analysis (Line Chart)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        plt.figure(figsize=(10, 5))
        df[numeric_columns[0]].plot(title=f'Trend Analysis of {numeric_columns[0]}')
        st.pyplot(plt)
        st.markdown("**Insight:** Trend analysis can highlight seasonality or anomalies.")

# Main Streamlit App
def main():
    st.title("Data Insights Application")
    st.sidebar.header("Upload CSV File")

    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        explore_data(df)
        visualize_insights(df)
    else:
        st.info("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main()
