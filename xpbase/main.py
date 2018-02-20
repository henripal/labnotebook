from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime as dt
import xpbase.config as config


def initialize(db_string):
    global Experiment
    global TrainingStep
    global session

    engine = create_engine(db_string)
    config.Base = declarative_base(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    from xpbase.model import Experiment, TrainingStep
    Experiment.steps = relationship("TrainingStep", order_by=TrainingStep.timestep,
                               back_populates="experiment")
    config.Base.metadata.create_all(engine)

def add_experiment(gpu, final_trainloss):
    xp = Experiment(dt=dt.datetime.now(),
    gpu = gpu,
    model_desc = {'haha': 200})
    session.add(xp)
    session.commit()

