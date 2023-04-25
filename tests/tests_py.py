from peewee import SqliteDatabase
from work_func import name_code, make_one_driver_data, build_report, add_key_data
from models import insert_data_to_db, initialize_db, DRIVERS
from tests import client
from config import ABBREVIATIONS, END, START
import json



DATA = add_key_data(build_report(START,END,ABBREVIATIONS))



if not 'drivers.db':
    db = SqliteDatabase('drivers.db')
    initialize_db()
    insert_data_to_db(DATA)


def test_make_one_driver_data():
	assert make_one_driver_data('DRR', DRIVERS)=='Daniel Ricciardo | RED BULL RACING TAG HEUER | 0:02:47.999987'

def test_name_code():
    assert name_code() == {'SVF': 'Sebastian Vettel', 'VBM': 'Valtteri Bottas', 'KRF': 'Kimi Räikkönen', 'SPF': 'Sergio Perez', 'SVM': 'Stoffel Vandoorne', 'FAM': 'Fernando Alonso', 'CLS': 'Charles Leclerc', 'RGH': 'Romain Grosjean', 'PGS': 'Pierre Gasly', 'CSR': 'Carlos Sainz', 'NHR': 'Nico Hulkenberg', 'MES': 'Marcus Ericsson', 'LSW': 'Lance Stroll', 'KMH': 'Kevin Magnussen', 'BHS': 'Brendon Hartley', 'DRR': 'Daniel Ricciardo', 'SSW': 'Sergey Sirotkin', 'EOF': 'Esteban Ocon', 'LHM': 'Lewis Hamilton'}




def test_landing(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Report of Monaco race 2018' in html

    assert "<p>Hello, it's web-report with results of race in Monaco 2018. </p>" in html
    assert "/report </a>  shows common statistics <br>" in html
    assert "/report/drivers </a>  shows a list of driver's names and codes." in html
    assert "report/drivers?id=SVF or /report/SVF </a> shows info about a driver" in html



def test_report(client):
    landing = client.get("/report")
    html = landing.data.decode()
    res = DATA
    for driver in res:
	    assert driver['data'] in html


def test_report_desc(client):
    landing = client.get("/report?order=desc")
    html = landing.data.decode()
    res = DATA
    for driver in res:
	    assert driver['data'] in html


def test_get_error(client):
    landing = client.get("/api/v1/report/")
    res = landing.data.decode()
    assert 'Wrong format. Use json or xml' in res



def test_get_json(client):
    landing = client.get("/api/v1/report/?format=json")
    res = json.loads(landing.data.decode())
    fl = False
    for part in res:
        if 'Lewis Hamilton | MERCEDES | 0:06:47.999540' in part['data']:
            fl = True
    assert fl is True



def test_get_xml(client):
    landing = client.get("/api/v1/report/?format=xml")
    res = landing.data.decode()
    print(res)
    fl = False
    if 'Lewis Hamilton | MERCEDES | 0:06:47.999540' in res:
        fl = True
    assert fl is True

