import calendar
import datetime
import sys

from google_interface import Interface

from bs4 import BeautifulSoup
import requests


def make_datetime(date_str: str, duration_str=None) -> datetime.datetime:
    # date_str format: Tue Oct 4, 8:03 PM
    # duration_str format: 4 min

    timestamp = datetime.datetime.strptime(date_str, "%a %b %d, %I:%M %p")

    year = datetime.date.today().year
    timestamp = timestamp.replace(year=year)

    if duration_str is not None:
        timestamp = timestamp + datetime.timedelta(minutes=int(duration_str.split(" ")[0]))
    return timestamp


# print(CLIENT_ID)

old_stdout = sys.stdout
log_file = open("message.log", "a")
sys.stdout = log_file

print("Running Code")

# URL = "https://spotthestation.nasa.gov/sightings/view.cfm?country=Canada&region=British_Columbia&city=Burnaby#.YzyIf0zMKUk"
#
# html = requests.get(URL)
# html.raise_for_status()
#
# soup = BeautifulSoup(html.text, "html.parser")
#
# rows = soup.find_all(name="tr")
#
# interface = Interface()
#
# months_mapping = {month: index for index, month in enumerate(calendar.month_abbr) if month}
#
# for row in rows[1:]:
#     data = row.find_all(name="td")
#
#     start_timestamp = make_datetime(data[0].getText())
#     end_timestamp = make_datetime(data[0].getText(), data[1].getText())
#
#     max_height = data[2].getText()
#     appears = data[3].getText()
#     disappears = data[4].getText()
#
#     if not interface.check_for_event(start_timestamp):
#         interface.create_event(start_timestamp, end_timestamp, max_height, appears, disappears)

log_file.close()