'''
Created on May 16, 2013

@author: kpaskov
'''
from model_new_schema import Base, EqualityByIDMixin
from model_new_schema.bioentity import Bioentity
from model_new_schema.evidence import Evidence
from model_new_schema.phenotype import Phenotype
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

class Interaction(Base, EqualityByIDMixin):
    __tablename__ = "interaction"
    
    id = Column('interaction_id', Integer, primary_key = True)
    interaction_type = Column('interaction_type', String)
    format_name = Column('format_name', String)
    display_name = Column('display_name', String)
    link = Column('obj_link', String)
    bioent1_id = Column('bioent1_id', Integer)
    bioent2_id = Column('bioent2_id', Integer)
    evidence_count = Column('evidence_count', Integer)
    type = 'INTERACTION'
    
    def __init__(self, interaction_id, interaction_type, display_name, format_name, link, bioent1_id, bioent2_id):
        self.id = interaction_id
        self.interaction_type = interaction_type
        self.display_name = display_name
        self.format_name = format_name
        self.link = link
        self.bioent1_id = bioent1_id
        self.bioent2_id = bioent2_id
        
    def unique_key(self):
        return (self.format_name, self.interaction_type)
    
    
class InteractionFamily(Base, EqualityByIDMixin):
    __tablename__ = "interaction_family"
    
    id = Column('interaction_family_id', Integer, primary_key = True)
    bioent_id = Column('bioent_id', Integer)
    bioent1_id = Column('bioent1_id', Integer)
    bioent2_id = Column('bioent2_id', Integer)
    evidence_count = Column('evidence_count', Integer)
    genetic_ev_count = Column('gen_ev_count', Integer)
    physical_ev_count = Column('phys_ev_count', Integer)
    
    def __init__(self, bioent_id, bioent1_id, bioent2_id, 
                 genetic_ev_count, physical_ev_count, evidence_count):
        self.bioent_id = bioent_id
        self.bioent1_id = bioent1_id
        self.bioent2_id = bioent2_id
        self.genetic_ev_count = genetic_ev_count
        self.physical_ev_count = physical_ev_count
        self.evidence_count = evidence_count
        
    def unique_key(self):
        return (self.bioent_id, self.bioent1_id, self.bioent2_id)

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
    bioent1_name_with_link = Column('bioent1_name_with_link', String)
    bioent2_name_with_link = Column('bioent2_name_with_link', String)
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

        
        
        