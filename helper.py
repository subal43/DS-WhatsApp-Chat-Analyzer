import pandas as pd
from wordcloud import WordCloud
from collections import Counter

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width = 800, height = 800, min_font_size = 10, background_color='white').generate(df['message'].str.cat(sep = " "))
    return wc

def stop_word_for_wp():
    with open("stop_word_for_wp.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()
    return stop_words

def most_common_words(selected_user, df):
    with open("stop_word_for_wp.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != "group notification"]
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp["message"] = temp["message"].astype(str).str.replace(r"[^\w\s\U0001F300-\U0001FAFF\u2600-\u27BF]", " ", regex=True) 
    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(10), columns = ['Word', 'Count'])
    