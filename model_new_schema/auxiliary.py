'''
Created on Aug 8, 2013

@author: kpaskov
'''
from model_new_schema import Base, EqualityByIDMixin
from model_new_schema.bioconcept import Bioconcept
from model_new_schema.bioentity import Bioentity
from model_new_schema.reference import Reference
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

class Biofact(Base, EqualityByIDMixin):
    __tablename__ = 'biofact'

    id = Column('biofact_id', Integer, primary_key=True)
    bioent_id = Column('bioent_id', Integer, ForeignKey(Bioentity.id))
    biocon_id = Column('biocon_id', Integer, ForeignKey(Bioconcept.id))
    biocon_type = Column('biocon_type', String)
    type = "BIOFACT"
    
    def __init__(self, bioent_id, biocon_id, biocon_type):
        self.bioent_id = bioent_id
        self.biocon_id = biocon_id
        self.biocon_type = biocon_type

    def unique_key(self):
        return (self.bioent_id, self.biocon_id, self.biocon_type)
    
class Interaction(Base, EqualityByIDMixin):
    __tablename__ = "interaction"
    
    id = Column('interaction_id', Integer, primary_key = True)
    interaction_type = Column('interaction_type', String)
    format_name = Column('format_name', String)
    display_name = Column('display_name', String)
    bioent1_id = Column('bioent1_id', Integer)
    bioent2_id = Column('bioent2_id', Integer)
    evidence_count = Column('evidence_count', Integer)
    type = 'INTERACTION'
    
    def __init__(self, interaction_id, interaction_type, display_name, format_name, bioent1_id, bioent2_id):
        self.id = interaction_id
        self.interaction_type = interaction_type
        self.display_name = display_name
        self.format_name = format_name
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

class BioconAncestor(Base, EqualityByIDMixin):
    __tablename__ = 'biocon_ancestor'

    id = Column('biocon_ancestor_id', Integer, primary_key=True)
    ancestor_id = Column('ancestor_biocon_id', Integer, ForeignKey(Bioconcept.id))
    child_id = Column('child_biocon_id', Integer, ForeignKey(Bioconcept.id))
    generation = Column('generation', Integer)
    bioconanc_type = Column('bioconanc_type', String)
   
    ancestor_biocon = relationship('Bioconcept', uselist=False, backref=backref('child_family', cascade='all,delete'), primaryjoin="BioconAncestor.ancestor_id==Bioconcept.id")
    child_biocon = relationship('Bioconcept', uselist=False, backref=backref('parent_family', cascade='all,delete'), primaryjoin="BioconAncestor.child_id==Bioconcept.id")
    type = "BIOCON_ANCESTOR"

    def __init__(self, ancestor_id, child_id, bioconanc_type, generation):
        self.ancestor_id = ancestor_id
        self.child_id = child_id
        self.bioconanc_type = bioconanc_type
        self.generation = generation

    def unique_key(self):
        return (self.ancestor_id, self.child_id, self.bioconanc_type)

class BioentReference(Base):
    __tablename__ = 'bioent_reference'
    
    id = Column('bioent_reference_id', Integer, primary_key=True)
    bioent_id = Column('bioent_id', Integer, ForeignKey("sprout.bioent.bioent_id"))
    reference_id = Column('reference_id', Integer, ForeignKey(Reference.id))
    bioent_ref_type = Column('bioent_ref_type', String)
    
    def __init__(self, bioent_ref_type, bioent_id, reference_id):
        self.bioent_ref_type = bioent_ref_type
        self.bioent_id = bioent_id
        self.reference_id = reference_id
        
    def unique_key(self):
        return (self.bioent_id, self.reference_id, self.bioent_ref_type)