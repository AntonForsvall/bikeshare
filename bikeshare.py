import time
import pandas as pd
import numpy as np
import calendar as cal
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid       inputs
    line = '-'*13
    layout = '-'*48
    month_alt = ['january','february', 'march', 'april', 'may', 'june', 'all']
    day_alt = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    while True:
        city = input('What city do you want to explore? Chicago, New York City or Washington?:  ').lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            month = input(f"""\nWhat month do you want to explore in {city.title()}?
                \n {layout} \n | January  | February  | March     | April     |
                \n {layout} \n | May      | June      | All       |           |
                \n {layout}  \n\n ...  """).lower()
            if month in month_alt:            
                day = input(f"""\nWhat day do you want to explore in {month.title()}?
                    \n {layout} \n | Sunday   | Monday    | Tuesday   | Wednesday |
                    \n {layout} \n | Thursday | Friday    | Saturday  | All       |
                    \n {layout}  \n\n ...  """).lower()
                if day in day_alt:
                    break
                else: 
                    print('I did not really understand that, try again')
                    continue
                
            else:
                print('I did not really understand that, try again')
                continue
        else:
            print('I did not really understand that, try again')
            continue
    # Get user input for month (all, january, february, ... , june)
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = np.bincount(df['month']).argmax()
    print('Most common month:', cal.month_name[common_month])


    # Display the most common day of week
    week_day = df['Start Time'].dt.dayofweek
    common_week = np.bincount(week_day).argmax()
    print('Most common day:', cal.day_name[common_week])

    # Display the most common start hour
    start_hour = df['Start Time'].dt.hour
    common_hour = np.bincount(start_hour).argmax()
    print('Most common start hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df.groupby(['Start Station']).size().nlargest(1)
    print ('Most commonly used', common_start_station.to_string())
    
    # Display most commonly used end station
    common_end_station = df.groupby(['End Station']).size().nlargest(1)
    print ('\nMost commonly used', common_end_station.to_string())
    

    # Display most frequent combination of start station and end station trip
    common_start_end = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print ('\nMost frequent combination of Start and End Station \n' + common_start_end.to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # Display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts().to_string()
    print(f'Number of User Types:\n{user_type}\n')
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_type = df['Gender'].value_counts().to_string()
        print(f'Number of Genders: \n{gender_type}\n')
    

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        earliest = int(birth_year.min())
        most_recent = int(birth_year.max())
        most_common = int(birth_year.value_counts().idxmax())
        print(f'Earliest date of birth: {earliest}')
        print(f'Most Recent date of birth: {most_recent}')
        print(f'Most common year of birth: {most_common}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):
        
        yes = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break
        
        # retrieve and convert data to json format
        # split each json row data 
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
     

if __name__ == "__main__":
	main()