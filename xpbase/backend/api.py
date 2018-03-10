from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask.ext.cors import CORS, cross_origin
import xpbase
from collections import defaultdict

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
api = Api(app)

xp,ts = xpbase.initialize("postgres://postgres:1418@localhost/experiments")

class HelloWorld(Resource):
    def get(self):
        query = xpbase.session.query(ts.step_id,
        ts.timestep,
        ts.run_id,
        ts.trainacc,
        ts.valacc,
        ts.trainloss).filter(ts.run_id == 32).all()
        result = xpbase.run_schema.dump(query)[0]
        # final_result = defaultdict(list)
        # for dic in result[1:]:
        #     for k, v in dic.items():
        #         final_result[k].append(v)

        return jsonify(obj=result, many=True)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, port=3000)