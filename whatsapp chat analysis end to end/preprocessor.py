import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Define the pattern to match date and time
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    
    # Split data into messages and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    # Create a DataFrame
    df = pd.DataFrame({"user_message": messages, "message_date": dates})
    
    # Clean and format the date column
    df["message_date"] = df["message_date"].str.strip(" -")
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%y, %H:%M")
    
    # Initialize user and message lists
    users = []
    messages = []
    
    # This loop processes each message
    for msg in df["user_message"]:
        entry = re.split(r"([\w\W]+?):\s", msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append("group notification")
            messages.append(entry[0])
    
    # Adding user and message columns to DataFrame
    df["user"] = users
    df["message"] = messages
    
    # Dropping the original user_message column
    df.drop(columns=["user_message"], inplace=True)
    
    # Extracting date and time information
    df["Year"] = df["message_date"].dt.year
    df["Month"] = df["message_date"].dt.month_name()
    df["Day"] = df["message_date"].dt.day
    df["hour"] = df["message_date"].dt.hour
    df["minute"] = df["message_date"].dt.minute
    df["month_num"] = df["message_date"].dt.month
    df["only_date"] = df["message_date"].dt.date
    df["day_name"] = df["message_date"].dt.day_name()
    period = []
    for hour in df[['day_name' , 'hour']]['hour']:
        if hour == 23:
           period.append(str(hour) + "-"+str("00"))
        elif hour == 0:
           period.append(str("00") + "-"+str(hour+1))
        else :
            period.append(str(hour) + "-"+str(hour+1))
    df['period'] = period
        


    return df

# Example usage
if __name__ == "__main__":
    with open("chat.txt", "r", encoding="utf-8") as f:
        data = f.read()
    
    df = preprocess(data)
    print(df.head())  # This will print the first few rows of the DataFrame
