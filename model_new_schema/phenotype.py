'''
Created on May 15, 2013

@author: kpaskov
'''
from model_new_schema.bioconcept import Bioconcept
from model_new_schema.bioentity import Bioentity
from model_new_schema.evidence import Evidence
from model_new_schema.misc import Allele
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Float


class Phenotype(Bioconcept):
    __tablename__ = "phenotype"
    
    id = Column('biocon_id', Integer, ForeignKey(Bioconcept.id), primary_key = True)
    observable = Column('observable', String)
    qualifier = Column('qualifier', String)
    mutant_type = Column('mutant_type', String)
    phenotype_type = Column('phenotype_type', String)
    direct_gene_count = Column('direct_gene_count', Integer)
    type = "PHENOTYPE"
       
    __mapper_args__ = {'polymorphic_identity': "PHENOTYPE",
                       'inherit_condition': id==Bioconcept.id}

    def __init__(self, biocon_id, display_name, format_name, link,
                 observable, qualifier, mutant_type, phenotype_type, 
                 date_created, created_by):
        Bioconcept.__init__(self, biocon_id, 'PHENOTYPE', display_name, format_name, link, None, 
                            date_created, created_by)
        self.observable = observable
        self.qualifier = qualifier
        self.mutant_type = mutant_type
        self.phenotype_type = phenotype_type
        
class Phenoevidence(Evidence):
    __tablename__ = "phenoevidence"
    
    id = Column('evidence_id', Integer, ForeignKey(Evidence.id), primary_key=True)
    allele_id = Column('allele_id', Integer, ForeignKey(Allele.id))
    
    reporter = Column('reporter', String)
    reporter_desc = Column('reporter_desc', String)
    allele_info = Column('allele_info', String)
    strain_details = Column('strain_details', String)
    details = Column('details', String)
    experiment_details = Column('experiment_details', String)
    conditions = Column('conditions', String)
    
    budding_index = Column('budding_index', String)
    glutathione_excretion = Column('glutathione_excretion', String)
    z_score = Column('z_score', String)
    relative_fitness_score = Column('relative_fitness_score', Float)
    chitin_level = Column('chitin_level', Float)

    bioent_id = Column('bioent_id', Integer, ForeignKey(Bioentity.id))
    biocon_id = Column('biocon_id', Integer, ForeignKey(Phenotype.id))
    
    type = 'BIOCON_EVIDENCE'
    
    #Relationship
    bioentity = relationship(Bioentity, uselist=False)
    bioconcept = relationship(Phenotype, uselist=False)
    allele = relationship(Allele, lazy='subquery', uselist=False, backref='phenoevidences')

    __mapper_args__ = {'polymorphic_identity': "PHENOTYPE_EVIDENCE",
                       'inherit_condition': id==Evidence.id}
    
    def __init__(self, evidence_id, experiment_id, reference_id, strain_id, source,
                 bioent_id, biocon_id, allele_id, 
                 allele_info, reporter, reporter_desc, strain_details, experiment_details, conditions, details,
                 date_created, created_by):
        Evidence.__init__(self, evidence_id, 'PHENOTYPE_EVIDENCE', experiment_id, reference_id, strain_id, source, 
                          date_created, created_by)
        self.bioent_id = bioent_id
        self.biocon_id = biocon_id
        self.allele_id = allele_id
        
        self.allele_info = allele_info
        self.reporter = reporter
        self.reporter_desc = reporter_desc
        self.strain_details = strain_details
        self.experiment_details = experiment_details
        self.conditions = conditions
        self.details = details

    
        
        

    