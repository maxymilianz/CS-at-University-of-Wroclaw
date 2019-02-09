from datetime import date, timedelta
import matplotlib.pyplot as plt
import sys


def parse_date(string):
    year, month, day = [int(number) for number in string.split('-')]
    return date(year, month, day)


def get_filename(date):
    return 's_d_t_' + (str(date.month) if date.month >= 10 else ('0' + str(date.month))) + '_' + str(date.year) + '.csv'


def get_day_data(date):
    with open(get_filename(date), 'r') as file:
        for line in file.readlines():
            parameters = line.split(',')
            if int(parameters[4][1:-1]) == date.day:
                return float(parameters[9]), float(parameters[11])


def get_1_day_data(day):
    result = []

    for _ in range(10):
        result.append(get_day_data(day))
        day = date(day.year, day.month - 1, day.day)     # works only for 2018, so it's fine that this may become negative :)

    return result


def plot_1_day(date):
    data = get_1_day_data(date)
    plt.plot(data)
    plt.show()


def get_data(from_date, to_date):
    result = []
    date = from_date

    while date != to_date:
        result.append(get_day_data(date))
        date += timedelta(days = 1)

    result.append(get_day_data(date))
    return result


def plot(from_date, to_date):
    data = get_data(from_date, to_date)
    plt.plot(data)
    plt.show()


def main():
    if len(sys.argv) == 2:
        plot_1_day(parse_date(sys.argv[1]))
    elif len(sys.argv) == 3:
        plot(parse_date(sys.argv[1]), parse_date(sys.argv[2]))
    else:
        raise Exception('Wrong number of arguments')


main()