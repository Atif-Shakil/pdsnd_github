import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities=['chicago', 'new york city', 'washington']
months=['all', 'january', 'february', 'march', 'april', 'may', 'june']
days=['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            input_city=input('Please select the city.\n[chicago, new york city, washington]\n').lower()
            if input_city in cities:
                city=input_city
                break
            else:
                print('\nPlease enter the correct name.\n')
        except:
            print('\nException occurred.\n')
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            input_month=input('\nPlease select the month.\n[all, january, february, march, april, may , june]\n').lower()
            if input_month in months:
                month=input_month
                break
            else:
                print('\nPlease enter the correct month.\n')
        except:
            print('\nException occurred.\n')
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            input_day=input('\nPlease select the day.\n[all, monday, tuesday, wednesday, thursday, friday, saturday, sunday]\n').lower()
            if input_day in days:
                day=input_day
                break
            else:
                print('\nPlease enter the correct day.\n')
        except:
            print('\nException occurred.\n')
            break

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

    # display the most common month
    most_common_month=df['month'].mode()[0]
    print('The most common month to travel is:\n {}'.format(months[most_common_month].title()))

    # display the most common day of week
    most_common_day=df['day_of_week'].mode()[0]
    print('\nThe most common day of week to travel is:\n {}'.format(most_common_day.title()))

     # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour=df['hour'].mode()[0]
    print('\nThe most common hour to start the journey is:\n {}'.format(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station=df['Start Station'].mode()[0]
    print('The most common station to start the journey is:\n {}'.format(most_common_start_station.title()))

    # display most commonly used end station
    most_common_end_station=df['End Station'].mode()[0]
    print('\nThe most common station to end the journey is:\n {}'.format(most_common_end_station.title()))

    # display most frequent combination of start station and end station trip
    df['Combination']=df['Start Station']+'-'+df['End Station']
    most_common_combination=df['Combination'].mode()[0]
    print('\nThe most frequent combination of start station and end station are:\n Start Staion: {}\n End Station: {}'.format(most_common_combination.split('-')[0].title(), most_common_combination.split('-')[1].title()))
    df.pop('Combination')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_travel=sum(df['Trip Duration'])/60
    print('Total travel time is:\n {} minutes'.format(total_time_travel))

    # display mean travel time
    mean_travel_time=total_time_travel/len(df['Trip Duration'])
    print('\nAverage travel time is:\n {} minutes'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    washington_station='Columbus Circle / Union Station'

    if washington_station in list(df['Start Station']):
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('The user type and their count are:\n{}'.format(user_types))

        print('\nWe are sorry, the gender data and birth year data are only available for Chicago and New York City')

    else:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('The user type and their count are:\n{}'.format(user_types))

        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nThe gender count are:\n {}'.format(gender_count))

        # Display earliest, most recent, and most common year of birth
        earliest_year=df['Birth Year'].min()
        recent_year=df['Birth Year'].max()
        common_year=df['Birth Year'].mode()
        print('\nThe most ealiest birth year is:\n {}\nThe most recent birth year is:\n {}\nThe most common birth year is:\n {}'.format(earliest_year, recent_year, common_year))

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

        lower_limit, upper_limit = 0,5
        while True:
            raw_data = input('\nWould you like to see 5 lines of the raw data? (yes/no)\n')
            if raw_data != 'yes':
                break
            else:
                print(df.iloc[lower_limit:upper_limit])
                lower_limit+=5
                upper_limit+=5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
