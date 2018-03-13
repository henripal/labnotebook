from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import xpbase
from collections import defaultdict
from sqlalchemy.sql import func

"""
API definititions
"""

app = Flask(__name__)
# this is for the ability to run everything from different servers.
cors = CORS(app)
api = Api(app)

xp,ts = xpbase.initialize("postgres://postgres:1418@localhost/experiments")

def flip_dict(dict_list):
    """
    helper function to flip list of dicts to dict of lists
    """
    result = defaultdict(list)

    for dic in dict_list:
        for k, v in dic.items():
            result[k].append(v)
    
    return result

class Steps(Resource):
    def get(self, run_id):
        query = xpbase.session.query(ts.step_id,
        ts.timestep,
        ts.run_id,
        ts.trainacc,
        ts.valacc,
        ts.trainloss).filter(ts.run_id == run_id).all()
        result = xpbase.runs_schema.dump(query)[0]

        return jsonify(flip_dict(result))

class Experiments(Resource):
    def get(self):
        query = xpbase.session.query(xp.run_id,
        xp.dt,
        xp.gpu,
        xp.completed,
        xp.final_trainacc,
        xp.final_trainloss,
        xp.final_valacc,
        xp.model_desc
        ).order_by(xp.run_id.desc()).all()
        result = xpbase.xps_schema.dump(query)[0]

        return jsonify(result)

# our api:
api.add_resource(Steps, '/steps/<string:run_id>')
api.add_resource(Experiments, '/experiments')

if __name__ == '__main__':
    app.run(debug=True, port=3000)