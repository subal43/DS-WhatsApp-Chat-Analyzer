import streamlit as st
import preprocessor
from urlextract import URLExtract
from matplotlib import pyplot as plt
import helper
import pandas as pd
from collections import Counter
import re
import seaborn as sns
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

        with col4:
            extractor = URLExtract()
            links = []
            for message in df['message']:
                links.extend(extractor.find_urls(message))
            st.subheader("Total links shared")
            if selected_user == 'Overall':
                st.subheader(len(links))
            else:
                links = pd.Series(links)
                st.subheader(len(links[links.str.contains(selected_user, regex=False)]))


        if selected_user == 'Overall':
            st.title("Most Active Users")
            col1, col2 = st.columns(2)
            temp = df[df['user'] != "group notification"]
            with col1:
                x = temp['user'].value_counts().head()
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                x = round(temp['user'].value_counts().head()/temp.shape[0]*100,2)
                fig, ax = plt.subplots()
                ax.pie(x, labels = x.index, autopct = '%1.1f%%')
                st.pyplot(fig)

        with open("stop_word_for_wp.txt", "r", encoding="utf-8") as f:
            stop_words = f.read()

        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df, stop_words)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        col1, col2 = st.columns(2)
        
        with col1:
            st.title("Most Common Words")
            most_common_words = helper.most_common_words(selected_user, df, stop_words)
            st.dataframe(most_common_words)
        with col2:
            st.title("Most Common Emojis")
            emoji_df = helper.emoji_helper(selected_user, df)
            st.dataframe(emoji_df)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)
    

        st.title("Weekly Activity")
        col1, col2 = st.columns(2)
        with col1:
            st.title("Most busy day")
            week_activity = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(week_activity.index, week_activity.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        
        with col2:
            st.title("Most busy month")
            month_activity = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            sns.countplot(month_activity["month"])
            st.pyplot(fig)

        st.title("Heatmap")
        user_heatmap = helper.user_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap)
        st.pyplot(fig)
