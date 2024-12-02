"""
Assignment 0 - Sample tests

CSC148, Fall 2024

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.
"""
import pytest
from datetime import date
from datetime import timedelta
from weather import DailyWeather, HistoricalWeather, Country, load_data, \
    load_country
import python_ta.contracts
python_ta.contracts.ENABLE_CONTRACT_CHECKING = False


def test_add_and_retrieve_weather():
    """Test that we can add and retrieve a single weather record from
    HistoricalWeather."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    daily = DailyWeather((1.0, 2.0, 3.0), (4.0, 2.0, 2.0))
    record_date = date(2020, 1, 12)
    historical.add_weather(record_date, daily)

    assert historical.retrieve_weather(record_date) is daily, \
        "Calling retrieve_weather() on a date should return the " + \
        "DailyWeather object that was added to that date."


def test_valid_weather_initialization():
    # Normal case with no trace precipitation
    weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
    assert weather.avg_temp == 13.1
    assert weather.low_temp == 9.2
    assert weather.high_temp == 20.3
    assert weather.precipitation == 5
    assert weather.rainfall == 0
    assert weather.snowfall == 0

    # Case with trace precipitation
    weather_trace = DailyWeather((10.0, 5.0, 15.0), (-1, -1, -1))
    assert weather_trace.precipitation == -1
    assert weather_trace.rainfall == -1
    assert weather_trace.snowfall == -1


def test_temperature_edge_cases():
    # Minimum and maximum temperatures are equal
    weather_equal_temps = DailyWeather((10.0, 10.0, 10.0), (0, 0, 0))
    assert weather_equal_temps.low_temp == 10.0
    assert weather_equal_temps.avg_temp == 10.0
    assert weather_equal_temps.high_temp == 10.0

    # Minimum temperature equal to average temperature, high temperature slightly higher
    weather_min_avg_equal = DailyWeather((10.0, 10.0, 10.1), (0, 0, 0))
    assert weather_min_avg_equal.low_temp == 10.0
    assert weather_min_avg_equal.avg_temp == 10.0
    assert weather_min_avg_equal.high_temp == 10.1

    # Average temperature equal to high temperature, low temperature slightly lower
    weather_avg_max_equal = DailyWeather((10.0, 9.9, 10.0), (0, 0, 0))
    assert weather_avg_max_equal.low_temp == 9.9
    assert weather_avg_max_equal.avg_temp == 10.0
    assert weather_avg_max_equal.high_temp == 10.0


def test_invalid_temperature_ranges():
    try:
        # Avg temp less than low temp
        DailyWeather((5.0, 10.0, 15.0), (0, 0, 0))
        assert False, "Initialization should fail with avg < low"
    except AssertionError:
        pass

    try:
        # Avg temp greater than high temp
        DailyWeather((20.0, 15.0, 10.0), (0, 0, 0))
        assert False, "Initialization should fail with avg > high"
    except AssertionError:
        pass


def test_precipitation_edge_cases():
    # Precipitation exactly zero
    weather_zero_precip = DailyWeather((10.0, 5.0, 15.0), (0, 0, 0))
    assert weather_zero_precip.precipitation == 0
    assert weather_zero_precip.rainfall == 0
    assert weather_zero_precip.snowfall == 0

    # Trace precipitation
    weather_trace_precip = DailyWeather((10.0, 5.0, 15.0), (-1, -1, -1))
    assert weather_trace_precip.precipitation == -1
    assert weather_trace_precip.rainfall == -1
    assert weather_trace_precip.snowfall == -1

    try:
        # Negative values for precipitation not allowed except for trace amounts
        DailyWeather((10.0, 5.0, 15.0), (-2, 0, 0))
        assert False, "Initialization should fail with negative precipitation"
    except AssertionError:
        pass

    try:
        DailyWeather((10.0, 5.0, 15.0), (0, -2, 0))
        assert False, "Initialization should fail with negative rainfall"
    except AssertionError:
        pass

    try:
        DailyWeather((10.0, 5.0, 15.0), (0, 0, -2))
        assert False, "Initialization should fail with negative snowfall"
    except AssertionError:
        pass


def test_string_representation():
    weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 0))
    expected_output = "Average: 13.10 Low: 9.20 High: 20.30 Precipitation: 5.00 Snow: 0.00 Rain: 0.00"
    assert str(weather) == expected_output

    weather_trace = DailyWeather((13, 9, 20), (-1, -1, -1))
    expected_output = "Average: 13.00 Low: 9.00 High: 20.00 Precipitation: -1.00 Snow: -1.00 Rain: -1.00"
    assert str(weather_trace) == expected_output


def test_record_high1():
    """Test record_high on a HistoricalWeather with two points of data,
    where the record high is at the earlier year."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(
        date(2012, 6, 4), DailyWeather((0.0, 0.0, 20.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2010, 6, 4), DailyWeather((0.0, 0.0, 30.0), (0.0, 0.0, 0.0)))

    assert historical.record_high(6, 4) == 30.0


def test_monthly_average1():
    """Test monthly_average on a HistoricalWeather that has one point of data
    per month, all within a single year."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(
        date(2012, 1, 8), DailyWeather((-0.25, -1.75, 0.25), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 2, 9), DailyWeather((0.0, -3.0, 1.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 3, 10), DailyWeather((0.75, -3.75, 2.25), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 4, 11), DailyWeather((2.0, -4.0, 4.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 5, 12), DailyWeather((3.75, -3.75, 6.25), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 6, 13), DailyWeather((6.0, -3.0, 9.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 7, 14), DailyWeather((8.75, -1.75, 12.25), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 8, 15), DailyWeather((12.0, 0.0, 16.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 9, 16), DailyWeather((15.75, 2.25, 20.25), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 10, 17), DailyWeather((20.0, 5.0, 25.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 11, 18), DailyWeather((24.75, 8.25, 30.25), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2012, 12, 19), DailyWeather((30.0, 12.0, 36.0), (0.0, 0.0, 0.0)))

    assert historical.monthly_average() == {
        'Jan': -1.75, 'Feb': -3.0, 'Mar': -3.75, 'Apr': -4.0,
        'May': -3.75, 'Jun': -3.0, 'Jul': -1.75, 'Aug': 0.0,
        'Sep': 2.25, 'Oct': 5.0, 'Nov': 8.25, 'Dec': 12.0
    }


def test_contiguous_precipitation():
    """Test contiguous_precipitation on a HistoricalWeather that has alternating
    snow and rain."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(
        date(2012, 6, 4), DailyWeather((0.0, 0.0, 0.0), (3.0, 3.0, 0.0)))

    historical.add_weather(
        date(2012, 6, 5), DailyWeather((0.0, 0.0, 0.0), (2.0, 0.0, 2.0)))

    historical.add_weather(
        date(2012, 6, 6), DailyWeather((0.0, 0.0, 0.0), (4.0, 4.0, 0.0)))

    historical.add_weather(
        date(2012, 6, 7), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 1.0)))

    historical.add_weather(
        date(2012, 6, 8), DailyWeather((0.0, 0.0, 0.0), (5.0, 5.0, 0.0)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 4), 5)


def test_single_day_with_precipitation():
    """Test contiguous_precipitation with only one day recorded with precipitation."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 1)


def test_all_continuous_days_with_precipitation():
    """Test contiguous_precipitation with all days being consecutive with precipitation."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 2), DailyWeather((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 3), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 3)


def test_no_continuous_days_with_precipitation():
    """Test contiguous_precipitation with no consecutive sequence of precipitation days."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 3), DailyWeather((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 5), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 1)


def test_continuous_sequence_at_end_of_month():
    """Test contiguous_precipitation with a sequence that spans the end of a month."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 29), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 30), DailyWeather((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 31), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 2, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 29), 4)


def test_continuous_sequence_with_trace_precipitation():
    """Test contiguous_precipitation with a sequence that includes trace amounts of precipitation."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 2), DailyWeather((0.0, 0.0, 0.0), (-1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 3), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 3)


def test_intermittent_precipitation_with_large_gaps():
    """Test contiguous_precipitation with intermittent precipitation and large gaps."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 10), DailyWeather((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 20), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 1)


def test_longest_sequence_not_at_beginning():
    """Test contiguous_precipitation where the longest sequence starts later in the list."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 3), DailyWeather((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 4), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 5), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 4), 2)


def test_non_continuous_sequence_due_to_missing_days():
    """Test contiguous_precipitation with missing days preventing continuous sequence."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 2, 27), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 2, 28), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 3, 2), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 2, 27), 2)


def test_all_non_precipitating_days():
    """Test contiguous_precipitation with all days having no precipitation."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 2), DailyWeather((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 1)


def test_alternating_precipitation_and_non_precipitation():
    """Test contiguous_precipitation with alternating days of precipitation and no precipitation."""
    historical = HistoricalWeather("Test City", (0, 0))
    historical.add_weather(date(2024, 1, 1), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 2), DailyWeather((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 3), DailyWeather((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)))
    historical.add_weather(date(2024, 1, 4), DailyWeather((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    assert historical.contiguous_precipitation() == (date(2024, 1, 1), 1)


def test_percentage_snowfall1():
    """Test percentage_snowfall on a HistoricalWeather that has a single day
    with both snow and rain"""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(
        date(2012, 11, 21), DailyWeather((0.0, 0.0, 0.0), (7.0, 3.0, 2.0)))

    assert historical.percentage_snowfall() == 0.4


def test_add_and_retrieve_history():
    """Test that we can add and retrieve a single weather record from
    a Country."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    country = Country("Country Name")
    country.add_history(historical)

    assert country.retrieve_history("City Name") is historical, \
        "Calling retrieve_history() on a location should return the " + \
        "HistoricalWeather object that was added to that location."


def test_snowiest_location():
    """Test that snowiest_location with two locations returns the one with a
    higher percentage snowfall."""
    country = Country('Country Name')

    # Create one HistoricalWeather record
    historical = HistoricalWeather('City Name', (-1.234, 4.567))

    historical.add_weather(
        date(2012, 11, 21), DailyWeather((-5.0, -10.0, 15.0), (7.0, 3.0, 2.0)))

    historical.add_weather(
        date(2012, 10, 21), DailyWeather((-7.0, -20.0, 15.0), (0.0, 0.0, 0.0)))

    historical.add_weather(
        date(2011, 11, 21), DailyWeather((-8, -15, 15), (0.0, 0.0, 0.0)))

    country.add_history(historical)

    # Create another HistoricalWeather record
    historical2 = HistoricalWeather("Another City", (0.123, -3.4567))

    historical2.add_weather(
        date(2012, 11, 21), DailyWeather((-5.0, -10.0, 15.0), (9.0, 5.0, 4.0)))

    historical2.add_weather(
        date(2012, 10, 21), DailyWeather((-7.0, -20.0, 15.0), (20.0, 15.0, 5.0)))

    country.add_history(historical2)

    assert country.snowiest_location() == ('City Name', 0.4)


def test_load_data():
    """Test load_data on small_sample_data.csv"""
    with open('student_data/small_sample_data.csv') as source:
        historical_weather = load_data(source)

    assert historical_weather is not None, \
        "HistoricalWeather should have been returned when calling load_data " \
        "on small_sample_data.csv but got None."

    assert historical_weather.name == 'THUNDER BAY'

    # Note: You may want to check more properties below!
    #       The current test just reads the HistoricalWeather object from
    #       student_data/small_sample_data.csv
    #       and checks that the name attribute is properly set.


def test_add_weather():
    weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    today = date.today()
    daily_weather = DailyWeather((13, 9, 20), (5, 0, 0))

    # Adding weather to a new date
    weather.add_weather(today, daily_weather)
    assert today in weather.get_record()
    assert weather.retrieve_weather(today).avg_temp == 13

    # Attempting to add weather to the same date should not override
    updated_weather = DailyWeather((20, 15, 25), (10, 5, 0))
    weather.add_weather(today, updated_weather)
    assert weather.retrieve_weather(today).avg_temp == 13  # Should still be 13, not 20


def test_retrieve_weather():
    weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    today = date.today()
    daily_weather = DailyWeather((13, 9, 20), (5, 0, 0))

    # Retrieving weather when no weather has been recorded
    assert weather.retrieve_weather(today) is None

    # Retrieving weather after adding it
    weather.add_weather(today, daily_weather)
    retrieved_weather = weather.retrieve_weather(today)
    assert retrieved_weather is not None
    assert retrieved_weather.avg_temp == 13
    assert retrieved_weather.low_temp == 9
    assert retrieved_weather.high_temp == 20


def test_record_high2():
    weather1 = DailyWeather((13.0, 10.0, 40.0), (0.0, 0.0, 0.0))
    weather2 = DailyWeather((13.0, 10.0, 30.0), (0.0, 0.0, 0.0))
    toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    day1 = date(2024, 6, 8)
    day2 = date(2023, 6, 8)
    toronto_weather.add_weather(day1, weather1)
    toronto_weather.add_weather(day2, weather2)

    assert toronto_weather.record_high(6, 8) == 40.0

    day3 = date(2022, 6, 8)
    weather3 = DailyWeather((13.0, 10.0, 50.0), (0.0, 0.0, 0.0))
    toronto_weather.add_weather(day3, weather3)
    assert toronto_weather.record_high(6, 8) == 50.0


def test_monthly_average2():
    toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    jan1_weather = DailyWeather((13, 11, 30), (0, 0, 0))
    toronto_weather.add_weather(date(2023, 1, 1), jan1_weather)
    jan2_weather = DailyWeather((13, 10, 30), (0, 0, 0))
    toronto_weather.add_weather(date(2023, 1, 2), jan2_weather)
    jan2024_weather = DailyWeather((13, 0, 30), (0, 0, 0))
    toronto_weather.add_weather(date(2024, 1, 18), jan2024_weather)
    feb_weather = DailyWeather((13, 11, 30), (0, 0, 0))
    toronto_weather.add_weather(date(2023, 2, 1), feb_weather)

    # Test average minimum temperatures
    d = toronto_weather.monthly_average()
    assert len(d) == 12
    assert d['Jan'] == 7.0
    assert d['Feb'] == 11.0
    assert d['Mar'] is None


def test_percentage_snowfall():
    # Scenario 1: Mix of snowfall and rainfall
    weather1 = DailyWeather((0, 0, 0), (1, 0, 1))  # 1 cm snow, no rain
    weather2 = DailyWeather((0, 0, 0), (3, 3, 0))  # 3 mm rain, no snow
    today = date(2024, 5, 1)
    delta = timedelta(days=1)
    toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    toronto_weather.add_weather(today, weather1)
    toronto_weather.add_weather(today + delta, weather2)

    # Expected Calculation:
    # Total snowfall = 1 cm
    # Total rainfall = 3 mm
    # Percentage of snowfall: 1 / (1 + 3) = 0.25
    assert abs(toronto_weather.percentage_snowfall() - 0.25) < 1e-9

    # Scenario 2: Adding only snow and only rain to the mix
    snow_only = DailyWeather((0, 0, 0), (0, 0, 10))  # 10 cm snow, no rain
    rain_only = DailyWeather((0, 0, 0), (10, 10, 0))  # 10 mm rain, no snow
    toronto_weather.add_weather(today + 2 * delta, snow_only)
    toronto_weather.add_weather(today + 3 * delta, rain_only)

    # Expected Calculation:
    # Total snowfall = 1 (from weather1) + 10 (from snow_only) = 11 cm
    # Total rainfall = 3 (from weather2) + 10 (from rain_only) = 13 mm
    # Percentage of snowfall: 11 / (11 + 13) = 11 / 24 = 0.4583333333333333
    expected_percentage = 11 / (11 + 13)
    actual_percentage = toronto_weather.percentage_snowfall()

    print(f"Expected percentage: {expected_percentage}")
    print(f"Actual percentage: {actual_percentage}")
    assert abs(actual_percentage - expected_percentage) < 1e-9



def test_country_initialization():
    # Test basic initialization
    canada = Country('Canada')
    assert canada.name == 'Canada'
    assert canada._histories == {}

def test_add_history():
    # Setup
    weather = DailyWeather((13, 9, 20), (5, 0, 0))
    toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    toronto_weather.add_weather(date.today(), weather)
    canada = Country('Canada')

    # Test adding history
    canada.add_history(toronto_weather)
    assert 'Toronto' in canada._histories
    assert canada.retrieve_history('Toronto') == toronto_weather

    # Test adding duplicate location
    duplicate_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    canada.add_history(duplicate_weather)
    assert len(canada._histories) == 1  # Should not add duplicate

def test_retrieve_history():
    # Setup
    canada = Country('Canada')
    toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    canada.add_history(toronto_weather)

    # Test retrieving existing history
    assert canada.retrieve_history('Toronto') == toronto_weather

    # Test retrieving non-existent history
    assert canada.retrieve_history('Montreal') is None

def test_snowiest_location():
    # Setup
    weather = DailyWeather((13, 9, 20), (5, 2, 3))  # 60% snowfall
    other_weather = DailyWeather((13, 4, 20), (5, 2, 2))  # 50% snowfall
    toronto_weather = HistoricalWeather('Toronto', (43.6529, -79.3849))
    mtl_weather = HistoricalWeather('Montreal', (45.47, -73.74))
    toronto_weather.add_weather(date.today(), weather)
    mtl_weather.add_weather(date.today(), other_weather)
    canada = Country('Canada')
    canada.add_history(toronto_weather)
    canada.add_history(mtl_weather)

    # Test snowiest location
    assert canada.snowiest_location() == ('Toronto', 0.6)

    # Test tie case
    tie_weather = DailyWeather((0, 0, 0), (5, 2, 3))  # Same percentage as Toronto
    ottawa_weather = HistoricalWeather('Ottawa', (45.4215, -75.6972))
    ottawa_weather.add_weather(date.today(), tie_weather)
    canada.add_history(ottawa_weather)

    # Test snowiest location with a tie (any tied result is acceptable)
    snowiest = canada.snowiest_location()
    assert snowiest[1] == 0.6
    assert snowiest[0] in ['Toronto', 'Ottawa']

    # Test empty country case
    empty_country = Country('EmptyLand')
    assert empty_country.snowiest_location() == (None, None)


def test_str_representation():
    # Setup
    weather = DailyWeather((13, 9, 20), (5, 0, 0))
    loc1_data = HistoricalWeather('Toronto', (43.6, -79.63))
    loc1_data.add_weather(date(2024, 7, 13), weather)
    loc2_data = HistoricalWeather('YYZ', (43.6529, -79.3849))
    loc2_data.add_weather(date(2024, 7, 12), weather)
    loc2_data.add_weather(date(2024, 7, 14), DailyWeather((14, 10, 21), (5, 0, 2.0)))
    canada = Country('Canada')
    canada.add_history(loc1_data)
    canada.add_history(loc2_data)

    # Expected string format
    expected = (
        "Canada:\n"
        "Toronto (43.60, -79.63):\n"
        "2024-07-13: Average: 13.00 Low: 9.00 High: 20.00 Precipitation: 5.00 Snow: 0.00 Rain: 0.00\n"
        "YYZ (43.65, -79.38):\n"
        "2024-07-12: Average: 13.00 Low: 9.00 High: 20.00 Precipitation: 5.00 Snow: 0.00 Rain: 0.00\n"
        "2024-07-14: Average: 14.00 Low: 10.00 High: 21.00 Precipitation: 5.00 Snow: 2.00 Rain: 0.00"
    )
    assert str(canada) == expected


if __name__ == '__main__':
    pytest.main(['a0_starter_tests.py'])
