import numpy as np
import warnings

from pynwb import register_class
from pynwb.core import DynamicTable, DynamicTableRegion
from hdmf.utils import docval, get_docval, getargs, popargs, call_docval_func, AllowPositional
from hdmf.common import ExternalResources
from hdmf.common.resources import Key


@register_class('AllelesTable', 'ndx-genotype')
class AllelesTable(DynamicTable):
    """A table to hold structured allele information."""

    __columns__ = (
        {'name': 'symbol',
         'description': 'Symbol/name of the allele.',
         'required': True},
        {'name': 'recombinase',
         'description': ('An enzyme that mediates a recombination exchange'
                         'reaction between two DNA templates, each containing a specific recognition site.'),
         'required': False,
         'index': True},
        {'name': 'reporter',
         'description': ('Sequence that forms all or part of the protein product encoded by a'
                         'transgenic locus or modified endogenous locus and that encodes an enzyme'
                         'whose activity can be used to detect the presence of that protein product.'),
         'required': False,
         'index': True},
        {'name': 'promoter',
         'description': ('A DNA sequence at which RNA polymerase binds and initiates transcription.'),
         'required': False,
         'index': True},
        {'name': 'recombinase_recognition_site',
         'description': ('Site where recombination occurs mediated by a specific recombinase, leading to'
                         'integration, deletion or inversion of a DNA fragment.'),
         'required': False,
         'index': True}
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
            {'name': 'symbol',
            'type': str,
            'doc': ('Symbol/name of the allele, e.g., Rorb-IRES-Cre. This must be unique in the table.')},
            {'name': 'recombinase',
            'type': str,
            'doc': ('An enzyme that mediates a recombination exchange'
                    'reaction between two DNA templates, each containing a specific recognition site.'),
            'default': None},
            {'name': 'reporter',
            'type': str,
            'doc': ('Sequence that forms all or part of the protein product encoded by a'
                    'transgenic locus or modified endogenous locus and that encodes an enzyme'
                    'whose activity can be used to detect the presence of that protein product.'),
            'default': None},
            {'name': 'promoter',
            'type': str,
            'doc': ('A DNA sequence at which RNA polymerase binds and initiates transcription.'),
            'default': None},
            {'name': 'recombinase_recognition_site',
            'type': str,
            'doc': ('Site where recombination occurs mediated by a specific recombinase, leading to'
                    'integration, deletion or inversion of a DNA fragment.'),
            'default': None},
            allow_extra=True,
            allow_positional=AllowPositional.ERROR)
    def add_allele(self, **kwargs):
        """Add an allele to this table. Return the row index of the new allele."""
        symbol = getargs('symbol', kwargs)
        if symbol in self.symbol:
            raise ValueError("Allele symbol '%s' already exists in AllelesTable." % symbol)
        # get the index of the new allele in the table, which will be the ID if passed, or the table length if
        # auto-incremented
        ind = len(self)
        super().add_row(**kwargs)
        return ind

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
            warnings.warn("Multiple rows in alleles table contain symbol '%s'. Using the first match." % symbol)
        return index[0]

    @docval({'name': 'field', 'type': str, 'default': None,
             'doc': ('the column in the AllelesTable for the external resource'
                     'i.e symbol, recombinase, reporter, promoter, or recombinase_recognition_site')},
            {'name': 'key', 'type': (str, Key), 'default': None,
             'doc': 'the name of the entity'},
            {'name': 'resource_name', 'type': str, 'doc': 'the name of the resource to be created', 'default': None},
            {'name': 'resource_uri', 'type': str, 'doc': 'the uri of the resource to be created', 'default': None},
            {'name': 'entity_id', 'type': str, 'doc': 'the identifier for the entity at the resource', 'default': None},
            {'name': 'entity_uri', 'type': str, 'doc': 'the URI for the identifier at the resource', 'default': None})
    def add_external_resource(self, **kwargs):
        field = kwargs['field']
        key = kwargs['key']
        resource_name = kwargs['resource_name']
        resource_uri = kwargs['resource_uri']
        entity_id = kwargs['entity_id']
        entity_uri = kwargs['entity_uri']

        # assert that field is a column of the alleles table  # TODO test this
        # if field not in self.colnames:
        #     msg = "%s is not a column of AllelesTable" % field
        #     raise ValueError(msg)

        nwbfile = self.get_ancestor(data_type='GenotypeNWBFile')  # TODO change me to NWBFile after merge with NWB core
        if nwbfile is None:
            msg = "AllelesTable must have a GenotypeNWBFile as an ancestor to associate with ExternalResources"
            raise ValueError(msg)

        er = nwbfile.external_resources.add_ref(
            container=self,
            field=field,
            key=key,
            resource_name=resource_name,
            resource_uri=resource_uri,
            entity_id=entity_id,
            entity_uri=entity_uri
        )
        return er

# NOTE: cannot write an empty genotypes table

@register_class('GenotypesTable', 'ndx-genotype')
class GenotypesTable(DynamicTable):
    """A table to hold structured genotype information."""

    __fields__ = (
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
         'description': '...',  # TODO fill in descriptions
         'table': True,
         'required': True},
        {'name': 'allele2',
         'description': '...',
         'table': True,
         'required': True},
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
            'type': AllelesTable,
            'doc': 'The table of alleles for a genotype. If not provided, an AllelesTable will be created.',
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
        if self['allele1'].table is None:
            self['allele1'].table = self.alleles_table
        if self['allele2'].table is None:
            self['allele2'].table = self.alleles_table
        if self.allele3 is not None and self['allele3'].table is None:
            self['allele3'].table = self.alleles_table

    @docval(
        {
            'name': 'locus',
            'type': str,
            'doc': 'Symbol/name of the locus, e.g., Rorb.',
        },
        {
            'name': 'allele1',
            'type': (int, str),
            'doc': ('The index of the first allele in the alleles table, or the symbol of the first allele. Providing '
                    'the index is more efficient than providing the symbol, which requires a search through the '
                    'alleles table.'),
        },
        {
            'name': 'allele2',
            'type': (int, str),
            'doc': ('The index of the second allele in the alleles table, or the symbol of the second allele. Providing '
                    'the index is more efficient than providing the symbol, which requires a search through the '
                    'alleles table.'),
        },
        {
            'name': 'allele3',
            'type': (int, str),
            'doc': ('The index of the third allele in the alleles table, or the symbol of the third allele. Providing '
                    'the index is more efficient than providing the symbol, which requires a search through the '
                    'alleles table.'),
            'default': None,
        },
        {
            'name': 'locus_resource_name',
            'type': str,
            'doc': 'The name of the locus external resource used for reference',
            'default': None,
        },
        {
            'name': 'locus_resource_uri',
            'type': str,
            'doc': 'The URI of the locus external resource',
            'default': None,
        },
        {
            'name': 'locus_entity_id',
            'type': str,
            'doc': 'The unique ID from the external resource for the locus',
            'default': None,
        },
        {
            'name': 'locus_entity_uri',
            'type': str,
            'doc': 'The URI for the locus entity',
            'default': None,
        },
        allow_extra=True,
        allow_positional=AllowPositional.ERROR,
    )
    def add_genotype(self, **kwargs):
        """Add a genotype to this table."""

        locus = getargs('locus', kwargs)
        # if the allele symbol is passed in, get the index of the allele and use that in add_row
        allele1 = getargs('allele1', kwargs)
        if isinstance(allele1, str):
            allele1_ind = self.get_allele_index(allele1)
            if allele1_ind is None:
                raise ValueError("'allele1' symbol '%s' not found in alleles table. Please first add the allele "
                                 "using GenotypeTable.add_allele()." % allele1)
            kwargs['allele1'] = allele1_ind
        allele2 = getargs('allele2', kwargs)
        if isinstance(allele2, str):
            allele2_ind = self.get_allele_index(allele2)
            if allele2_ind is None:
                raise ValueError("'allele2' symbol '%s' not found in alleles table. Please first add the allele "
                                 "using GenotypeTable.add_allele()." % allele1)
            kwargs['allele2'] = allele2_ind
        allele3 = getargs('allele3', kwargs)
        if allele3 is not None and isinstance(allele3, str):
            allele3_ind = self.get_allele_index(allele3)
            if allele3_ind is None:
                raise ValueError("'allele3' symbol '%s' not found in alleles table. Please first add the allele "
                                 "using GenotypeTable.add_allele()." % allele1)
            kwargs['allele3'] = allele3_ind

        locus_resource_name = popargs('locus_resource_name', kwargs)
        locus_resource_uri = popargs('locus_resource_uri', kwargs)
        locus_entity_id = popargs('locus_entity_id', kwargs)
        locus_entity_uri = popargs('locus_entity_uri', kwargs)
        super().add_row(**kwargs)

        if self.allele3 is not None and self['allele3'].table is None:
            self['allele3'].table = self.alleles_table

        nwbfile = self.get_ancestor(data_type='GenotypeNWBFile')  # TODO changeme to NWBFile after migration

        # TODO warn if no external resource information is provided
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
        else:
            warnings.warn("User did not provide ExternalResources parameters. No external resource was created.")

    @docval(*get_docval(AllelesTable.add_allele))
    def add_allele(self, **kwargs):
        return self.alleles_table.add_allele(**kwargs)
        # return call_docval_func(self.alleles_table.add_allele, kwargs)

    @docval(*get_docval(AllelesTable.get_allele_index))
    def get_allele_index(self, **kwargs):
        return call_docval_func(self.alleles_table.get_allele_index, kwargs)
