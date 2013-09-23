'''
Created on Sep 20, 2013

@author: kpaskov
'''
from model_new_schema import Base, EqualityByIDMixin
from model_new_schema.bioentity import Bioentity
from model_new_schema.evidence import Evidence
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

class Protein(Bioentity):
    __tablename__ = "proteinbioentity"
    
    id = Column('bioentity_id', Integer, ForeignKey(Bioentity.id), primary_key=True)
    locus_id = Column('locus_id', Integer, ForeignKey(Bioentity.id))
    molecular_weight = Column('molecular_weight', Integer)
    length = Column('protein_length', Integer)
    n_term_seq = Column('n_term_seq', String)
    c_term_seq = Column('c_term_seq', String)
        
    __mapper_args__ = {'polymorphic_identity': 'PROTEIN',
                       'inherit_condition': id == Bioentity.id}
    
    def __init__(self, bioentity_id, display_name, format_name, 
                 locus_id, length, n_term_seq, c_term_seq, link,
                 date_created, created_by):
        Bioentity.__init__(self, bioentity_id, 'PROTEIN',  display_name, format_name, link, 'SGD', None, date_created, created_by)
        self.locus_id = locus_id
        self.length = length
        self.n_term_seq = n_term_seq
        self.c_term_seq = c_term_seq
        
class Domain(Base, EqualityByIDMixin):
    __tablename__ = "pdomain"
    
    id = Column('pdomain_id', Integer, primary_key=True)
    source = Column('source', String)
    format_name = Column('format_name', String)
    display_name = Column('display_name', String)
    description = Column('description', String)
    interpro_id = Column('interpro_id', String)
    interpro_description = Column('interpro_description', String)
    link = Column('obj_link', String)
    
    def __init__(self, format_name, display_name, description, 
                 interpro_id, interpro_description, link, source):
        self.source = source
        self.format_name = format_name
        self.display_name = display_name
        self.description = description
        self.interpro_id = interpro_id
        self.interpro_description = interpro_description
        self.link = link
        
    def unique_key(self):
        return (self.format_name, self.source)
    
class Domainevidence(Evidence):
    __tablename__ = "pdomainevidence"
    
    id = Column('evidence_id', Integer, ForeignKey(Evidence.id), primary_key=True)
    start = Column('start_index', Integer)
    end = Column('end_index', Integer)
    evalue = Column('evalue', String)
    status = Column('status', String)
    date_of_run = Column('date_of_run', String)
    protein_id = Column('protein_id', Integer, ForeignKey(Protein.id))
    domain_id = Column('pdomain_id', Integer, ForeignKey(Domain.id))
       
    __mapper_args__ = {'polymorphic_identity': 'DOMAIN',
                       'inherit_condition': id==Evidence.id}
    
    #Relationships
    domain = relationship(Domain, uselist=False)

    def __init__(self, evidence_id, reference_id, strain_id, source, 
                 start, end, evalue, status, date_of_run, protein_id, domain_id,
                 date_created, created_by):
        Evidence.__init__(self, evidence_id, 'DOMAIN', 
                          None, reference_id, strain_id, source, None,
                          date_created, created_by)
        self.start = start
        self.end = end
        self.evalue = evalue
        self.status = status
        self.date_of_run = date_of_run
        self.protein_id = protein_id
        self.domain_id = domain_id
        
        