'''
Created on Nov 6, 2012

@author: kpaskov

This is some test code to experiment with working with SQLAlchemy - particularly the Declarative style. These classes represent what 
will eventually be the Bioentity classes/tables in the new SGD website schema. This code is currently meant to run on the KPASKOV 
schema on fasolt.
'''
from model_new_schema import Base, EqualityByIDMixin
from model_new_schema.misc import Alias, Url
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Float

class Bioentity(Base, EqualityByIDMixin):
    __tablename__ = 'bioent'
    
    id = Column('bioent_id', Integer, primary_key=True)
    display_name = Column('display_name', String)
    format_name = Column('format_name', String)
    link = Column('obj_link', String)
    bioent_type = Column('bioent_type', String)
    source = Column('source', String)
    status = Column('status', String)
    
    date_created = Column('date_created', Date)
    created_by = Column('created_by', String)
    
    __mapper_args__ = {'polymorphic_on': bioent_type,
                       'polymorphic_identity':"BIOENTITY"}
    
    #Relationships
    aliases = association_proxy('bioentaliases', 'name')
    type = "BIOENTITY"
            
    def __init__(self, bioent_id, bioent_type, display_name, format_name, link, source, status,
                 date_created, created_by):
        self.id = bioent_id
        self.bioent_type = bioent_type
        self.display_name = display_name
        self.format_name = format_name
        self.link = link
        self.source = source
        self.status = status
        self.date_created = date_created
        self.created_by = created_by
            
    def unique_key(self):
        return (self.format_name, self.bioent_type)
    
    @hybrid_property
    def alias_str(self):
        return ', '.join(self.aliases)
    
    
class BioentAlias(Alias):
    __tablename__ = 'bioentalias'
    
    id = Column('alias_id', Integer, ForeignKey(Alias.id), primary_key=True)
    bioent_id = Column('bioent_id', Integer, ForeignKey(Bioentity.id))
    
    __mapper_args__ = {'polymorphic_identity': 'BIOENT_ALIAS',
                       'inherit_condition': id == Alias.id}
        
    #Relationships
    bioent = relationship(Bioentity, uselist=False, backref=backref('bioentaliases', passive_deletes=True))
        
    def __init__(self, name, source, used_for_search, bioent_id, date_created, created_by):
        Alias.__init__(self, name, 'BIOENT_ALIAS', source, used_for_search, date_created, created_by)
        self.bioent_id = bioent_id
        
    def unique_key(self):
        return (self.name, self.bioent_id)
    
class BioentUrl(Url):
    __tablename__ = 'bioenturl'
    id = Column('url_id', Integer, ForeignKey(Url.id), primary_key=True)
    bioent_id = Column('bioent_id', ForeignKey(Bioentity.id))
    
    __mapper_args__ = {'polymorphic_identity': 'BIOENT_URL',
                       'inherit_condition': id == Url.id}
    
    #Relationships
    reference = relationship(Bioentity, uselist=False, backref=backref('urls', passive_deletes=True))
    
    def __init__(self, url, display_name, category, source, bioent_id, date_created, created_by):
        Url.__init__(self, url, display_name, category, 'BIOENT_URL', source, date_created, created_by)
        self.bioent_id = bioent_id
        
    def unique_key(self):
        return (self.url, self.category, self.bioent_id)
                       
class Locus(Bioentity):
    __tablename__ = "locus"
    
    id = Column('bioent_id', Integer, ForeignKey(Bioentity.id), primary_key=True)
    qualifier = Column('qualifier', String)
    attribute = Column('attribute', String)
    name_description = Column('name_description', String)
    headline = Column('headline', String)
    description = Column('description', String)
    genetic_position = Column('genetic_position', String)
    locus_type = Column('locus_type', String)
    type = "LOCUS"
        
    __mapper_args__ = {'polymorphic_identity': 'LOCUS',
                       'inherit_condition': id == Bioentity.id}
    
    def __init__(self, bioent_id, display_name, format_name, link, source, status, 
                 locus_type, qualifier, attribute, short_description, headline, description, genetic_position,
                 date_created, created_by):
        Bioentity.__init__(self, bioent_id, 'LOCUS',  display_name, format_name, link, source, status, date_created, created_by)
        self.locus_type = locus_type
        self.qualifier = qualifier
        self.attribute = attribute
        self.short_description = short_description
        self.headline = headline
        self.description = description
        self.genetic_position = genetic_position
        
class DNA(Bioentity):
    __tablename__ = 'dna'
    
    id = Column('bioent_id', Integer, ForeignKey(Bioentity.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'DNA',
                       'inherit_condition': id == Bioentity.id}
    
    @hybrid_property
    def search_additional(self):
        return None
    @hybrid_property
    def search_entry_type(self):
        return 'DNA'

    def __init__(self, bioent_id, display_name, format_name, link, date_created, created_by):
        Bioentity.__init__(self, bioent_id, 'DNA', display_name, format_name, link, 'SGD', None, date_created, created_by)

class RNA(Bioentity):
    __tablename__ = 'rna'
    
    id = Column('bioent_id', Integer, ForeignKey(Bioentity.id), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'RNA',
                       'inherit_condition': id == Bioentity.id}
    
    @hybrid_property
    def search_additional(self):
        return None
    @hybrid_property
    def search_entry_type(self):
        return 'DNA'

    def __init__(self, bioent_id, display_name, format_name, link, date_created, created_by):
        Bioentity.__init__(self, bioent_id, 'RNA', display_name, format_name, link, 'SGD', None, date_created, created_by)


class Protein(Bioentity):
    __tablename__ = "protein"
    
    id = Column('bioent_id', Integer, ForeignKey(Bioentity.id), primary_key=True)
    
    molecular_weight = Column('molecular_weight', Integer)
    pi = Column('pi', Float)
    cai = Column('cai', Float)
    length = Column('length', Integer)
    n_term_seq = ('n_term_seq', String)
    c_term_seq = ('c_term_seq', String)
    codon_bias = ('codon_bias', Float)
    fop_score = Column('fop_score', Float)
    gravy_score = Column('gravy_score', Float)
    aromaticity_score = Column('aromaticity_score', Float)
    type = "PROTEIN"
    
    ala = Column('ala', Integer)
    arg = Column('arg', Integer)
    asn = Column('asn', Integer)
    asp = Column('asp', Integer)
    cys = Column('cys', Integer)
    gln = Column('gln', Integer)
    glu = Column('glu', Integer)
    gly = Column('gly', Integer)
    his = Column('his', Integer)
    ile = Column('ile', Integer)
    leu = Column('leu', Integer)
    lys = Column('lys', Integer)
    met = Column('met', Integer)
    phe = Column('phe', Integer)
    pro = Column('pro', Integer)
    thr = Column('thr', Integer)
    ser = Column('ser', Integer)
    trp = Column('trp', Integer)
    tyr = Column('tyr', Integer)
    val = Column('val', Integer)
    
    aliphatic_index = Column('aliphatic_index', Float)
    atomic_comp_H = Column('atomic_comp_h', Integer)
    atomic_comp_S = Column('atomic_comp_s', Integer)
    atomic_comp_N = Column('atomic_comp_n', Integer)
    atomic_comp_O = Column('atomic_comp_o', Integer)
    atomic_comp_C = Column('atomic_comp_c', Integer)
    
    instability_index = Column('instability_index', Float)
    molecules_per_cell = Column('molecules_per_cell', Integer)
         
    __mapper_args__ = {'polymorphic_identity': "PROTEIN",
                       'inherit_condition': id == Bioentity.id}
    

    @hybrid_property
    def search_entry(self):
        entry = ''
        if len(self.aliases) > 0:
            entry = '<span class="muted">Aliases: ' + self.alias_str + '</span><br>'
        return entry
    @hybrid_property
    def search_entry_type(self):
        return 'Protein'
    
    def get_percent_aa(self, aa_abrev):
        return "{0:.2f}".format(100*float(getattr(self, aa_abrev))/self.length) + '%'

    def __init__(self, bioent_id, display_name, format_name, link,
                 molecular_weight, pi, cai, length, n_term_seq, c_term_seq,
                 codon_bias, fop_score, gravy_score, aromaticity_score, 
                 ala, arg, asn, asp, cys, gln, glu, gly, his, ile, leu, lys, met, phe, pro, thr, ser, trp, tyr, val, 
                 aliphatic_index, atomic_comp_H, atomic_comp_S, atomic_comp_N, atomic_comp_O, atomic_comp_C,
                 instability_index, molecules_per_cell,
                 date_created, created_by):
        Bioentity.__init__(self, bioent_id, 'PROTEIN', display_name, format_name, link, 'SGD', None, date_created, created_by)
        
        self.molecular_weight = molecular_weight
        self.pi = pi
        self.cai = cai
        self.length = length
        self.n_term_seq = n_term_seq
        self.c_term_seq = c_term_seq
        self.codon_bias = codon_bias
        self.fop_score = fop_score
        self.gravy_score = gravy_score
        self.aromaticity_score = aromaticity_score
        
        self.ala = ala
        self.arg = arg
        self.asn = asn
        self.asp = asp
        self.cys = cys
        self.gln = gln
        self.glu = glu
        self.gly = gly
        self.his = his
        self.ile = ile
        self.leu = leu
        self.lys = lys
        self.met = met
        self.phe = phe
        self.pro = pro
        self.thr = thr
        self.ser = ser
        self.trp = trp
        self.tyr = tyr
        self.val = val
        
        self.aliphatic_index = aliphatic_index
        self.atomic_comp_H = atomic_comp_H
        self.atomic_comp_S = atomic_comp_S
        self.atomic_comp_N = atomic_comp_N
        self.atomic_comp_O = atomic_comp_O
        self.atomic_comp_C = atomic_comp_C
        
        self.instability_index = instability_index
        self.molecules_per_cell = molecules_per_cell
        
        