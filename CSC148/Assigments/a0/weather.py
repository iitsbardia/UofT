"""
Assignment 0
CSC148, Fall 2024

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.
"""
from datetime import date, timedelta
from typing import Optional, TextIO, Union, Tuple
import os
import python_ta
from python_ta.contracts import check_contracts

# This program reads weather data from csv files. These are the column
# numbers where each kind of information appears. For example, column 9
# contains maximum temperatures.
LONG, LAT = 0, 1
STN_NAME, CL_ID = 2, 3
DATE, YEAR, MONTH, DAY = 4, 5, 6, 7
DATA_QUALITY = 8
MAX_TEMP, MAX_TEMP_FLAG = 9, 10
MIN_TEMP, MIN_TEMP_FLAG = 11, 12
MEAN_TEMP, MEAN_TEMP_FLAG = 13, 14
HEAT_DEG_DAYS, HEAT_DEG_DAYS_FLAG = 15, 16
COOL_DEG_DAYS, COOL_DEG_DAYS_FLAG = 17, 18
TOTAL_RAIN, TOTAL_RAIN_FLAG = 19, 20
TOTAL_SNOW, TOTAL_SNOW_FLAG = 21, 22
TOTAL_PRECIP, TOTAL_PRECIP_FLAG = 23, 24
SNOW_ON_GRND, SNOW_ON_GRND_FLAG = 25, 26
DIR_MAX_GUST, DIR_MAX_GUST_FLAG = 27, 28
SPD_MAX_GUST, SPD_MAX_GUST_FLAG = 29, 30


@check_contracts
class DailyWeather:
    """Weather facts for a single day.

    === Instance Attributes ===
    avg_temp: Average temperature on this day, in degrees Celsius
    low_temp: Minimum temperature on this day, in Celsius
    high_temp: Maximum temperature on this day, in Celsius
    precipitation: Total precipitation on this day in mm,
        or -1 if there were only "trace amounts" of precipitation
    rainfall: Total rainfall on this day in mm,
        or -1 for trace amounts
    snowfall: Total snowfall on this day in cm,
        or -1 for trace amounts

    === Representation Invariants ===
    - self.precipitation >= 0 or self.precipitation == -1
    - self.rainfall >= 0 or self.rainfall == -1
    - self.snowfall >= 0 or self.snowfall == -1
    - self.low_temp <= self.avg_temp <= self.high_temp

    === Sample Usage ===
    >>> weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
    >>> print(weather.avg_temp)
    13.1
    >>> print(weather.low_temp)
    9.2
    >>> print(weather.high_temp)
    20.3
    >>> print(weather.precipitation)
    5
    """
    avg_temp: float
    low_temp: float
    high_temp: float
    precipitation: float
    snowfall: float
    rainfall: float

    def __init__(self, temperature_statistics: tuple[float, float, float],
                 precipitation_statistics: tuple[float, float, float]) -> None:
        """Initialize this day's weather.

        temperature_statistics[0] is the average temperature in Celsius
        temperature_statistics[1] is the minimum temperature in Celsius
        temperature_statistics[2] is the maximum temperature in Celsius

        precipitation_statistics[0] is the total precipitation in mm
        precipitation_statistics[1] is the total rainfall in mm
        precipitation_statistics[2] is the total snowfall in cm

        For all values in precipitation_statistics, -1 indicates trace amounts.

        Preconditions:
        - all(elem >= 0 or elem == -1 for elem in precipitation_statistics)
        - minimum temperature <= average temperature <= high temperature

        >>> weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
        >>> print(weather.avg_temp)
        13.1
        """
        self.avg_temp = temperature_statistics[0]
        self.low_temp = temperature_statistics[1]
        self.high_temp = temperature_statistics[2]
        self.precipitation = precipitation_statistics[0]
        self.rainfall = precipitation_statistics[1]
        self.snowfall = precipitation_statistics[2]

    def __str__(self) -> str:
        """Return a str representing this DailyWeather.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> print(weather)
        Average: 13.00 Low: 9.00 High: 20.00 Precipitation: 5.00 Snow: 0.00 \
Rain: 0.00
        """
        return f'Average: {self.avg_temp:.2f} Low: {self.low_temp:.2f} ' \
               f'High: {self.high_temp:.2f} ' \
               f'Precipitation: {self.precipitation:.2f} ' \
               f'Snow: {self.snowfall:.2f} Rain: {self.rainfall:.2f}'


@check_contracts
class HistoricalWeather:
    """A record of historical weather information for a fixed place on Earth.

    === Instance Attributes ===
    name: The name of the place for which the weather is being recorded.
    coordinates: The latitude and longitude of this place.

    === Private Attributes ===
    _records: The daily weather records for this place. Each key is a
        date and its value is the location's weather on that day. There may
        be gaps in the data. For example, there could be data for Jan 1, 2024
        and Jan 5, 2024, but not for the days in between.

    === Representation Invariants ===
    - -90 <= self.coordinates[0] <= 90
    - -180 <= self.coordinates[1] <= 180

    === Sample Usage ===
    >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
    >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    >>> toronto_weather.add_weather(date.today(), weather)
    >>> print(toronto_weather.name)
    Toronto
    >>> print(toronto_weather.coordinates)
    (43.6529, -79.3849)
    >>> print(toronto_weather.retrieve_weather(date.today()).avg_temp)
    13
    """
    name: str
    coordinates: tuple[float, float]
    _records: dict[date, DailyWeather]

    def __init__(self, name: str, coordinates: tuple[float, float]) -> None:
        """Initialize this historical weather record with the coordinates
        <coordinates>, place name <name>, and no recorded weather so far.

        Preconditions:
        - -90 <= coordinates[0] <= 90
        - -180 <= coordinates[1] <= 180

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> print(toronto_weather.name)
        Toronto
        """
        self.name = name
        self.coordinates = coordinates
        self._records = {}

    def __str__(self) -> str:
        """Return a str representing this HistoricalWeather.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> loc = HistoricalWeather('Toronto', (43.6, -79.63))
        >>> loc.add_weather(date(2024,7,13), weather)
        >>> print(loc)
        Toronto (43.60, -79.63):
        2024-07-13: Average: 13.00 Low: 9.00 High: 20.00 Precipitation: 5.00 \
Snow: 0.00 Rain: 0.00
        """
        lat, long = self.coordinates
        res = f"{self.name} ({lat:.2f}, {long:.2f}):\n"
        res += "\n".join([f"{k}: {str(v)}" for k, v in self._records.items()])
        return res

    def get_record(self) -> dict[date, DailyWeather]:
        """returns self._records"""
        return self._records

    def add_weather(self, d: date, w: DailyWeather) -> None:
        """Record that <w> was the weather on the date <d>.

        If a record for date <d> already exists, then do nothing (i.e. do not
        change the information that is already recorded).

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> print(toronto_weather.retrieve_weather(date.today()).avg_temp)
        13
        """
        if d not in self._records:
            self._records[d] = w

    def retrieve_weather(self, d: date) -> Optional[DailyWeather]:
        """Return the weather on day <d> if available, otherwise return None.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> toronto_weather.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if d in self._records:
            return self._records[d]
        return None

    def record_high(self, m: int, d: int) -> float:
        """Return the highest temperature recorded at this location on month <m>
        and day <d> in any year.
        Note that months are represented by numbers 1-12.

        Preconditions:
        - 1 <= m <= 12
        - 1 <= d <= 31 and d is possible day for the month m. For example,
          if m is 9 (for September), m will not be 31, since September has
          30 days.
        - The weather on month m and day d has been recorded for this
          location in at least one year.

        >>> weather1 = DailyWeather((13.0, 10.0, 40.0), (0.0, 0.0, 0.0))
        >>> weather2 = DailyWeather((13.0, 10.0, 30.0), (0.0, 0.0, 0.0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> day1 = date(2024, 6, 8)
        >>> day2 = date(2023, 6, 8)
        >>> toronto_weather.add_weather(day1, weather1)
        >>> toronto_weather.add_weather(day2, weather2)
        >>> toronto_weather.record_high(6, 8)
        40.0
        """
        highest_temp = float('-inf')

        for record_date, weather in self._records.items():
            if record_date.month == m and record_date.day == d:
                if weather.high_temp > highest_temp:
                    highest_temp = weather.high_temp

        return highest_temp

    def monthly_average(self) -> dict[str, Optional[float]]:
        """For each of the 12 months, return the average of the minimum
        temperatures for all dates in that month (in any year) that have
        weather recorded.

        Return the result in a dictionary mapping month name to average,
        and using these three-character names for the months:
            Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec.
        If a month has no weather recorded in any year, map that month name
        to the value None.

        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> jan1_weather = DailyWeather((13, 11, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2023, 1, 1), jan1_weather)
        >>> jan2_weather = DailyWeather((13, 10, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2023, 1, 2), jan2_weather)
        >>> jan2024_weather = DailyWeather((13, 0, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2024, 1, 18), jan2024_weather)
        >>> feb_weather = DailyWeather((13, 11, 30), (0, 0, 0))
        >>> toronto_weather.add_weather(date(2023, 2, 1), feb_weather)
        >>> d = toronto_weather.monthly_average()
        >>> len(d)
        12
        >>> d['Jan'] == 7.0
        True
        >>> d['Feb'] == 11.0
        True
        >>> d['Mar'] is None
        True
        """
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_avg = {month_: [] for month_ in months}

        for record_date, weather in self._records.items():
            month_name = months[record_date.month - 1]
            monthly_avg[month_name].append(weather.low_temp)

        for month in monthly_avg:
            temps = monthly_avg[month]
            if temps:
                monthly_avg[month] = sum(temps) / len(temps)
            else:
                monthly_avg[month] = None

        return monthly_avg

    @staticmethod
    def _check_precipitation(weather: DailyWeather) -> bool:
        """Check if the weather record
        indicates precipitation."""
        return weather.precipitation > 0 or weather.precipitation == -1

    @staticmethod
    def _contiguous(dates: list[date], i: int) -> bool:
        """Check if the index in list of dates
          is the next day after last index .
          Precondition:
        - 1 < i < len(dates)
        so both i and i-1 are valid elements of dates
        """
        delta = timedelta(days=1)
        return dates[i - 1] + delta == dates[i]

    @staticmethod
    def _update(curr_start: Optional[date],
                curr_len: int,
                longest: int,
                longest_start: date) -> Tuple[int, date]:
        """returns the new longest len and respective start date"""
        if curr_start and curr_len > longest:
            return curr_len, curr_start
        return longest, longest_start

    def contiguous_precipitation(self) -> tuple[date, int]:
        """Return the start date and length of the longest sequence of
        consecutive days that had precipitation.

        A day is considered to have had precipitation if its precipitation
        value is either above 0 or is -1 (indicating that there were trace
        amounts of precipitation). The days in a sequence must have been
        consecutive, that is, there can be no day between them. For example.
        if we have recorded weather for July 3rd, 5th, and 6th, that is not
        a sequence of consecutive days.

        In the case of a tie for the longest sequence, any one of the tied
        start dates can be returned.

        In the case when there are no contigious days with percipitation
        (there were no days with percipitation at all),
        return a tuple with any date in self._records and 1.

        NOTE: You may not assume the addition order of data into this
            HistoricalWeather object.

        Preconditions:
        - At least one day's weather has been recorded.

        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> weather2 = DailyWeather((0, 0, 0), (2, 0, 0))
        >>> weather3 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> weather4 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> delta = timedelta(days=1)
        >>> toronto_weather.add_weather(date.today(), weather1)
        >>> toronto_weather.add_weather(date.today() + delta, weather2)
        >>> toronto_weather.add_weather(date.today() + 2 * delta, weather3)
        >>> toronto_weather.add_weather(date.today() + 3 * delta, weather4)
        >>> result = toronto_weather.contiguous_precipitation()
        >>> result[0] == date.today()
        True
        >>> result[1]
        4
        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> weather2 = DailyWeather((0, 0, 0), (2, 0, 0))
        >>> weather3 = DailyWeather((0, 0, 0), (1, 0, 0))
        >>> montreal_weather = HistoricalWeather('Montreal', (45.47, -73.74))
        >>> montreal_weather.add_weather(date(2024, 4, 3), weather1)
        >>> montreal_weather.add_weather(date(2024, 4, 5), weather2)
        >>> montreal_weather.add_weather(date(2024, 4, 7), weather3)
        >>> # No consecutive days
        >>> result = montreal_weather.contiguous_precipitation()
        >>> result[1]
        1
        """
        sorted_dates = sorted(self._records.keys())

        longest_start = sorted_dates[0]
        longest = 1

        curr_len = 0
        curr_start = None

        for i in range(len(sorted_dates)):
            weather = self._records[sorted_dates[i]]

            if self._check_precipitation(weather):
                if curr_len == 0:
                    curr_start = sorted_dates[i]
                    curr_len = 1
                elif self._contiguous(sorted_dates, i):
                    curr_len += 1
                else:
                    longest, longest_start = self._update(curr_start,
                                                          curr_len,
                                                          longest,
                                                          longest_start)
                    curr_start = sorted_dates[i]
                    curr_len = 1
            else:
                longest, longest_start = self._update(curr_start, curr_len,
                                                      longest, longest_start)
                curr_len = 0

        longest, longest_start = self._update(curr_start, curr_len,
                                              longest, longest_start)

        return longest_start, longest

    def percentage_snowfall(self) -> float:
        """Return the fraction of the snowfall and rainfall at this location
        that was snowfall, across all dates when weather was recorded there.

        The answer returned should be calculated as:
            total snowfall / (total snowfall + total rainfall)

        Do not count trace amounts in this calculation. Ignore the units in
        the calculation.  (This is equivalent to assuming that 1 mm of
        rain is equivalent to 1 cm of snow.)

        Precondition:
        - At least one day's weather has been recorded where
          snowfall > 0 or rainfall > 0 or both.

        >>> weather1 = DailyWeather((0, 0, 0), (1, 0, 1))
        >>> weather2 = DailyWeather((0, 0, 0), (3, 3, 0))
        >>> today = date(2024, 5, 1)
        >>> delta = timedelta(days=1)
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(today, weather1)
        >>> toronto_weather.add_weather(today + delta, weather2)
        >>> toronto_weather.percentage_snowfall()
        0.25
        """
        total_snowfall = 0.0
        total_rainfall = 0.0

        for weather in self._records.values():
            if weather.snowfall > 0:
                total_snowfall += weather.snowfall
            if weather.rainfall > 0:
                total_rainfall += weather.rainfall

        if total_snowfall + total_rainfall == 0:
            return 0.0
        return total_snowfall / (total_snowfall + total_rainfall)


@check_contracts
class Country:
    """ The weather records for various locations in a country.

    === Instance Attributes ===
    name: Name of the country.

    === Private Attributes ===
    _histories:
        The weather records for this country. Each key is a location's name,
        and its value is that location's weather history

    === Representation Invariants ===
    - For each key, k, of _histories, k == _histories[k].name

    === Sample Usage ===
    >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
    >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
    >>> toronto_weather.add_weather(date.today(), weather)
    >>> canada = Country('Canada')
    >>> canada.add_history(toronto_weather)
    >>> yyz = canada.retrieve_history('YYZ')
    >>> yyz.retrieve_weather(date.today()).avg_temp == 13
    True
    """
    name: str
    _histories: dict[str, HistoricalWeather]

    def __init__(self, n: str) -> None:
        """ Initialize this Country with name <n> and no weather history so far.

        >>> canada = Country('Canada')
        >>> print(canada.name)
        Canada
        """
        self.name = n
        self._histories = {}

    def __str__(self) -> str:
        """Return a str representing this Country.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> weather_2 = DailyWeather((14, 10, 21), (5, 0, 2.0))
        >>> canada = Country('Canada')
        >>> the_date = date(2024,7,13)
        >>> loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
        >>> loc1_data.add_weather(the_date, weather)
        >>> loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> loc2_data.add_weather(the_date - timedelta(1), weather)
        >>> loc2_data.add_weather(the_date + timedelta(1), weather_2)
        >>> canada.add_history(loc1_data)
        >>> canada.add_history(loc2_data)
        >>> print(canada)
        Canada:
        Toronto (43.60, -79.63):
        2024-07-13: Average: 13.00 Low: 9.00 High: 20.00 Precipitation: 5.00 \
Snow: 0.00 Rain: 0.00
        YYZ (43.65, -79.38):
        2024-07-12: Average: 13.00 Low: 9.00 High: 20.00 Precipitation: 5.00 \
Snow: 0.00 Rain: 0.00
        2024-07-14: Average: 14.00 Low: 10.00 High: 21.00 Precipitation: 5.00 \
Snow: 2.00 Rain: 0.00
        """
        result = f"{self.name}:\n"

        for history in self._histories.values():
            result += str(history) + "\n"

        return result.strip()

    def add_history(self, hw: HistoricalWeather) -> None:
        """Add a location to this Country. <hw> is the location's weather
        history, and hw.name is the location's name.

        If a location with the name hw.name is already recorded in this Country,
        then do nothing (i.e. do not change the data that is already present
        for that location).

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> yyz = canada.retrieve_history('YYZ')
        >>> yyz.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        if hw.name not in self._histories:
            self._histories[hw.name] = hw

    def retrieve_history(self, name: str) -> Optional[HistoricalWeather]:
        """Return the weather history for the location called <name>, or
        None if no such location has been recorded in this Country.

        >>> weather = DailyWeather((13, 9, 20), (5, 0, 0))
        >>> toronto_weather = HistoricalWeather('YYZ', (43.6529, -79.3849))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> yyz = canada.retrieve_history('YYZ')
        >>> yyz.retrieve_weather(date.today()).avg_temp == 13
        True
        """
        return self._histories.get(name)

    def snowiest_location(self) -> Union[tuple[str, float], tuple[None, None]]:
        """Return the name of location with the highest percentage snowfall in
        this Country, and its percentage snowfall.

        In the case of a tie, any one of the tied locations can be returned.

        If there are no locations in this Country, return (None, None).

        Preconditions:
        - For all locations in this Country, at least one day's
          weather has been recorded where snowfall > 0 or rainfall > 0
          or both.

        >>> weather = DailyWeather((13, 9, 20), (5, 2, 3))
        >>> other_weather = DailyWeather((13, 4, 20), (5, 2, 2))
        >>> toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
        >>> mtl_weather = HistoricalWeather('Montreal', (45.47, -73.74))
        >>> toronto_weather.add_weather(date.today(), weather)
        >>> mtl_weather.add_weather(date.today(), other_weather)
        >>> canada = Country('Canada')
        >>> canada.add_history(toronto_weather)
        >>> canada.add_history(mtl_weather)
        >>> result = canada.snowiest_location()
        >>> result[0]
        'Toronto'
        >>> result[1]
        0.6
        """
        res = (None, None)

        if not self._histories:
            return res

        max_ = float('-inf')
        for location, w in self._histories.items():
            percentage = w.percentage_snowfall()
            if percentage > max_:
                max_ = percentage
                res = (location, max_)
        return res

    def generate_summary(self) -> None:
        """Write a summary of interesting statistics for the locations
        in this Country to a markdown file called report.md

        Precondition:
        - All locations in this Country have at least one row of data
          recorded in December of any year
        - Data has been recorded for Dec 25 in at least one year
        """
        headers = ["Location", "record high <br/> for Dec 25",
                   "december <br/> average",
                   "contiguous <br/> precipitation",
                   "percentage <br/> snowfall"]

        with open("report.md", 'w') as f:
            f.write(" | ".join(headers) + "\n")
            f.write(":|-".join(["-" * len(col) for col in headers]) + ":\n")
            for key in self._histories:
                loc = self._histories[key]
                (rec_high, mon_avg,
                 ctgs_prec, perc_snow) = (loc.record_high(12, 25),
                                          loc.monthly_average(),
                                          loc.contiguous_precipitation(),
                                          loc.percentage_snowfall())
                f.write(f"{key: <20} | {rec_high: <10.4} | "
                        f"{mon_avg['Dec']} | "
                        f"{ctgs_prec[1]: <24} | {perc_snow: <18.2}\n")


def parse_date(parts: list[str]) -> Optional[date]:
    """Parse the date from the CSV parts list.

    Return the date if valid, otherwise return None.
    """
    try:
        year = int(parts[YEAR])
        month = int(parts[MONTH])
        day = int(parts[DAY])
        return date(year, month, day)
    except (ValueError, IndexError):
        return None


def parse_temperatures(parts: list[str]) \
        -> Optional[tuple[float, float, float]]:
    """Parse and validate temperatures from the CSV parts list.

    Return a tuple of (mean_temp, min_temp, max_temp)
    if valid, otherwise return None.
    """
    try:
        max_temp = float(parts[MAX_TEMP])
        min_temp = float(parts[MIN_TEMP])
        mean_temp = float(parts[MEAN_TEMP])
        if min_temp <= mean_temp <= max_temp:
            return mean_temp, min_temp, max_temp
        return None
    except (ValueError, IndexError):
        return None


def parse_precipitation(parts: list[str]) -> tuple[float, float, float]:
    """Parse precipitation, rainfall, and snowfall
    values from the CSV parts list.

    Return a tuple of (precipitation, rainfall, snowfall),
    converting trace values to -1.
    """
    def get_precip_value(precip: str, flag: str) -> float:
        """helper"""
        if flag == "T":
            return -1
        try:
            value = float(precip)
            return value if value >= 0 else 0.0
        except ValueError:
            return 0.0

    precip_flag = parts[TOTAL_PRECIP_FLAG]
    rain_flag = parts[TOTAL_RAIN_FLAG]
    snow_flag = parts[TOTAL_SNOW_FLAG]

    precipitation = get_precip_value(parts[TOTAL_PRECIP], precip_flag)
    rainfall = get_precip_value(parts[TOTAL_RAIN], rain_flag)
    snowfall = get_precip_value(parts[TOTAL_SNOW], snow_flag)

    return precipitation, rainfall, snowfall


def load_data(f: TextIO) -> Optional[HistoricalWeather]:
    """Return a HistoricalWeather record representing the weather data in the
    already open csv file <f>.

    If <f> contains no lines of data aside from its header, return None.

    The data might not consistently cover consecutive days, but will be
    in order from the oldest dates to most recent dates.
    Do not add daily weather for days where there is missing data
    (as defined in the handout).
    A "T" in the file indicates that there were trace values.
    Record trace values as -1 in the corresponding attribute.

    Preconditions:
    - f is open and is set to the beginning of the file.
    - The first line of f is a header, and the remaining lines
      follow the format specified in the handout.
    - There may be no lines of data, but there is at least a header.
    """
    lines = f.readlines()
    if len(lines) <= 1:
        return None

    first_row = lines[1].strip().split(',')
    station_name = first_row[STN_NAME]
    longitude = float(first_row[LONG])
    latitude = float(first_row[LAT])
    historical_weather = HistoricalWeather(station_name,
                                           (latitude, longitude))

    for line in lines[1:]:
        parts = line.strip().split(',')

        record_date = parse_date(parts)
        if not record_date:
            continue

        temperatures = parse_temperatures(parts)
        if not temperatures:
            continue

        precipitation, rainfall, snowfall = parse_precipitation(parts)

        weather = DailyWeather(temperatures,
                               (precipitation,
                                rainfall,
                                snowfall))
        historical_weather.add_weather(record_date, weather)

    return historical_weather if historical_weather.get_record() else None


def load_country(folder_name: str, name: str) -> Country:
    """Return a Country called <name> that contains all the historical weather
     data stored in the files that are in the folder called <folder_name>.

    Precondition:
    - Each file in the folder called folder_name:
        - is a .csv files that obeys the format specified in the handout
        - contains data for one location within this Country
    """
    country = Country(name)
    for filename in os.listdir(folder_name):
        # If there are any "dot files", ignore them.
        if not filename.startswith('.'):
            with open(os.path.join(folder_name, filename), 'r') as loc_file:
                history = load_data(loc_file)
                if history is not None:
                    country.add_history(history)

    return country


def generate_usage_example() -> Country:
    """Generate a toy example.
    """
    weather_1 = DailyWeather((13, 9, 20), (5, 0, 0))
    weather_2 = DailyWeather((14, 10, 21), (5, 0, 2.0))
    country = Country('Canada')
    the_date = date(2024, 7, 13)
    loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
    loc1_data.add_weather(the_date, weather_1)
    loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
    loc2_data.add_weather(the_date - timedelta(1), weather_1)
    loc2_data.add_weather(the_date + timedelta(1), weather_2)
    country.add_history(loc1_data)
    country.add_history(loc2_data)
    return country


if __name__ == '__main__':
    CHECK_PYTA = True  # Set to False to disable pyta checking
    if CHECK_PYTA:
        python_ta.check_all(config={
            'allowed-io': ['load_country', 'Country.generate_summary'],
            'allowed-import-modules': [
                'doctest', 'python_ta', 'python_ta.contracts', 'typing',
                'datetime', 'os'],
            'disable': ['E1136'],
            'max-attributes': 15,
        })

    import doctest
    doctest.testmod()

    # Example use (1):
    # Create weather day "by hand" and examine it using __str__ methods
    # defined in the various classes.
    canada = generate_usage_example()
    toronto = canada.retrieve_history('Toronto')
    toronto_day = toronto.retrieve_weather(date(2024, 7, 13))
    # Try printing instances of each of the 3 classes.
    print(f'----- a DailyWeather object:\n{canada}')
    print(f'----- a HistoricalWeather object:\n{toronto}')
    print(f'----- a Country object:\n{canada}')

    # Example use (2):
    # Load all the data in a folder, and generate a file "report.md"
    # containing a simple summary of that data.
    # Note: The file uses a format called "markdown", which includes
    # special symbols describing desired formatting.  Open report.md in
    # Pycharm, and it will show you a formatted version.
    canada = load_country('./student_data/', 'Canada')
    canada.generate_summary()
    print('bye')
