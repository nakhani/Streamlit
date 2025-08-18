import streamlit as st
import pandas as pd
import altair as alt

#sidebar
st.sidebar.title("📊 About This App")
st.sidebar.info("""
Welcome to the Data Science App!
- Upload a CSV file
- View your data in a table
- Visualize it with charts
""")

#title
st.title(" Data Science App")


#upload csv file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    
    #remove space
    df.columns = df.columns.astype(str).str.strip()

    #show table
    st.subheader("Data Preview")
    st.dataframe(df)

    #show information
    st.subheader("Summary Statistics")
    st.write(df.describe())

    #show chart line/bar/scatter
    st.subheader("Chart Visualization")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_columns) >= 2:
        x_axis = st.selectbox("Choose X-axis column", numeric_columns)
        y_axis = st.selectbox("Choose Y-axis column", [col for col in numeric_columns if col != x_axis])
        chart_type = st.radio("Select chart type", ["Line Chart", "Bar Chart", "Scatter Chart"])

        if chart_type == "Line Chart":
            chart = alt.Chart(df).mark_line().encode(
                x=alt.X(x_axis, type='quantitative'),
                y=alt.Y(y_axis, type='quantitative')
            )
        elif chart_type == "Bar Chart":
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_axis, type='quantitative'),
                y=alt.Y(y_axis, type='quantitative')
            )
        elif chart_type == "Scatter Chart":
            chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X(x_axis, type='quantitative'),
                y=alt.Y(y_axis, type='quantitative'),
                tooltip=[x_axis, y_axis]
            ).interactive()

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Please upload a CSV with at least two numeric columns for charting.")
else:
    st.info("Please upload a CSV file to get started.")
