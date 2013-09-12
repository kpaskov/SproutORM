'''
Created on May 16, 2013

@author: kpaskov
'''
from model_new_schema.bioentity import Bioentity
from model_new_schema.evidence import Evidence
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

class Regulationevidence(Evidence):
    __tablename__ = "regulationevidence"
    
    id = Column('evidence_id', Integer, ForeignKey(Evidence.id), primary_key=True)
    bioent1_id = Column('bioent1_id', Integer, ForeignKey(Bioentity.id))
    bioent2_id = Column('bioent2_id', Integer, ForeignKey(Bioentity.id))
       
    __mapper_args__ = {'polymorphic_identity': "REGULATION_EVIDENCE",
                       'inherit_condition': id==Evidence.id}

    def __init__(self, evidence_id, experiment_id, reference_id, strain_id, source, 
                 bioent1_id, bioent2_id,
                 date_created, created_by):
        Evidence.__init__(self, evidence_id, 'REGULATION_EVIDENCE', 
                          experiment_id, reference_id, strain_id, source, 
                          date_created, created_by)
        self.bioent1_id = bioent1_id
        self.bioent2_id = bioent2_id
        