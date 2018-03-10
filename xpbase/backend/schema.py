from marshmallow import Schema, fields, ValidationError, pre_load
import xpbase

class RunSchema(Schema):
    step_id = fields.Int()
    run_id = fields.Int()
    timestep = fields.Int()
    
    trainloss = fields.Float()
    trainacc = fields.Float()
    valacc = fields.Float()
    
    epoch = fields.Int()

run_schema = RunSchema(many=True)




