from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime as dt
import xpbase.config as config


def initialize(db_string):
    """
    initializes the engine given the database, creates session,
    and declares the Experiment and TrainingStep objects.
    """
    
    engine = create_engine(db_string)
    config.Base = declarative_base(engine)
    Session = sessionmaker(bind = engine)
    config.session = Session()

    # Experiment and TrainingStep are objects that
    # we need to access everywhere. 
    # we cannot import before knowing db_string
    global Experiment
    global TrainingStep
    from xpbase.model import Experiment, TrainingStep

    # we link the Experiment and TrainingStep objects
    Experiment.steps = relationship("TrainingStep", order_by=TrainingStep.timestep,
                               back_populates="experiment")

    # and we update the metadata
    config.Base.metadata.create_all(engine)

def start_experiment(dt = dt.datetime.now(), 
                    gpu_id = 0,
                    model_desc = None):
    """
    initializes the experiment run
    ___________
    PARAMETERS:
    ___________
    dt: the run's start time
    gpu_id: which gpu the experiment is run on
    model_desc: a dict containing the model's params, or anything else, really
    ________
    RETURNS:
    ________
    the Experiment object
    """
    xp = Experiment(dt=dt,
        gpu = gpu_id,
        model_desc = model_desc)
    config.session.add(xp)
    config.session.commit()

    return xp

def end_experiment(xp, final_trainloss=None, final_trainacc=None,
                    final_valacc=None):
    """
    closes the experiment run
    ___________
    PARAMETERS:
    ___________
    xp: the Experiment object 
    final_trainloss, final_trainacc, final_valacc: optional scalars showing the stage
    of the experiment after it ended
    ________
    RETURNS:
    ________
    an Experiment object
    """

    xp.final_trainloss = final_trainloss
    xp.final_trainacc = final_trainacc
    xp.final_valacc = final_valacc
    xp.completed = True
    config.session.commit()

    return xp

def step_experiment(xp, timestep,
        trainloss=None, trainacc=None, valacc=None,
        epoch=None, model_params=None):
    """
    add a step to the experiment
    ___________
    PARAMETERS:
    ___________
    xp: the Experiment object 
    trainloss, trainacc, valacc: optional scalars showing the state of the xp after the step
    timestep: step label
    epoch: optional epoch label
    model_params: weights of the model after the step
    ________
    RETURNS:
    ________
    a TrainingStep object
    """
    step = TrainingStep(run_id=xp.run_id, timestep=timestep,
        trainloss=trainloss, trainacc=trainacc, valacc=valacc, 
        epoch=epoch, model_params=model_params)
    config.session.add(step)
    config.session.commit()

    return step

    

