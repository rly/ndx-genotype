import numpy as np
import warnings

from pynwb import register_class
from pynwb.core import DynamicTable, DynamicTableRegion
from hdmf.utils import docval, get_docval, getargs, popargs, call_docval_func, AllowPositional


@register_class('AllelesTable', 'ndx-genotype')
class AllelesTable(DynamicTable):
    """A table to hold structured allele information."""

    __columns__ = (
        {'name': 'symbol',
         'description': 'Symbol/name of the allele.',
         'required': True},
    )

    @docval(
        {
            'name': 'name',
            'type': str,
            'doc': 'Name of this AllelesTable object.',
            'default': 'alleles_table',
        },
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A description of what is in this table.',
            'default': 'Structured allele information',
        },
    )
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)

    @docval(
        {
            'name': 'symbol',
            'type': str,
            'doc': 'Symbol/name of the allele, e.g., Rorb-IRES-Cre.',
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_allele(self, **kwargs):
        """Add an allele to this table."""
        symbol = getargs('symbol', kwargs)
        if symbol in self.symbol:
            raise ValueError("Allele symbol '%s' already exists in AllelesTable." % symbol)
        super().add_row(**kwargs)

    @docval(
        {
            'name': 'symbol',
            'type': str,
            'doc': 'The symbol to search for.',
        },
    )
    def get_allele_index(self, **kwargs):
        """Return the index of the allele with the given symbol from the alleles table, or None if not found."""
        symbol = getargs('symbol', kwargs)
        index = np.where(np.array(self.symbol.data) == symbol)[0]
        if len(index) == 0:
            return None
        elif len(index) > 1:
            warnings.warn("Multiple rows in alleles table contain symbol '%s'" % symbol)
        return index[0]


# NOTE: cannot write an empty genotypes table

@register_class('GenotypesTable', 'ndx-genotype')
class GenotypesTable(DynamicTable):
    """A table to hold structured genotype information."""

    __nwbfields__ = (
        'process',
        'process_url',
        'assembly',
        'annotation',
        {'name': 'alleles_table', 'child': True, 'required_name': 'alleles_table'},
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

    @docval(
        {
            'name': 'name',
            'type': str,
            'doc': 'Name of this GenotypesTable object.',
            'default': 'genotypes_table',
        },
        *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
        {
            'name': 'description',
            'type': str,
            'doc': 'A description of what is in this table.',
            'default': 'Structured genotype information',
        },
        {
            'name': 'process',
            'type': str,
            'doc': 'Description of the process or assay used to determine the genotype, e.g., PCR.',
            'default': None,
        },
        {
            'name': 'process_url',
            'type': str,
            'doc': 'URL to online document that provides further details of the protocol used.',
            'default': None,
        },
        {
            'name': 'assembly',
            'type': str,
            'doc': 'Description of the assembly of the reference genome, e.g., GRCm38.p6.',
            'default': None,
        },
        {
            'name': 'annotation',
            'type': str,
            'doc': ('Description of the annotation of the reference genome, '
                    'e.g., NCBI Mus musculus Annotation Release 108.'),
            'default': None,
        },
        {
            'name': 'alleles_table',
            'type': str,
            'doc': ('Description of the annotation of the reference genome, '
                    'e.g., NCBI Mus musculus Annotation Release 108.'),
            'default': None,
        },
        allow_positional=AllowPositional.ERROR,
    )
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)
        self.process = getargs('process', kwargs)
        self.process_url = getargs('process_url', kwargs)
        self.assembly = getargs('assembly', kwargs)
        self.annotation = getargs('annotation', kwargs)
        self.alleles_table = getargs('alleles_table', kwargs)
        if self.alleles_table is None:
            self.alleles_table = AllelesTable()

    @docval(
        {
            'name': 'locus',
            'type': str,
            'doc': 'Symbol/name of the locus, e.g., Rorb.',
        },
        {
            'name': 'allele1',
            'type': 'scalar_data',
            'doc': ('...'),
        },
        {
            'name': 'allele2',
            'type': 'scalar_data',
            'doc': ('...'),
        },
        {
            'name': 'allele3',
            'type': 'scalar_data',
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
        allow_positional=AllowPositional.ERROR,
    )
    def add_genotype(self, **kwargs):
        """Add a genotype to this table."""

        # TODO check allele1 is an int
        locus_resource_name = popargs('locus_resource_name', kwargs)
        locus_resource_uri = popargs('locus_resource_uri', kwargs)
        locus_entity_id = popargs('locus_entity_id', kwargs)
        locus_entity_uri = popargs('locus_entity_uri', kwargs)
        super().add_row(**kwargs)

        if self['allele1'].table is None:
            self['allele1'].table = self.alleles_table
        if self['allele2'].table is None:
            self['allele2'].table = self.alleles_table
        if 'allele3' in self and self['allele3'].table is None:
            self['allele3'].table = self.alleles_table

        locus = getargs('locus', kwargs)

        nwbfile = self.get_ancestor(data_type='GenotypeNWBFile')  # TODO changeme to NWBFile after migration
        if (locus_resource_name is not None and locus_resource_uri is not None and locus_entity_id is not None and
                locus_entity_uri is not None):
            nwbfile.external_resources.add_ref(
                container=self,
                field='locus',
                key=locus,
                resource_name=locus_resource_name,
                resource_uri=locus_resource_uri,
                entity_id=locus_entity_id,
                entity_uri=locus_entity_uri,
            )

    # TODO docval
    def add_allele(self, **kwargs):
        allele_ind = len(self.alleles_table)
        self.alleles_table.add_row(**kwargs)
        region = self.alleles_table.create_region(
            name='TODO',
            region=[allele_ind],
            description='reference to allele ' + kwargs.get('symbol'),
        )
        return region

    @docval(*get_docval(AllelesTable.get_allele_index))
    def get_allele_index(self, **kwargs):
        return call_docval_func(self.alleles_table.get_allele_index, kwargs)
