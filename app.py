import streamlit as st
import preprocessor
st.title("WhatsApp Chat Analyzer")
st.sidebar.header("Upload your chat file")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("File uploaded successfully")
    data = uploaded_file.read().decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)