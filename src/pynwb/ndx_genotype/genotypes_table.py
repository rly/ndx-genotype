from pynwb import register_class
from pynwb.core import DynamicTable
from hdmf.utils import docval, get_docval, getargs, popargs, call_docval_func, AllowPositional


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
        {'name': 'locus',
         'description': 'Symbol/name of the locus.',
         'required': True},
        {'name': 'allele1',
         'description': '...',
         'table': True,
         'required': True},
        {'name': 'allele2',
         'description': '...',
         'table': True,
         'required': False},
        {'name': 'allele3',
         'description': '...',
         'table': True,
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

    @docval(
        {
            'name': 'locus',
            'type': str,
            'doc': 'Symbol/name of the locus, e.g., Rorb.',
        },
        {
            'name': 'allele1',
            'type': DynamicTableRegion,
            'doc': ('...'),
        },
        {
            'name': 'allele2',
            'type': DynamicTableRegion,
            'doc': ('...'),
        },
        {
            'name': 'allele3',
            'type': DynamicTableRegion,
            'doc': ('...'),
            'default': None,
        },
        {
            'name': 'locus_resource_name',
            'type': str,
            'doc': '...',
            'default': None,
        },
        {
            'name': 'locus_resource_uri',
            'type': str,
            'doc': '...',
            'default': None,
        },
        {
            'name': 'locus_entity_id',
            'type': str,
            'doc': '...',
            'default': None,
        },
        {
            'name': 'locus_entity_uri',
            'type': str,
            'doc': '...',
            'default': None,
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR
    )
    def add_genotype(self, **kwargs):
        """Add a genotype to this table."""
        super().add_row(**kwargs)

        locus = getargs('locus', kwargs)
        locus_resource_name, locus_resource_uri, locus_entity_id, locus_entity_uri = getargs('locus_resource_name', 'locus_resource_uri', 'locus_entity_id', 'locus_entity_uri', kwargs)
        
        nwbfile = self.get_the_nwb_file()  # TODO
        nwbfile.external_resources.add_ref(
            container=self, 
            field='locus', 
            key=locus, 
            resource_name=locus_resource_name,
            resource_uri=locus_resource_urim
            entity_id=locus_entity_id,
            entity_uri=locus_entity_uri
        )

    def __add_crid(self, field_name, symbol, crid_arr):
        """Add a CRID to the NWBFile ontology table.

        Example usage: self.__add_crid('locus_symbol', 'Rorb', [('MGI', 'MGI:1343464')])
        """

        nwbfile = super().get_ancestor(data_type='GenotypeNWBFile')  # TODO changeme
        if nwbfile is None:
            raise ValueError('Cannot add CRID values to the ontology table because the NWBFile ancestor of this '
                             'GenotypesTable does not exist. Make sure the GenotypesTable is a descendant of the '
                             'NWBFile before adding CRID values to it.')

        # TODO make better API
        for crid in crid_arr:
            term_id = len(nwbfile.ontology_terms)
            nwbfile.ontology_terms.add_row(
                id=term_id,
                key=symbol,
                ontology=crid[0],
                uri=crid[1],
            )
            nwbfile.ontology_objects.add_row(
                id=len(nwbfile.ontology_objects),
                object_id=self.object_id,
                field=field_name,
                item=term_id,
            )

    def get_locus_crid(self, row):
        return self.__get_crid('locus_symbol', self.locus_symbol[row])

    def get_allele1_crid(self, row):
        return self.__get_crid('allele1_symbol', self.allele1_symbol[row])

    def get_allele2_crid(self, row):
        return self.__get_crid('allele2_symbol', self.allele2_symbol[row])

    def get_allele3_crid(self, row):
        return self.__get_crid('allele3_symbol', self.allele3_symbol[row])

    def __get_crid(self, field_name, symbol):
        """Get a CRID from the NWBFile ontology table by symbol.

        Example usage: self.__get_crid('locus_symbol', 'Rorb', ('MGI', 'MGI:1343464'))
        """

        nwbfile = super().get_ancestor(data_type='GenotypeNWBFile')  # TODO changeme
        if nwbfile is None:
            raise ValueError('Cannot add CRID values to the ontology table because the NWBFile ancestor of this '
                             'GenotypesTable does not exist. Make sure the GenotypesTable is a descendant of the '
                             'NWBFile before adding CRID values to it.')

        crid = nwbfile.ontology_objects.get_crid(
            object_id=self.object_id,
            field=field_name,
            key=symbol
        )
        return crid

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
