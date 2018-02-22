from sqlalchemy import Column, Integer, Sequence,  DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from xpbase import Base


class Experiment(Base):
    __tablename__ = 'experiments'
    
    run_id = Column(Integer, Sequence('run_is_seq'), primary_key=True)
    dt = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=True) # in seconds
    gpu = Column(Integer)
    model_desc = Column(JSONB, nullable=True)
    final_trainloss = Column(Float, nullable=True)
    final_trainacc = Column(Float, nullable=True)
    final_valacc = Column(Float, nullable=True)
    completed = Column(Boolean, nullable=False, default=False, server_default='false')
    
    def __repr__(self):
        return 'Run {} on GPU {} at {}'.format(self.run_id, self.gpu, self.dt)


class TrainingStep(Base):
    __tablename__ = 'trainingsteps'
    
    # this constrains the values here
    step_id = Column(Integer, Sequence('step_id_seq'), primary_key=True)
    run_id = Column(Integer, ForeignKey('experiments.run_id'))
    timestep = Column(Integer, nullable=True)
    
    experiment = relationship("Experiment", back_populates="steps")
    
    trainloss = Column(Float, nullable=True)
    trainacc = Column(Float, nullable=True)
    valacc = Column(Float, nullable=True)
    
    epoch = Column(Integer, nullable=True)
    model_params = Column(JSONB, nullable=True)
    
    def __repr__(self):
        return 'Step {} of run {}'.format(self.timestep, self.run_id)
     
