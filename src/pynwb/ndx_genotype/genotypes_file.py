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

    __nwbfields__ = ({'name': 'genotypes_table', 'child': True, 'required_name': 'genotypes_table'},
                     {'name': 'alleles_table', 'child': True, 'required_name': 'alleles_table'}, )

    @docval(
        *get_docval(Subject.__init__),
        {
            'name': 'genotypes_table',
            'type': 'GenotypesTable',
            'doc': 'Table of genotypes.',
            'default': None,
        },
        {
            'name': 'alleles_table',
            'type': 'AllelesTable',
            'doc': 'Table of alleles.',
            'default': None,
        }
    )
    def __init__(self, **kwargs):
        genotypes_table, alleles_table = popargs('genotypes_table', 'alleles_table', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.genotypes_table = genotypes_table
        self.alleles_table = alleles_table

    def add_genotype(self, **kwargs):
        if self.genotypes_table is None:
            self.genotypes_table = GenotypesTable()
        self.genotypes_table.add_row(**kwargs)


@register_class('OntologyTable', 'ndx-genotype')
class OntologyTable(NWBTable):

    __defaultname__ = 'objects'

    __columns__ = (
        {'name': 'id', 'type': (int, np.uint64), 'doc': 'The unique identifier in this table.'},
        {'name': 'object_id', 'type': str, 'doc': 'The UUID for the object that uses this ontology term.'},
        {'name': 'field', 'type': str,
         'doc': 'The field from the object (specified by object_id) that uses this ontological term.'},
        {'name': 'item', 'type': (int, np.uint64), 'doc': 'An index into the OntologyMap that contains the term.'},
    )

    @docval(*__columns__)
    def add_row(self, **kwargs):
        id, item = popargs('id', 'item', kwargs)
        if id >= 0 and len(self.which(id=id)) == 0:
            kwargs['id'] = np.uint64(id)
        else:
            raise ValueError('id must be a non-negative integer that is not already in the table: %d' % id)
        if item >= 0:
            kwargs['item'] = np.uint64(item)
        else:
            raise ValueError('item must be a non-negative integer: %d' % id)
        return super().add_row(kwargs)

    def get_crid(self, object_id, field, key):
        """Return the CRIDs (tuple of (registry, symbol) tuples) associated with the given object_id, field, and key.
        """

        # get the values in the item column where the values in the object_id and field columns match the arguments
        oid_idx_matches = self.which(object_id=object_id)
        field_col_idx = self.__colidx__.get('field')
        item_col_idx = self.__colidx__.get('item')
        terms_indices = list()
        for i in oid_idx_matches:
            row = self.data[i]
            field_val = row[field_col_idx]
            if field_val == field:
                item_val = row[item_col_idx]
                terms_indices.append(item_val)

        nwbfile = super().get_ancestor(neurodata_type='GenotypeNWBFile')  # TODO changeme
        if nwbfile is None:
            raise ValueError('NWBFile must be an ancestor of the OntologyTable.')

        if nwbfile.ontology_terms is None:
            raise ValueError('NWBFile.ontology_terms must exist.')

        key_col_idx = OntologyMap.__colidx__.get('key')
        ontology_col_idx = OntologyMap.__colidx__.get('ontology')
        uri_col_idx = OntologyMap.__colidx__.get('uri')

        ret = list()
        for i in terms_indices:
            terms_row = nwbfile.ontology_terms.data[i]
            key_val = terms_row[key_col_idx]
            if key_val == key:
                ontology_val = terms_row[ontology_col_idx]
                uri_val = terms_row[uri_col_idx]
                ret.append((ontology_val, uri_val))

        return tuple(ret)


@register_class('OntologyMap', 'ndx-genotype')
class OntologyMap(NWBTable):

    __defaultname__ = 'terms'

    __columns__ = (
        {'name': 'id', 'type': (int, np.uint64), 'doc': 'The unique identifier in this table.'},
        {'name': 'key', 'type': str, 'doc': 'The user key that maps to the ontology term / registry symbol.'},
        {'name': 'ontology', 'type': str, 'doc': 'The ontology/registry that the term/symbol comes from.'},
        {'name': 'uri', 'type': str, 'doc': 'The unique resource identifier for the ontology term / registry symbol.'},
    )

    @docval(*__columns__)
    def add_row(self, **kwargs):
        id = popargs('id', kwargs)
        if id >= 0 and len(self.which(id=id)) == 0:
            kwargs['id'] = np.uint64(id)
        else:
            raise ValueError('id must be a non-negative integer that is not already in the table: %d' % id)
        return super().add_row(kwargs)
