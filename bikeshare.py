import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'D:\python\chicago.csv',
              'new york city': 'D:\python\new_york_city.csv',
              'washington': 'D:\python\washington.csv' }
CITY_DIC = ['chicago', 'new york city', 'washington']
MONTH_DIC = ['all','jan', 'feb', 'mar', 'apr', 'may', 'june']
WEEKEND_DIC = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
IS_CONTINUE = ['y','n']

def get_UserInput():
    print('Welcome to analyze the bikeshare data in the first half of 2017!')
    # Get cityinfo   test git v2
    city = input('Please input cityname，such as \'chicago\', \'new york city\', \'washington\': ').lower()
    while city not in CITY_DIC:
        city = input ("Input message error! Please input cityname，such as \'chicago\', \'new york city\', \'washington\':").lower()

    # Get Month  test git v2
    month = input('Please input month,such as \'all\', \'jan\', \'feb\', \'mar\', \'apr\', \'may\', \'june\': ').lower()
    while month not in MONTH_DIC:
        month = input('Input message error! Please input month,such as \'all\', \'jan\', \'feb\', \'mar\', \'apr\', \'may\', \'june\': ').lower()

    # Get weekend
    day = input('Please input weekend, such as \'all\', \'monday\', \'tuesday\', \'wednesday\', \'thursday\', \'friday\', \'saturday\', \'sunday\': ').lower()
    while day not in WEEKEND_DIC:
        month = input('Input message error! Please input weekend, such as \'all\', \'monday\', \'tuesday\', \'wednesday\', \'thursday\', \'friday\', \'saturday\', \'sunday\':').lower()
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # Get data
    df = pd.read_csv(CITY_DATA[city])

    # Convert date
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert month
    df['month'] = df['Start Time'].dt.month

    # Filter
    if month != 'all':
        month = MONTH_DIC.index(month)
        df = df[df['month'] == month]
    
    # Filter
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def popular_time(df):
    start_time = time.time()

    # most common month
    print("most common month: ", MONTH_DIC[int(df['month'].value_counts().idxmax())])

    # most common day of week
    print("most common day of week: ", df['day_of_week'].value_counts().idxmax())

    # most common hour of day
    print("most common hour of day: ", df['Start Time'].dt.hour.value_counts().idxmax())

    print("\nIt takes %s seconds." % (time.time() - start_time))
    print('-'*40)


def popular_station(df):
    start_time = time.time()

    # most common start station
    print("most common start station: ", df ['Start Station'].value_counts().idxmax())

    # most common end station
    print("The most common end station is: ", df['End Station'].value_counts().idxmax())

    # most common trip from start to end
    print("most common trip from start to end:", df.groupby(['Start Station', 'End Station']).size().nlargest(1))
    
    print("\nIt tasks %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration(df):
    start_time = time.time()

    # total travel time
    print("total travel time %s hours " % (df['Trip Duration'].sum() / 3600.0))

    # average travel time
    print("average travel time %s hours " % (df['Trip Duration'].mean() / 3600.0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def userinfo(df):
    start_time = time.time()

    # counts of each user type
    print("counts of each user type: ", df['User Type'].value_counts())

    # counts of each gender 
    print("counts of each gender: ", df['Gender'].value_counts())
    
    # earliest, most recent, most common year of birth 
    print("earliest, most recent, most common year of birth: ", int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].value_counts().idxmax()))

    print("\nIt tasks %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_userlist(df):
    pageIndex = 0
    pageSize = 5
    pageCount = df['month'].shape[0]
    while True:
        view_more = input("Do you want to see more raw data? Type 'y' to see, type 'n' to break.").lower()
        while view_more not in IS_CONTINUE:
            city = input ("Input message error! Please type 'y' to see more, type 'n' to break.").lower()
        if view_more == 'n':
            return
        if pageCount >=  pageIndex + pageSize + 1:
            print(df.iloc[pageIndex : pageIndex + pageSize])
            pageIndex = pageIndex + pageSize
        else:
            print(df.iloc[pageIndex : pageCount - 1])
            print("There are not more data!")
            return
        

def main():
    while True:
        city, month, day = get_UserInput()
        df = load_data(city, month, day)

        popular_time(df)
        popular_station(df)
        trip_duration(df)
        if city != 'washington':
            userinfo(df)
        get_userlist(df)

        restart = input('\nThis query has been completed. Input \'y\' to continue to query, input \'n\' to break.\n')
        while restart not in IS_CONTINUE:
            restart = input('\nInput message error! This query has been completed. Input \'y\' to continue to query, input \'n\' to break.\n')
        if restart.lower() == 'n':
            break


if __name__ == "__main__":
    main()