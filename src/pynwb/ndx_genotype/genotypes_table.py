from pynwb import NWBContainer, register_class
from pynwb.core import DynamicTable
from hdmf.utils import docval, get_docval, getargs, call_docval_func, AllowPositional

from . import CRIDVectorData

# NOTE: cannot write an empty genotypes table


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
            if crid[0] not in ('MGI', 'NCBI Gene', 'Ensembl'):
                return ('must be an array/list/tuple with tuples where the first element (registry) '
                        'is one of: "MGI", "NCBI Gene", or "Ensembl".')
            if not isinstance(crid[1], str):
                return 'must be an array/list/tuple with tuples where the second element (symbol) is a string.'
        return None
