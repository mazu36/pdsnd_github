import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = [ 'january', 'february', 'march', 'avril', 'may', 'june']

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
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        print("\nUse CTRL+C to quit the program \n")
        try:
            city= input("Enter a city (chicago, new york city, washington) : ").lower()
            if city not in CITY_DATA:
                print("Name of the city is incorrect ! Retry a new entry \n")
                continue

            month= input("Enter a month (all, january, february, march, avril, may, june) : ").lower()
            if month != 'all' and month not in MONTHS :
                print("Name of the month is incorrect! Retry a new entry \n")
                continue

            day= input("Enter a day (all, monday, tuesday, ... sunday) : ").lower()
            if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']  :
                print("Name of the day is incorrect ! Retry a new entry\n" )
                continue
            break

        except ValueError as e:
            print ("Error occured {} ".format(e))
            continue
        except KeyboardInterrupt as e:
            city=""
            month=""
            day=""
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

    df  = pd.read_csv(CITY_DATA[city])

    # convert "Start Time" to type datetime:
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # add new columns: month, day_of_weak, hour:
    df["month"] = df['Start Time'].dt.month
    df["day_of_week"] = df['Start Time'].dt.weekday_name
    df["hour"] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTHS.index(month) +1
        df = df[ df['month']== month]

    if day != 'all':
        df=df[df["day_of_week"]== day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    #print("The most common month is: ",df.groupby(['month'])['month'].count().sort_values(ascending=False) )
    calc_month_num=df.groupby(['month'])['month'].count().sort_values(ascending=False).index[0]
    calc_month_name=MONTHS[calc_month_num-1]

    #print("The most common month is: ",df.groupby(['month'])['month'].count().sort_values(ascending=False).index[0])
    print("The most common month is: ", calc_month_num," ",calc_month_name)

    # display the most common day of week
    #print(df.groupby(['day_of_week'])['day_of_week'].count().sort_values(ascending=False) )
    print("The most common day of week is: ",df.groupby(['day_of_week'])['day_of_week'].count().sort_values(ascending=False).index[0])


    # display the most common start hour
    #print(df.groupby(['hour'])['hour'].count().sort_values(ascending=False) )
    print("The most common start hour is: ",df.groupby(['hour'])['hour'].count().sort_values(ascending=False).index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #print(df.groupby(['Start Station'])['Start Station'].count().sort_values(ascending=False) )
    print("The most common start station is: ",df.groupby(['Start Station'])['Start Station'].count().sort_values(ascending=False).index[0])


    # display most commonly used end station
    #print(df.groupby(['End Station'])['End Station'].count().sort_values(ascending=False) )
    print("The most common end station is: ",df.groupby(['End Station'])['End Station'].count().sort_values(ascending=False).index[0])


    # display most frequent combination of start station and end station trip
    #print(df.groupby(['Start Station', 'End Station'])['Start Station'].count().sort_values( ascending=False) )
    print("The most frequent combination of start station and end station trip is: ",
    df.groupby(['Start Station', 'End Station'])['Start Station'].count().sort_values( ascending=False).index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is: ", df['Trip Duration'].sum() )

    # display mean travel time
    print("Mean travel time is: ",df['Trip Duration'].mean() )
    #print(df['Trip Duration'].describe())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #print("Counts of user types:",df['User Type'].unique().size )
    print("Counts of user types:\n",df['User Type'].value_counts())

    if 'Gender' not in df.columns:
        print("\nNo Gender values for this city  !\n" )
    else:
        #print(df[df['Gender'].notnull()]['Gender'].unique().size)
        print("\nCounts of gender:\n",df['Gender'].value_counts())

    if 'Birth Year' not in df.columns:
        print("\nNo Birth Year values for this city  !\n" )
    else:
        # Display earliest, most recent, and most common year of birth
        print("\n STATISTICS on Birth Year:")
        print("\n",df['Birth Year'].describe())
        print('\nEarliest year of birth',df['Birth Year'].min())
        print('\nMost recent year of birth',df['Birth Year'].max())
        print('\nMost common year of birth',df['Birth Year'].mean())
        #print('\nMost common year of birth bis',df.groupby(['Birth Year'])['Birth Year'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    The main function contains:
        user's input;
        aggregated statistics output;
        detailed data output
    """
    while True:
        city, month, day = get_filters()
        if city =="":
            print("End of the program ...")
            break

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        curr_step=5
        curr_iloc=0

        while True:
            try:

                if curr_iloc == 0:
                    lbl_message="Do you want to see the first 5 rows of data ? Enter yes or no :\n"
                else:
                    lbl_message="Do you want to see the next 5 rows of data ? Enter yes or no :\n"

                view_raw_data = input(lbl_message).lower()
                if view_raw_data not in [ 'yes', 'no']:
                    print('Answer is incorrect ! "yes" or "no" are equired. Retry a new entry \n')
                    continue

                if view_raw_data == "yes":
                    print(df.iloc[curr_iloc : curr_iloc + curr_step])
                    curr_iloc += curr_step

                else:
                    break

            except ValueError as e:
                print ("Error occured {} ".format(e))
                continue
            except KeyboardInterrupt as e:
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    # Call the main function
	main()
