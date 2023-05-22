import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
    while city not in CITY_DATA.keys():
        print('Please Enter a Valid City')
        city = input("choose a city to see data for Chicago, New York, or Washington? ")

    # get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "june"]
    while True:

        month = input("choose a month: (all, january, february, ... , june). ").lower()
        if month in months:
            break
        else:
            print("Invalid input!")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "monday", "tuesday", "sunday", "thursday", "friday", "saturday", "sunday"]
    while True:

        day = input("choose a day: (all, monday, tuesday, ... sunday). ").lower()
        if day in days:
            break
        else:
            print("Invalid input!")

    print('-' * 40)
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
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["start hour"] = df["Start Time"].dt.hour

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
    print("The most common month is {}".format(df['month'].mode()[0]))

    # display the most common day of week
    print("The most common day of week is {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("The most common hour is {}".format(df['start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most commonly used start station: {}".format(df["Start Station"].mode()[0]))

    # display most commonly used end station
    print("most commonly used end station: {}".format(df["End Station"].mode()[0]))

    # display most frequent combination of start station and end station trip
    df["most_freq_combo"] = df["Start Station"] + df["End Station"]
    print("most frequent combination of start station and end station trip: {}".format(df["most_freq_combo"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("total travel time: ", (df["Trip Duration"].sum()).round())

    # display mean travel time
    print("mean travel time: ", round((df["Trip Duration"].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print(user_types)

    # Display counts of gender
    if city != "washington":
        gender = df['Gender'].value_counts().to_frame()
        print(gender)

        # Display earliest, most recent, and most common year of birthN

        earliest = np.min(df['Birth Year'])
        print(f"the earliest date of birth: {earliest}")
        most_recent = np.max(df['Birth Year'])
        print(f"the most recent date of birth: {most_recent}")
        most_common = df['Birth Year'].mode()[0]
        print(f"the most recent date of birth: {most_common}")
    else:
        print("data is not available for washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """
    displays the raw data from a DataFrame 5 rows at a time, based on user input(yes or no)
    """

    user_input = input("Would you like to see the first 5 rows of the data? Type 'yes' or 'no': ").lower()

    while user_input not in ['yes', 'no']:
        print("Please enter a valid choice.")
        user_input = input("Would you like to see the first 5 rows of the data? Type 'yes' or 'no': ").lower()

    if user_input == 'yes':
        index = 0

        while index + 5 < df.shape[0]:
            print(df.iloc[index:index + 5])
            index += 5
            user_input = input("If you would like to see more rows of the data, type 'yes': ").lower()

            if user_input != 'yes':
                print('Thank you.')
                break

    else:
        print("Thank you.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
