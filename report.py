from flask import Flask, render_template, request, jsonify, make_response
from flask_restful import Resource, Api
from flasgger import Swagger
from flasgger.utils import swag_from
from work_func import make_one_driver_data, name_code, make_xml, make_json, build_report, add_key_data
from models import db, insert_data_to_db, initialize_db, DRIVERS
from config import START, END, ABBREVIATIONS

app = Flask(__name__)

api = Api(app)
swagger = Swagger(app)

app.config['JSON_AS_ASCII']=False


@app.route('/')
def index():
    """Start page. It returns information how to use this app"""
    return render_template('index.html')


@app.route("/report")
def report():
    """Returns full report about results of Monaco Race 2018. You also can choose type of sorting of this report in next format:
    /report?order=asc or /report?order=desc """
    if request.args:
        order_of_sorting = request.args.get("order")
        if order_of_sorting == 'asc': #it enumerates from 1 in asc order
            ordered_list_of_drivers = ['. '.join([str(number), driver.data]) for number, driver in enumerate(DRIVERS, 1)]
        elif order_of_sorting == 'desc': #it enumerates from 1 in desc order
            ordered_list_of_drivers = ['. '.join([str(number), driver.data]) for number, driver in enumerate(reversed(DRIVERS), 1)]
        else: #if you choose nor asc, nor desc order it returns mistake
            return make_response(jsonify({'error': 'Wrong format. Choose order of sorting: asc or desc'}), 400)
    else: #default order is asc
        ordered_list_of_drivers = ['. '.join([str(number), driver.data]) for number, driver in enumerate(DRIVERS, 1)]

    return render_template('report.html', title='report', ordered_list_of_drivers=ordered_list_of_drivers)




@app.route("/report/drivers")
def all_drivers():
    """It returns list of racers in next format:
    {name} {abbreviatiom}
    Abbreviations are active links to full data about driver"""
    if 'id' in request.args:
        driver_id = request.args['id']
        return ''.join([racer.data for racer in DRIVERS if racer.code==driver_id])
    else:
        return render_template('drivers.html', name_code=name_code())



@app.route("/report/<string:code>")
def driver_data(code):
    """It returns full data about driver if you click to his code in /report/drivers"""
    return make_one_driver_data(code, DRIVERS)


class ReportAPI_GetPost(Resource):
    """Creates class for api resource"""
    @swag_from('api_doc.yml')
    def get(self):
        """Returns api-report in xml or json formats"""
        parser = request.args.get("format")
        if parser == 'json':
            return jsonify(make_json(add_key_data(build_report(START,END,ABBREVIATIONS))))
        elif parser == 'xml':
            return make_xml(add_key_data(build_report(START,END,ABBREVIATIONS)))
        return make_response(jsonify({'error': 'Wrong format. Use json or xml'}), 400)


@app.errorhandler(404)
def not_found(error):
    """It handles errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


api.add_resource(ReportAPI_GetPost, '/api/v1/report/')


if __name__ == '__main__':
    if not db:
        """Creates db if it doesn't exist"""
        initialize_db()
        insert_data_to_db(add_key_data(build_report(START,END,ABBREVIATIONS)))
    app.run(debug=True)


