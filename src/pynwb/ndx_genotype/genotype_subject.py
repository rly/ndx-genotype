from pynwb import register_class
from pynwb.file import Subject
from hdmf import Ontology
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

    @docval({'name': 'attribute', 'type': str,
             'doc': 'The attribute of the Subject for the external reference.', 'default': None},
            {'name': 'key', 'type': str,
             'doc': 'The name of the key or the Key object from the KeyTable for the key to add a resource for.'},
            {'name': 'ontology', 'type': Ontology,
             'doc': 'The ontology to be used as the external resource'})
    def add_ontology_browser(self, **kwargs):
        attribute =  kwargs['attribute']
        key = kwargs['key']
        ontology = kwargs['ontology']

        ontology_name = ontology.ontology_name
        ontology_uri = ontology.ontology_uri

        # Retrieve entity_id and entity_uri
        entity_id, entity_uri = ontology.get_entity_browser(key=key)

        container = self.get_ancestor_container(data_type='ExternalResources')  # check container for external_resources.
        if container is None:
            msg = "Cannot find Container with ExternalResources"
            raise ValueError(msg)

        er = container.external_resources.add_ref(
            container=self,
            attribute=attribute,
            key=key,
            resource_name=ontology_name,
            resource_uri=ontology_uri,
            entity_id=entity_id,
            entity_uri=entity_uri
        )
        return er
