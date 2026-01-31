import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

def create_wordcloud(selected_user, df , stop_words):
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
    text = " ".join(words)
    wc = WordCloud(width = 800, height = 800, min_font_size = 10, background_color='white').generate(text)
    return wc


def most_common_words(selected_user, df , stop_words):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != "group notification"]
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp["message"] = temp["message"].astype(str).str.replace(r"[^\w\s]", " ", regex=True)

    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(10), columns = ['Word', 'Count'])


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for messages in df["message"]:
        emojis.extend([c for c in messages if c in emoji.EMOJI_DATA])
    return pd.DataFrame(Counter(emojis).most_common(10), columns = ['Emoji', 'Count'])
    

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(["year","month_num","month"]).count()["message"].reset_index()
    times = []
    for i in range(timeline.shape[0]):
        times.append(timeline["month"][i]+" - "+str(timeline["year"][i]))
    timeline["time"] = times
    return timeline

def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df["day_name"].value_counts()