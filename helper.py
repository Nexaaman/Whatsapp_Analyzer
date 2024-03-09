from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['person'].value_counts().head()
    df = round((df['person'].value_counts() / df.shape[0]) * 100,2).reset_index().rename(columns={'count': 'Percent', 'person': 'Name'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]

    temp = df[df['person'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open("stop_hinglish.txt",'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]

    temp = df[df['person'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['person'] == selected_user]

    return df['month'].value_counts()
