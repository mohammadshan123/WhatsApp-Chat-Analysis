import re
import pandas as pd



# Preprocess function to clean and structure WhatsApp chat
def preprocess(data):
    # Define a general pattern for the different date formats
    patterns = [
        r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}[\u202f\s]?[APMapm]{2}",  # MM/DD/YY, HH:MM AM/PM format
        r"\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}[:\d]{0,2}\s?[APMapm]{2}\]",  # [MM/DD/YY, HH:MM AM/PM]
        r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}[:\d]{0,2}\s?[APMapm]{2}",  # Another general MM/DD/YY format
    ]
    
    # Try to find all matching timestamps using the patterns
    for pattern in patterns:
        dates = re.findall(pattern, data)
        if dates:
            print("Dates found:", dates)  # Debugging line
            break
    else:
        print("No matching dates found.")  # Debugging line

    if not dates:
        return pd.DataFrame()  # Early return if no dates are found

    messages = re.split(pattern, data)[1:]
    print("Messages found:", messages)  # Debugging line

    # Clean each date string by removing \u202f
    cleaned_dates = [d.replace('\u202f', '') for d in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': cleaned_dates})

    # convert message_date type
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M%p")
    except Exception as e:
        print(f"Error converting date: {e}")
        return pd.DataFrame()  # Return empty DataFrame if date conversion fails

    df['message_date'] = df['message_date'].dt.strftime("%m/%d/%Y, %I:%M %p")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Ensure 'date' is in string format
    df['date'] = df['date'].astype(str)
    try:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y, %I:%M %p', errors='coerce')
    except Exception as e:
        print(f"Error converting date: {e}")
        return pd.DataFrame()  # Return empty DataFrame if date conversion fails

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.strftime('%I')  # Extract hour in 12-hour format (01-12)
    df['minute'] = df['date'].dt.strftime('%M')  # Extract minute
    df['AM_PM'] = df['date'].dt.strftime('%p')  # Extract AM/PM

    df['date'] = df['date'].dt.strftime('%m/%d/%Y, %I:%M %p')

    period = []
    for index, row in df.iterrows():
        hour = int(row['hour'])
        hour_in_12hr = hour % 12  # Converts hour to 12-hour format (0-11)
        am_pm = 'AM' if hour < 12 else 'PM'

        if hour == 0:
            period.append(str('12') + " AM - " + str('01') + " AM")
        elif hour == 12:
            period.append(str('12') + " PM - " + str('01') + " PM")
        else:
            next_hour_in_12hr = (hour + 1) % 12
            next_am_pm = 'AM' if (hour + 1) < 12 else 'PM'
            period.append(f"{hour_in_12hr} {am_pm} - {next_hour_in_12hr} {next_am_pm}")

    df['period'] = period
    print("Processed DataFrame:", df)  # Debugging line
    return df
