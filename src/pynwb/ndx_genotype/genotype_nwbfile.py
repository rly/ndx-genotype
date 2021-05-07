from pynwb import register_class
from pynwb.file import Subject, NWBFile
from hdmf.utils import docval, get_docval, call_docval_func, popargs
from hdmf.common import ExternalResources  # TODO import this from pynwb after ExternalResources is aliased in PyNWB

from .genotypes_table import GenotypesTable


def _get_nwbfile_init_docval_except_subject():
    dv = get_docval(NWBFile.__init__)
    return filter(lambda x: x['name'] != 'subject', dv)


@register_class('GenotypeNWBFile', 'ndx-genotype')
class GenotypeNWBFile(NWBFile):

    __nwbfields__ = (
        {'name': 'external_resources', 'child': True, 'required_name': '.external_resources'},
    )

    @docval(*_get_nwbfile_init_docval_except_subject(),
            {'name': 'subject',
             'type': 'GenotypeSubject',
             'doc': 'An enhanced Subject type that has an additional field for a genotype table.',
             'default': None},
            {'name': 'external_resources',
             'type': 'ExternalResources',
             'doc': 'The external resources that objects in the file are related to',
             'default': None},)
    def __init__(self, **kwargs):
        subject = popargs('subject', kwargs)
        external_resources = popargs('external_resources', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.subject = subject
        if external_resources is not None:
            self.external_resources = external_resources
        else:
            self.external_resources = ExternalResources('.external_resources')


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
