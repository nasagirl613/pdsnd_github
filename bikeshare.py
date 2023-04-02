#import necessary libraries
import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True: #Convert user input to lowercase and check for acceptable user input; if acceptable, break from while loop, if incorrect, prompt user for valid entry until acceptable input is received.
        city = input("Please enter the name of the city you would like to explore: Chicago, New York City, or Washington? ").lower()
        if city in ["chicago", "new york city", "washington"]:
            break
        else:
            print("Invalid input. Please enter a valid city name.")

    # get user input for month (all, january, february, ... , june)
    while True: #Convert user input to lowercase and check for acceptable user input; if acceptable, break from while loop, if incorrect, prompt user for valid entry until acceptable input is received.
        month = input("Please enter the month you would like to explore (January - June), or 'all' to see all months: ").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: #Convert user input to lowercase and check for acceptable user input; if acceptable, break from while loop, if incorrect, prompt user for valid entry until acceptable input is received.
        day = input("Please enter the day of the week you would like to explore, or 'all' to see all days: ").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print("Invalid input. Please enter a valid day of the week or 'all'.")

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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

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

    # Ask the user if they want to see 5 rows of raw data at a time
    display = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n')
    start_loc = 0

    # Display data in batches of 5 rows
    while display.lower() == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        display = input("Do you wish to continue?: ").lower()

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("Most Common Month:", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("Most Common Day of Week:", common_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station:", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most Commonly Used End Station:", common_end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Station'] = df['Start Station'] + ' to ' + df['End Station']
    common_start_end_station = df['Start-End Station'].mode()[0]
    print("Most Frequent Combination of Start and End Station Trip:", common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time:", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("\nCounts of User Types:\n", user_counts)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)
    else:
        print("\nNo gender data available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print("\nEarliest Birth Year:", earliest_birth_year)

        most_recent_birth_year = int(df['Birth Year'].max())
        print("Most Recent Birth Year:", most_recent_birth_year)

        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("Most Common Birth Year:", most_common_birth_year)
    else:
        print("\nNo birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
