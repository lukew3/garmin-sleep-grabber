from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)
import datetime, json, csv, configparser

config = configparser.ConfigParser()
config.read('config.ini')
YOUR_EMAIL = config['CONFIG']['email']
YOUR_PASSWORD = config['CONFIG']['password']
START_YEAR = int(config['CONFIG']['start_year'])
START_MONTH = int(config['CONFIG']['start_month'])
START_DATE = int(config['CONFIG']['start_date'])

rows = []

try:
    client = Garmin(YOUR_EMAIL, YOUR_PASSWORD)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client init")
    quit()

print("Logging in...")
try:
    client.login()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client login: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client login")
    quit()

def add_sleep_by_date(date):
    output = client.get_sleep_data(date)
    data = output["dailySleepDTO"]

    date = data["calendarDate"]
    total_time = data["sleepTimeSeconds"]
    start_time = data["sleepStartTimestampGMT"]
    end_time = data["sleepEndTimestampGMT"]

    try:
        hours_slept = round((total_time / 3600), 3)
        start_clock = (datetime.datetime.fromtimestamp(start_time/1000)).isoformat()[-8:]
        end_clock = (datetime.datetime.fromtimestamp(end_time/1000)).isoformat()[-8:]
    except Exception as e:
        hours_slept = "0"
        start_clock = "0"
        end_clock = "0"

    print(date)
    print(hours_slept)
    print(start_clock)
    print(end_clock)
    print("-------")
    rows.append([date, hours_slept, start_clock, end_clock])


def main():
    filename = "sleepdata.csv"
    fields = ['Date', 'Hours', 'Start', 'End']
    #START_DATE = "2019-08-10"
    start_date = datetime.datetime(START_YEAR, START_MONTH, START_DATE)
    present_date = datetime.datetime.now() - datetime.timedelta(days=1)
    working_date = start_date
    while working_date < present_date:
        working_date += datetime.timedelta(days=1)
        add_sleep_by_date(working_date.isoformat())
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

if __name__ == "__main__":
    main()
