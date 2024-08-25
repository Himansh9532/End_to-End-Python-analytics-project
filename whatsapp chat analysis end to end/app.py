import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # Fetch Unique Users
    users_list = df["user"].unique().tolist()
    if "group notification" in users_list:
        users_list.remove("group notification")
    users_list.sort()
    users_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", users_list)
    
    if st.sidebar.button("Show Analysis"):
        num_message, words, num_media_messages, num_links  = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics of Whatsapp Chat")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Message")
            st.title(num_message)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Links Shared")
            st.title(num_links)


    if selected_user == "Overall":
        st.title("Most busy Users")
        x,new_df = helper.most_busy_users(df)
        fig , ax = plt.subplots()
        
        
        col1 , col2 = st.columns(2)
        with col1:
            ax.bar(x.index , x.values , color = "red")
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    most_common_df = helper.most_common_words(selected_user , df)
    st.dataframe(most_common_df)
    fig , ax = plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1], color = "orange")
    plt.xticks(rotation = "vertical")
    st.title("Most Common Words")
    st.pyplot(fig)
    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")
    col1 , col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig , ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct= "%0.2f")
        st.pyplot(fig)

    st.title("Monthly timeline Analysis")
    timeline = helper.monthly_timeline(selected_user , df)
    fig , ax = plt.subplots()
    ax.plot(timeline['time'] ,timeline["message"])    
    plt.xticks(rotation = "vertical")
    st.pyplot(fig)
    #daily timeline
    st.title("Daily TIMELINE")
    daily_timeline = helper.daily_timeline(selected_user , df)
    fig , ax = plt.subplots()
    ax.plot(daily_timeline["only_date"] , daily_timeline["message"])
    plt.xticks(rotation = "vertical")
    st.pyplot(fig)
    st.title("Activity Map")
    col1 , col2 = st.columns(2)
    with col1 :
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user , df)
        fig , ax = plt.subplots()
        ax.bar(busy_day.index , busy_day.values , color = "purple")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.month_activity_map(selected_user , df)
        fig ,ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values , color = "pink")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
    st.title("Online Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user , df)
    fig , ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)




    
