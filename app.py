import streamlit as st
st.title("WhatsApp Chat Analyzer")
st.sidebar.header("Upload your chat file")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("File uploaded successfully")
    data = uploaded_file.read().decode("utf-8")
    st.text(data)