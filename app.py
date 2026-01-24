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


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Select a user",user_list)

    if st.sidebar.button("Analyze"):
        #stats analysis
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Total messages")
            if selected_user == 'Overall':
                st.subheader(df.shape[0])
            else:
                st.subheader(df[df['user'] == selected_user].shape[0])

        with col2:
            st.subheader("Total words")
            if selected_user == 'Overall':
                st.subheader(df['message'].str.len().sum())
            else:
                st.subheader(df[df['user'] == selected_user]['message'].str.len().sum())

        with col3:
            st.subheader("Total media shared")
            if selected_user == 'Overall':
                st.subheader(df[df['message'] == '<Media omitted>\n'].shape[0])
            else:
                st.subheader(df[df['user'] == selected_user][df['message'] == '<Media omitted>\n'].shape[0])

        