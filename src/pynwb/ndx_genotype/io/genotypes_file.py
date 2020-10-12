from pynwb import register_map
from pynwb.file import NWBFile
from pynwb.io import NWBFileMap


@register_map(NWBFile)
class NWBFileMap(NWBFileMap):

    def __init__(self, spec):
        super().__init__(spec)

        ontologies_group_spec = self.spec.get_group('.ontologies')

        # unmap auto-attribute '.ontologies' from NWBFile class
        self.unmap(ontologies_group_spec)

        # map attribute 'ontology_objects' on NWBFile class to dataset spec NWBFile/.ontologies/objects
        # map attribute 'ontology_terms' on NWBFile class to dataset spec NWBFile/.ontologies/terms
        self.map_spec('ontology_objects', ontologies_group_spec.get_dataset('objects'))
        self.map_spec('ontology_terms', ontologies_group_spec.get_dataset('terms'))
