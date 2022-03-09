from pynwb import register_class
from pynwb.file import Subject
from hdmf.utils import docval, get_docval, call_docval_func, popargs

from .genotypes_table import GenotypesTable


@register_class('GenotypeSubject', 'ndx-genotype')
class GenotypeSubject(Subject):

    __nwbfields__ = (
        {'name': 'genotypes_table', 'child': True, 'required_name': 'genotypes_table'},
    )

    @docval(
        *get_docval(Subject.__init__),
        {
            'name': 'genotypes_table',
            'type': 'GenotypesTable',
            'doc': 'Table of genotypes.',
            'default': None,
        },
    )
    def __init__(self, **kwargs):
        genotypes_table = popargs('genotypes_table', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.genotypes_table = genotypes_table

    def add_genotype(self, **kwargs):
        if self.genotypes_table is None:
            self.genotypes_table = GenotypesTable()
        self.genotypes_table.add_row(**kwargs)
