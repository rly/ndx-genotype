from pynwb import NWBContainer, register_class
from pynwb.core import DynamicTable
from pynwb.file import Subject, NWBFile

from hdmf.utils import docval, get_docval, getargs, call_docval_func, popargs, AllowPositional
from . import CRIDVectorData

# create nwbfile
# create subject
# call subject.add_genotype
# set nwbfile.subject
# or
# create nwbfile
# create genotype table
# create subject, passing in genotype table OR create subject, then set genotype table
# set nwbfile.subject

# NOTE: cannot write an empty genotypes table


def _get_nwbfile_init_docval_except_subject():
    dv = get_docval(NWBFile.__init__)
    return filter(lambda x: x['name'] != 'subject', dv)


@register_class('GenotypeNWBFile', 'ndx-genotype')
class GenotypeNWBFile(NWBFile):

    @docval(*_get_nwbfile_init_docval_except_subject(),
            {'name': 'subject',
             'type': 'GenotypeSubject',
             'doc': 'An enhanced Subject type that has an additional field for a genotype table.',
             'default': None})
    def __init__(self, **kwargs):
        subject = popargs('subject', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.subject = subject


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


# CURRENTLY UNUSED
class CRID(NWBContainer):
    """A centrally registered ID (registry-symbol pair), e.g., MGI 1343464."""

    # NOTE: this type is not mapped to a neurodata_type but useful as a type-checked, documented struct

    __nwbfields__ = (
        'registry',
        'symbol'
    )

    @docval({'name': 'registry',
             'type': str,
             'doc': 'Name of the registry. Should be either "MGI", "NCBI", or "Ensembl".',
             'enum': ['MGI', 'NCBI', 'Ensembl']},
            {'name': 'symbol',
             'type': str,
             'doc': 'Symbol (key) of the locus in the registry.'})
    def __init__(self, **kwargs):
        self.registry = getargs('registry', kwargs)
        self.symbol = getargs('symbol', kwargs)

    def to_tuple(self):
        return (self.registry, self.symbol)

    @classmethod
    def from_tuple(cls, tup):
        if len(tup) != 2:
            raise ValueError('Tuple must have length 2.')
        return CRID(tup[0], tup[1])


@register_class('GenotypesTable', 'ndx-genotype')
class GenotypesTable(DynamicTable):
    """A table to hold structured genotype information."""

    __fields__ = (
        'process',
        'process_url',
        'assembly',
        'annotation'
    )

    __columns__ = (
        {'name': 'locus_symbol',
         'description': 'Symbol/name of the locus.',
         'required': True},
        {'name': 'locus_crid',
         'description': 'Central Registry ID (CRID) of the locus.',
         'class': CRIDVectorData,
         'index': True,
         'required': True},
        {'name': 'allele1_symbol',
         'description': 'Symbol/name of the first allele.',
         'required': True},
        {'name': 'allele2_symbol',
         'description': 'Symbol/name of the second allele.',
         'required': True},
        {'name': 'locus_type',
         'description': 'Type of the locus, e.g., Gene, Transgene, Unclassified other.',
         'required': False},
        {'name': 'allele1_type',
         'description': 'Type of the first allele.',
         'required': False},
        {'name': 'allele1_crid',
         'description': 'Central Registry ID (CRID) of the first allele.',
         'class': CRIDVectorData,
         'index': True,
         'required': False},
        {'name': 'allele2_type',
         'description': 'Type of the second allele.',
         'required': False},
        {'name': 'allele2_crid',
         'description': 'Central Registry ID (CRID) of the second allele.',
         'class': CRIDVectorData,
         'index': True,
         'required': False},
        {'name': 'allele3_symbol',
         'description': 'Symbol/name of the third allele.',
         'required': False},
        {'name': 'allele3_type',
         'description': 'Type of the third allele.',
         'required': False},
        {'name': 'allele3_crid',
         'description': 'Central Registry ID (CRID) of the third allele.',
         'class': CRIDVectorData,
         'index': True,
         'required': False},
    )

    @docval({'name': 'name',
             'type': str,
             'doc': 'Name of this GenotypesTable object.',
             'default': 'genotypes_table'},
            *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
            {'name': 'description',
             'type': str,
             'doc': 'A description of what is in this table.',
             'default': 'Structured genotype information'},
            {'name': 'process',
             'type': str,
             'doc': 'Description of the process or assay used to determine the genotype, e.g., PCR.',
             'default': None},
            {'name': 'process_url',
             'type': str,
             'doc': 'URL to online document that provides further details of the protocol used.',
             'default': None},
            {'name': 'assembly',
             'type': str,
             'doc': 'Description of the assembly of the reference genome, e.g., GRCm38.p6.',
             'default': None},
            {'name': 'annotation',
             'type': str,
             'doc': ('Description of the annotation of the reference genome, '
                     'e.g., NCBI Mus musculus Annotation Release 108.'),
             'default': None},
            )
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)
        self.process = getargs('process', kwargs)
        self.process_url = getargs('process_url', kwargs)
        self.assembly = getargs('assembly', kwargs)
        self.annotation = getargs('annotation', kwargs)

    @docval({'name': 'locus_symbol',
             'type': str,
             'doc': 'Symbol/name of the locus, e.g., Rorb.'},
            {'name': 'locus_crid',
             'type': 'array_data',
             'doc': ('Central Registry ID (CRID) of the locus, e.g., MGI 1343464 => registry: MGI, symbol: 1343464. '
                     'Multiple CRIDs can be associated with each locus. At least one must be provided.'),
             'shape': (None, 2),
             },
            {'name': 'allele1_symbol',
             'type': str,
             'doc': ('Symbol/name of the first allele, e.g., Rorb-IRES2-Cre. '
                     '"wt" should be used to represent wild-type.')},
            {'name': 'allele2_symbol',
             'type': str,
             'doc': ('Symbol/name of the second allele, e.g., Rorb-IRES2-Cre. '
                     '"wt" should be used to represent wild-type.')},
            {'name': 'allele1_type',
             'type': str,
             'doc': ('Type of the first allele, e.g., Targeted (Recombinase), '
                     'Transgenic (Null/knockout, Transactivator), Targeted (Conditional ready, Inducible, Reporter).'
                     '"Wild Type" should be used to represent wild-type. Allele types can be found at: '
                     'http://www.informatics.jax.org/userhelp/ALLELE_phenotypic_categories_help.shtml#method'),
             'default': None},
            {'name': 'allele1_crid',
             'type': 'array_data',
             'doc': ('Central Registry ID (CRID) of the first allele, e.g., MGI 1343464 => registry: MGI, '
                     'symbol: 1343464. Multiple CRIDs can be associated with each allele.'),
             'default': None},
            {'name': 'allele2_type',
             'type': str,
             'doc': ('Type of the second allele, e.g., Targeted (Recombinase), '
                     'Transgenic (Null/knockout, Transactivator), Targeted (Conditional ready, Inducible, Reporter).'
                     '"Wild Type" should be used to represent wild-type. Allele types can be found at: '
                     'http://www.informatics.jax.org/userhelp/ALLELE_phenotypic_categories_help.shtml#method'),
             'default': None},
            {'name': 'allele2_crid',
             'type': 'array_data',
             'doc': ('Central Registry ID (CRID) of the second allele, e.g., MGI 1343464 => registry: MGI, '
                     'symbol: 1343464. Multiple CRIDs can be associated with each allele.'),
             'default': None},
            {'name': 'allele3_symbol',
             'type': str,
             'doc': ('Symbol/name of the third allele, e.g., Rorb-IRES2-Cre. '
                     '"wt" should be used to represent wild-type.'),
             'default': None},
            {'name': 'allele3_type',
             'type': str,
             'doc': ('Type of the third allele, e.g., Targeted (Recombinase), '
                     'Transgenic (Null/knockout, Transactivator), Targeted (Conditional ready, Inducible, Reporter).'
                     '"Wild Type" should be used to represent wild-type. Allele types can be found at: '
                     'http://www.informatics.jax.org/userhelp/ALLELE_phenotypic_categories_help.shtml#method'),
             'default': None},
            {'name': 'allele3_crid',
             'type': 'array_data',
             'doc': ('Central Registry ID (CRID) of the third allele, e.g., MGI 1343464 => registry: MGI, '
                     'symbol: 1343464. Multiple CRIDs can be associated with each allele.'),
             'default': None},
            {'name': 'id', 'type': int, 'default': None,
             'doc': 'the id for each unit'},
            allow_extra=True,
            allow_positional=AllowPositional.ERROR)
    def add_genotype(self, **kwargs):
        """Add a genotype to this table."""
        locus_crid = getargs('locus_crid', kwargs)
        if len(locus_crid) == 0:
            raise ValueError('locus_crid must be an array/list/tuple containing at least 1 CRID.')
        err_msg = GenotypesTable.__check_crid_array(locus_crid)
        if err_msg:
            raise ValueError('locus_crid %s' % err_msg)

        allele1_crid, allele2_crid, allele3_crid = getargs('allele1_crid', 'allele2_crid', 'allele3_crid', kwargs)
        if allele1_crid:
            err_msg = GenotypesTable.__check_crid_array(allele1_crid)
            if err_msg:
                raise ValueError('allele1_crid %s' % err_msg)
        if allele2_crid:
            err_msg = GenotypesTable.__check_crid_array(allele2_crid)
            if err_msg:
                raise ValueError('allele2_crid %s' % err_msg)
        if allele3_crid:
            err_msg = GenotypesTable.__check_crid_array(allele3_crid)
            if err_msg:
                raise ValueError('allele3_crid %s' % err_msg)

        allele3_symbol, allele3_type = getargs('allele3_symbol', 'allele3_type', kwargs)
        if (allele3_type or allele3_crid) and allele3_symbol is None:
            raise ValueError('allele3_symbol must be provided if allele3_type or allele3_crid are provided.')

        super().add_row(**kwargs)

    @classmethod
    def __check_crid_array(cls, arr):
        for crid in arr:
            if len(crid) != 2:
                return 'must be an array/list/tuple with tuples of length 2.'
            if crid[0] not in ('MGI', 'NCBI', 'Ensembl'):
                return ('must be an array/list/tuple with tuples where the first element (registry) '
                        'is one of: "MGI", "NCBI", or "Ensembl".')
            if not isinstance(crid[1], str):
                return 'must be an array/list/tuple with tuples where the second element (symbol) is a string.'
        return None
