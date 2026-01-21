import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,3},\s\d{1,2}:\d{2}\s?[AP]M\s-\s'
    msg = re.split(pattern,data)[1:]
    import unicodedata

    clean = [
        unicodedata.normalize("NFKC", m)
        for m in re.findall(pattern, data)
    ]
    df = pd.DataFrame({"user messages" : msg , "date" : clean})
    df['date'] = pd.to_datetime(df['date'],format = "%m/%d/%y, %I:%M %p - ")

    users = []
    messages = []

    for msg in df['user messages']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

    df = df.iloc[2:].reset_index(drop=True)
    df['user'] = users
    df['message'] = messages

    df.drop(columns = ['user messages'],inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df