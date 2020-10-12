from pynwb import register_class
from pynwb.file import Subject, NWBFile
from hdmf.utils import docval, get_docval, call_docval_func, popargs

from .genotypes_table import GenotypesTable


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
