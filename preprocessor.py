import re
import pandas as pd

def preprocess(data):
    # Pattern to match the date format and split the messages
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]  # Remove the first empty element
    dates = re.findall(pattern, data)

    # Debug: Print the first few elements of messages and dates
    print("First few messages:", messages[:5])
    print("First few dates:", dates[:5])
    print("Messages length:", len(messages))
    print("Dates length:", len(dates))

    # Ensure the lengths of messages and dates are the same
    if len(messages) != len(dates):
        raise ValueError("Messages and dates lists are not of the same length")

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Debug: Print the DataFrame before date conversion
    print("DataFrame before date conversion:")
    print(df.head())

    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Debug: Print the DataFrame after date conversion
    print("DataFrame after date conversion:")
    print(df.head())

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 1:  # user name
            users.append(entry[1])
            messages.append("".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period

    # Debug: Print the final DataFrame
    print("Final DataFrame:")
    print(df.head())

    return df
