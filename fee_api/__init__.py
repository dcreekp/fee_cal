# fee_api.py

from flask import Flask
from flask_restplus import Api, Resource
from fee_api.calculator import FeeCalculator


app = Flask(__name__)

api = Api(app, version='0.1', title='Fees',
          description='Given a loan and term; returns the fee.')

calculate = FeeCalculator()


@api.route('/api/v0.1/fee/<loan>/<term>', endpoint='fee')
class Fee(Resource):

    def get(self, loan, term):
        try:
            fee = calculate(float(loan), int(term))
        except ValueError as e:
            return {'message': str(e)}, 404
        return {'fee': fee}, 200
