from urlextract import URLExtract
import pandas as pd
from collections import Counter
import seaborn as sns
import emoji
# Initialize the URL extractor
extractor = URLExtract()

def fetch_stats(selected_user, df):
    # Filter the DataFrame to include only messages from the selected user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    # Calculate the number of messages
    num_messages = df.shape[0]
    
    # Calculate the total number of words
    words = []
    for message in df["message"]:
        words.extend(message.split())
    
    # Count the number of media messages (e.g., images, videos, etc.)
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # Extract and count the number of links
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
    
    # Return the calculated statistics
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df["user"].value_counts().head()
    # Calculate the percentage of messages sent by each user
    new_df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"}
    )
    return x, new_df
def most_common_words(selected_user , df):
    f = open("stop_hinglish (2).txt" , "r")
    stop_words = f.read()  
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    temp = df[df["user"] != "group notification" ]
    temp = temp[temp["message"]!= "<Media omitted>\n"]
    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_words =  pd.DataFrame(Counter(words).most_common(25))
    return most_common_words
def emoji_helper(selected_user , df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def monthly_timeline(selected_user , df):
    if selected_user != "Overall":
         df = df[df['user'] == selected_user]
    timeline = df.groupby(["Year","month_num" ,"Month"]).count()["message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["Month"][i] + "-" +str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user , df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby("only_date").count()["message"].reset_index()
    return daily_timeline
def week_activity_map(selected_user , df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df["day_name"].value_counts()

def month_activity_map(selected_user , df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df["Month"].value_counts()
def activity_heatmap(selected_user , df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index= "day_name" , columns = "period" , values = "message" , aggfunc = "count").fillna(0)
    return user_heatmap




