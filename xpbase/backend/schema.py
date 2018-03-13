from marshmallow import Schema, fields, ValidationError, pre_load
import xpbase

"""
We define the schemas using marshmallow for
easy serialization and validation.
This is a little sensitive since if the model changes,
this also needs to be changed, but we can't use
the flask_sqlalchemy / flask_marshmallo magic because
of our JSONB fields.
"""

class ExperimentSchema(Schema):
    run_id = fields.Int()
    dt = fields.DateTime("%Y-%m-%d %H:%m")
    duration = fields.Int()
    gpu = fields.Int()
    model_desc = fields.Raw()
    final_trainloss = fields.Float()
    final_trainacc = fields.Float()
    final_valacc = fields.Float()
    completed = fields.Boolean()
    steps = fields.Nested('RunSchema', many=True, exclude=('experiment',))

class RunSchema(Schema):
    step_id = fields.Int()
    run_id = fields.Int()
    timestep = fields.Int()
    
    trainloss = fields.Float()
    trainacc = fields.Float()
    valacc = fields.Float()
    
    epoch = fields.Int()

    model_params = fields.Raw()
    experiment = fields.Nested(ExperimentSchema)

runs_schema = RunSchema(many=True)
run_schema = RunSchema()
xps_schema = ExperimentSchema(many=True)
xp_schema = ExperimentSchema()
