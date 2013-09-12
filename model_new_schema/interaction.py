'''
Created on May 16, 2013

@author: kpaskov
'''
from model_new_schema.bioentity import Bioentity
from model_new_schema.evidence import Evidence
from model_new_schema.phenotype import Phenotype
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

class GeneticInterevidence(Evidence):
    __tablename__ = "geneticinterevidence"
    
    id = Column('evidence_id', Integer, ForeignKey(Evidence.id), primary_key=True)
    phenotype_id = Column('phenotype_id', Integer, ForeignKey(Phenotype.id))
    annotation_type = Column('annotation_type', String)
    bait_hit = Column('bait_hit', String)
    bioent1_id = Column('bioent1_id', Integer, ForeignKey(Bioentity.id))
    bioent2_id = Column('bioent2_id', Integer, ForeignKey(Bioentity.id))
    note = Column('note', String)
       
    __mapper_args__ = {'polymorphic_identity': "GENETIC_INTERACTION_EVIDENCE",
                       'inherit_condition': id==Evidence.id}
    
    #Relationships
    phenotype = relationship(Phenotype)

    def __init__(self, evidence_id, experiment_id, reference_id, strain_id, source, 
                 bioent1_id, bioent2_id, phenotype_id, annotation_type, bait_hit, note, 
                 date_created, created_by):
        Evidence.__init__(self, evidence_id, 'GENETIC_INTERACTION_EVIDENCE', 
                          experiment_id, reference_id, strain_id, source, 
                          date_created, created_by)
        self.bioent1_id = bioent1_id
        self.bioent2_id = bioent2_id
        self.phenotype_id = phenotype_id
        self.annotation_type = annotation_type
        self.bait_hit = bait_hit
        self.note = note
        
class PhysicalInterevidence(Evidence):
    __tablename__ = "physicalinterevidence"
    
    id = Column('evidence_id', Integer, ForeignKey(Evidence.id), primary_key=True)
    modification = Column('modification', String)
    annotation_type = Column('annotation_type', String)
    bait_hit = Column('bait_hit', String)
    bioent1_id = Column('bioent1_id', Integer, ForeignKey(Bioentity.id))
    bioent2_id = Column('bioent2_id', Integer, ForeignKey(Bioentity.id))
    note = Column('note', String)
            
    __mapper_args__ = {'polymorphic_identity': "PHYSICAL_INTERACTION_EVIDENCE",
                       'inherit_condition': id==Evidence.id}
    
        
    def __init__(self, evidence_id, experiment_id, reference_id, strain_id, source,
                 bioent1_id, bioent2_id, annotation_type, modification, bait_hit, note, 
                 date_created, created_by):
        Evidence.__init__(self, evidence_id, 'PHYSICAL_INTERACTION_EVIDENCE', 
                          experiment_id, reference_id, strain_id, source, 
                          date_created, created_by)
        self.bioent1_id = bioent1_id
        self.bioent2_id = bioent2_id
        self.annotation_type = annotation_type
        self.modification = modification
        self.bait_hit = bait_hit
        self.note = note

        
        
        