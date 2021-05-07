from pynwb import register_map
from pynwb.file import NWBFile
from pynwb.io.file import NWBFileMap


@register_map(NWBFile)
class NWBFileMap(NWBFileMap):

    def __init__(self, spec):
        super().__init__(spec)
        self.map_spec('external_resources', self.spec.get_group('.external_resources'))
