import pandas as pd
from wordcloud import WordCloud


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width = 800, height = 800, min_font_size = 10, background_color='white').generate(df['message'].str.cat(sep = " "))
    return wc

def stop_word_for_wp():
    with open("stop_word_for_wp.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()
    return stop_words
