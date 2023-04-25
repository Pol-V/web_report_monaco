from peewee import Model, CharField, TimeField
from config import db



class Driver(Model):
    name = CharField()
    team = CharField()
    time = TimeField()
    code = CharField(primary_key=True)
    data = CharField()

    class Meta:
        database = db
        order_by = ('time',)



def initialize_db():
    db.connect()
    db.create_tables([Driver], safe = True)
    db.close()




def insert_data_to_db(data):
    for racer in data:
        driver = Driver.create(name=racer['name'], team=racer['team'], time=racer['time'], code=racer['code'], data=racer['data'])
        driver.save()


DRIVERS = Driver.select()