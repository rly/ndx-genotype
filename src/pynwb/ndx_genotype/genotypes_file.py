import numpy as np

from pynwb import register_class
from pynwb.core import NWBTable
from pynwb.file import Subject, NWBFile
from hdmf.utils import docval, get_docval, call_docval_func, popargs

from .genotypes_table import GenotypesTable


def _get_nwbfile_init_docval_except_subject():
    dv = get_docval(NWBFile.__init__)
    return filter(lambda x: x['name'] != 'subject', dv)


@register_class('GenotypeNWBFile', 'ndx-genotype')
class GenotypeNWBFile(NWBFile):

    __nwbfields__ = ({'name': 'ontology_objects', 'child': True, 'required_name': 'objects'},
                     {'name': 'ontology_terms', 'child': True, 'required_name': 'terms'}, )

    @docval(*_get_nwbfile_init_docval_except_subject(),
            {'name': 'subject',
             'type': 'GenotypeSubject',
             'doc': 'An enhanced Subject type that has an additional field for a genotype table.',
             'default': None},
            {'name': 'ontology_objects',
             'type': 'OntologyTable',
             'doc': 'The objects that conform to an ontology.',
             'default': None},
            {'name': 'ontology_terms',
             'type': 'OntologyMap',
             'doc': 'The ontological terms that get used in this file.',
             'default': None},)
    def __init__(self, **kwargs):
        subject = popargs('subject', kwargs)
        ontology_objects, ontology_terms = popargs('ontology_objects', 'ontology_terms', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.subject = subject
        if ontology_objects is not None:
            self.ontology_objects = ontology_objects
        else:
            self.ontology_objects = OntologyTable()
        if ontology_terms is not None:
            self.ontology_terms = ontology_terms
        else:
            self.ontology_terms = OntologyMap()


@register_class('GenotypeSubject', 'ndx-genotype')
class GenotypeSubject(Subject):

    __nwbfields__ = ({'name': 'genotypes_table', 'child': True, 'required_name': 'genotypes_table'}, )

    @docval(*get_docval(Subject.__init__),
            {'name': 'genotypes_table',
             'type': 'GenotypesTable',
             'doc': 'Table of genotypes.',
             'default': None})
    def __init__(self, **kwargs):
        genotypes_table = popargs('genotypes_table', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.genotypes_table = genotypes_table

    def add_genotype(self, **kwargs):
        if self.genotypes_table is None:
            self.genotypes_table = GenotypesTable()
        self.genotypes_table.add_row(**kwargs)


@register_class('OntologyTable', 'ndx-genotype')
class OntologyTable(NWBTable):

    __defaultname__ = 'objects'

    __columns__ = (
        {'name': 'id', 'type': np.uint64, 'doc': 'The unique identifier in this table.'},
        {'name': 'object_id', 'type': str, 'doc': 'The UUID for the object that uses this ontology term.'},
        {'name': 'field', 'type': str,
         'doc': 'The field from the object (specified by object_id) that uses this ontological term.'},
        {'name': 'item', 'type': np.uint64, 'doc': 'An index into the OntologyMap that contains the term.'},
    )


@register_class('OntologyMap', 'ndx-genotype')
class OntologyMap(NWBTable):

    __defaultname__ = 'terms'

    __columns__ = (
        {'name': 'id', 'type': np.uint64, 'doc': 'The unique identifier in this table.'},
        {'name': 'key', 'type': str, 'doc': 'The user key that maps to the ontology term / registry symbol.'},
        {'name': 'ontology', 'type': str, 'doc': 'The ontology/registry that the term/symbol comes from.'},
        {'name': 'uri', 'type': str, 'doc': 'The unique resource identifier for the ontology term / registry symbol.'},
    )
