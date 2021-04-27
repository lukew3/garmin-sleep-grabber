# garmin-sleep-grabber
Fetches your sleep data from Garmin Connect and saves in a csv file 

## Usage
1. Clone the repository
2. Install dependencies by using `pip install -r requirements.txt`
3. Edit the config.ini to your preferences. You must set email and password to your garmin connect login credentials and set the start date fields to the first day of sleep that you want to retrieve. The program will get all sleep data from that date to today's date and add it to `sleepdata.csv`
4. Run `python main.py`. It may take some time to retrieve all data; it took me about 2 minutes for 2 years.
