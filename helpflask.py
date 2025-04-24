from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import emoji
import os
import seaborn as sns

extract = URLExtract()
STATIC_DIR = "static"

def fetch_stats(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

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

    path = os.path.join(STATIC_DIR, "wordcloud.png")
    plt.figure(figsize=(8, 8))
    plt.imshow(df_wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

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

    word_freq = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])

    path = os.path.join(STATIC_DIR, "common_words.png")
    plt.figure(figsize=(10, 6))
    plt.barh(word_freq['Word'][::-1], word_freq['Count'][::-1], color='skyblue')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def emoji_helper(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])

    top_emoji_df = emoji_df.head(10)

    path = os.path.join(STATIC_DIR, "emoji.png")
    plt.figure(figsize=(8, 5))
    plt.bar(top_emoji_df['Emoji'], top_emoji_df['Count'], color='orange')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return emoji_df, path

def monthly_timeline(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    path = os.path.join(STATIC_DIR, "monthly_timeline.png")
    plt.figure(figsize=(10, 6))
    plt.plot(timeline['time'], timeline['message'], marker='o')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def daily_timeline(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    daily = df.groupby('only_date').count()['message'].reset_index()

    path = os.path.join(STATIC_DIR, "daily_timeline.png")
    plt.figure(figsize=(10, 6))
    plt.plot(daily['only_date'], daily['message'], color='purple')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def week_activity_map(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    week_activity = df['day_name'].value_counts()

    path = os.path.join(STATIC_DIR, "busy_day.png")
    plt.figure(figsize=(8, 6))
    week_activity.plot(kind='bar', color='teal')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def month_activity_map(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    month_activity = df['month'].value_counts()

    path = os.path.join(STATIC_DIR, "busy_month.png")
    plt.figure(figsize=(8, 6))
    month_activity.plot(kind='bar', color='coral')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def activity_heatmap(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    heatmap_data = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    path = os.path.join(STATIC_DIR, "heatmap.png")
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='YlGnBu')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def most_busy_userss(df):
    x = df['users'].value_counts().head()
    df_percent = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})

    path = os.path.join(STATIC_DIR, "most_busy_users.png")
    plt.figure(figsize=(10, 6))
    x.plot(kind='bar', color='slateblue')
    plt.xlabel("Users")
    plt.ylabel("Message Count")
    plt.title("Most Active Users")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return x, df_percent, path
