import os
from pynwb import load_namespaces


# Set path of the namespace.yaml file to the expected install location
ndx_genotype_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-genotype.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_genotype_specpath):
    ndx_genotype_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-genotype.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_genotype_specpath)

from .genotypes_table import GenotypesTable, AllelesTable  # noqa: F401,E402
from .genotype_subject import GenotypeSubject  # noqa: F401,E402
