from datetime import datetime
from exceptions import CustomError
from models import Driver, DRIVERS
from functools import lru_cache
from dict2xml import dict2xml
from config import MAXSIZE_FOR_CASH


def make_dict_with_datetime_value(file):
	"""Func takes file with data in such format SVF2018-05-24_12:02:58.917
    and returns dictionary with data about abbreviation of racer and his time of start or end of best lap.
    e.g {SVF': datetime.datetime(2018, 5, 24, 12, 2, 58, 917)}

    It's used with files which have information about time of beginnign and of end of best lap
    """
	file = {line[:3]: line[3:].strip() for line in file.readlines()
	        if line != '\n'}
	res = {
		key: datetime(
			*map(
				int, ''.join([time if time.isdigit() else ' ' for time in values]).split()
			)
		)
		for key, values in file.items()
	}
	return res


def transform_abbreviations(file):
	"""It takes file with data about drivers with next content in one line: DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
        DDR - it's abbreviation> which is used for marking driver
        Daniel Ricciardo - his name
        RED BULL RACING TAG HEUER - his team

        And returns dictionary with such values:
        'DRR': ['Daniel Ricciardo', 'RED BULL RACING TAG HEUER']
        key = abbreviation
        value[0] = name of racer
        value[1] = his team
        """
	data_about_drivers = {driver.split("_")[0]: driver.strip().split("_")[1:] for driver in file.readlines()}
	return data_about_drivers


def sort_dictionary_by_time(abbreviations):
	""""This func takes dictionary with such content:
       {Abbreviation: [name of racer, his team, his time of best lap]
       Func sorts dictionary by time-parameter.
   """
	try:
		res = {value[0]: value[1:] + [k] for k, value in abbreviations.items()}
		res = dict(sorted(res.items(), key=lambda x: x[1][1]))
		return res
	except IndexError:
		raise CustomError('''Please use dictionary with data in next format: 
        {Abbreviation: [name of racer, his team, his time of best lap]''')


def build_report(start_of_race, end_of_race, data_about_drivers):
	"""This func takes 3 files with information about racers:
    1) file with time of the beginning of their best lap
    2) file with time of the end of their best lap
    3) Data about racers - theirs names, teams and abbreviations.
     It returns list of dictionaries sorted by the time with all information about drivers in next format
     {'name': 'Sebastian Vettel', 'team': 'FERRARI', 'time': datetime.timedelta(seconds=64, microseconds=999415), 'code': 'SVF'}
     """
	try:
		with open(start_of_race, "r") as start_of_race_file, open(end_of_race, "r") as end_of_race_file, open(
				data_about_drivers, "r") as data_about_drivers:
			start = make_dict_with_datetime_value(start_of_race_file)
			end = make_dict_with_datetime_value(end_of_race_file)
			data_about_drivers = transform_abbreviations(data_about_drivers)
			for element in data_about_drivers:
				data_about_drivers[element].append(abs(end[element] - start[element]))
			data_about_drivers = sort_dictionary_by_time(data_about_drivers)
			res = [{'name': key, 'team': value[0], 'time': value[1], 'code': value[2]} for key, value in
			       data_about_drivers.items()]
			return res
	except TypeError:
		raise CustomError('''You should use 3 files. 
        "Start of race" with content like "SVF2018-05-24_12:02:58.917"
        "end_of_race with content like "SVF2018-05-24_12:02:58.917"
        "abbreviations" with content like "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER"
        ''')
	except ValueError:
		raise CustomError('''You should use 3 files. 
        "Start of race" with content like "SVF2018-05-24_12:02:58.917"
        "end_of_race with content like "SVF2018-05-24_12:02:58.917"
        "abbreviations" with content like "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER"
        ''')
	except Exception as e:
		print(e)


def add_key_data(data):  # build_report()
	"""It adds to the result of build_report one more key and value: 'data': 'Sebastian Vettel | FERRARI | 0:01:04.999415'"""
	for driver in data:
		name = driver['name']
		team = driver['team']
		time = driver['time']
		info = f'{name} | {team} | {time}'
		driver['data'] = info
	return data


def name_code():
	"""It returns dictionary with next data:
    {code_of_racer: name_of_racer}"""
	res_name_code = dict([[driver.code, driver.name] for driver in DRIVERS])
	return res_name_code


@lru_cache(maxsize=MAXSIZE_FOR_CASH)
def make_one_driver_data(driver_id, drivers):
	"""It takes code of racer. And object of class Driver with data about drivers from database.
    And returns full data about this driver in next format:
    {name} | {team} | {time_of_lap}

    This function is cached with lru_cache.
    """
	one_driver_data = ''.join([driver.data for driver in DRIVERS if driver.code == driver_id])
	return one_driver_data


def make_xml(data):
	"""Takes result of build_report() and creates xml-version of report for api"""
	data = dict2xml(data)
	return data


def make_json(data):
	"""It takes result of build_report() and changes type of data with key 'time' in dictionary from datetime to str.
    And prepares data for serializing with jsonify. Because datetime can't be serialized to json"""
	res = data
	for driver in res:
		driver['time'] = str(driver['time'])
	return res
