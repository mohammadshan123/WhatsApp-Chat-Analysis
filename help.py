from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df['message'].str.contains('<Media omitted>', na=False).sum()

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_userss(df):
    x = df['users'].value_counts().head()
    df_percent = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})
    return x, df_percent

def create_wordcloud(selected_users, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    temp['cleaned'] = temp['message'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(" ".join(temp['cleaned'].dropna().astype(str)))
    return df_wc

def most_common_words(selected_users, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])

def emoji_helper(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])

def monthly_timeline(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    return df['day_name'].value_counts()

def month_activity_map(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    return df['month'].value_counts()

def activity_heatmap(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
