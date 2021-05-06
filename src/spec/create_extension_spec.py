# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBDtypeSpec
# TODO: import the following spec classes as needed
# from pynwb.spec import , NWBLinkSpec, , NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An NWB extension to describe the detailed genotype of an experimental subject""",
        name="""ndx-genotype""",
        version="""0.2.0""",
        author=list(map(str.strip, """Ryan Ly, Oliver Ruebel, Pam Baker, Lydia Ng, Matthew Avaylon""".split(','))),
        contact=list(map(str.strip, ("""rly@lbl.gov, oruebel@lbl.gov, pamela.baker@alleninstitute.org, """
                                     """LydiaN@alleninstitute.org, mavaylon@lbl.gov""").split(',')))
    )

    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('NWBFile', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('DynamicTableRegion', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('Data', namespace='core')

    genotypes_table_spec = NWBGroupSpec(
        neurodata_type_def='GenotypesTable',
        neurodata_type_inc='DynamicTable',
        doc='A table to hold structured genotype information.',
        attributes=[
            NWBAttributeSpec(
                name='process',
                doc='Description of the process or assay used to determine the genotype, e.g., PCR.',
                dtype='text',
                required=False,
            ),
            NWBAttributeSpec(
                name='process_url',
                doc=('URL to online document that provides further details of the protocol used, e.g., '
                     'https://dx.doi.org/10.17504/protocols.io.yjifuke'),
                dtype='text',
                required=False,
            ),
            NWBAttributeSpec(
                name='assembly',
                doc='Description of the assembly of the reference genome, e.g., GRCm38.p6.',
                dtype='text',
                required=False,
            ),
            NWBAttributeSpec(
                name='annotation',
                doc=('Description of the annotation of the reference genome, '
                     'e.g., NCBI Mus musculus Annotation Release 108.'),
                dtype='text',
                required=False,
            ),
        ],
        datasets=[
            NWBDatasetSpec(
                name='locus',
                neurodata_type_inc='VectorData',
                doc='Symbol/name of the locus, e.g., Rorb.',
                dtype='text',
            ),
            NWBDatasetSpec(
                name='allele1',
                neurodata_type_inc='DynamicTableRegion',
                doc=('...'),
            ),
            NWBDatasetSpec(
                name='allele2',
                neurodata_type_inc='DynamicTableRegion',
                doc=('...'),
            ),
            NWBDatasetSpec(
                name='allele3',
                neurodata_type_inc='DynamicTableRegion',
                doc=('...'),
            ),
        ],
        groups=[
            NWBGroupSpec(
                name='alleles_table',
                neurodata_type_inc='AllelesTable',
                doc='Structured allele information for the subject.',
            )
        ],
    )

    alleles_table_spec = NWBGroupSpec(
        neurodata_type_def='AllelesTable',
        neurodata_type_inc='DynamicTable',
        doc='A table to hold structured allele information.',
        datasets=[
            NWBDatasetSpec(
                name='symbol',
                neurodata_type_inc='VectorData',
                doc='Symbol/name of the allele',
                dtype='text',
            ),
            NWBDatasetSpec(
                name='generation_method',
                neurodata_type_inc='VectorData',
                doc='...',
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='recombinase',
                neurodata_type_inc='VectorData',
                doc='...',
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='reporter',
                neurodata_type_inc='VectorData',
                doc='...',
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='promoter',
                neurodata_type_inc='VectorData',
                doc='...',
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='flanked_sequence',
                neurodata_type_inc='VectorData',
                doc='...',
                dtype='text',
                quantity='?',
            ),
        ],
    )

    genotype_subject_spec = NWBGroupSpec(
        neurodata_type_def='GenotypeSubject',
        neurodata_type_inc='Subject',
        doc=('An enhanced Subject type that has an additional field for a genotype table. '
             'NOTE: If this proposal for extension '
             'to NWB gets merged with the core schema, then this type would be removed and the'
             'Subject specification updated instead.'),
        groups=[
            NWBGroupSpec(
                name='genotypes_table',
                neurodata_type_inc='GenotypesTable',
                doc='Structured genotype information for the subject.',
                quantity='?',
            ),
        ],
    )

    genotype_nwbfile_spec = NWBGroupSpec(
        neurodata_type_def='GenotypeNWBFile',
        neurodata_type_inc='NWBFile',
        doc=('Extension of the NWBFile class to allow 1) placing the new GenotypeSubject type '
             'in /general/subject in the NWBFile and 2) placing the new ontologies group containing an '
             'ontology table and ontology map. NOTE: If this proposal for extension '
             'to NWB gets merged with the core schema, then this type would be removed and the '
             'NWBFile specification updated instead. The ontologies types will be incorporated from HDMF '
             'when they are finalized.'),
        groups=[
            NWBGroupSpec(
                name='general',  # override existing general group
                doc='Expanded definition of general from NWBFile.',
                groups=[
                    NWBGroupSpec(
                        name='subject',  # override existing subject type
                        neurodata_type_inc='GenotypeSubject',
                        doc='Subject information with structured genotype information.',
                        quantity='?',
                    ),
                ],
            ),
            NWBGroupSpec(
                name='.ontologies',
                doc='Information about ontological terms used in this file.',
                quantity='?',
                datasets=[
                    NWBDatasetSpec(
                        name='objects',
                        neurodata_type_inc='OntologyTable',
                        doc='The objects that conform to an ontology.',
                    ),
                    NWBDatasetSpec(
                        name='terms',
                        neurodata_type_inc='OntologyMap',
                        doc='The ontological terms that get used in this file.',
                    ),
                ],
            ),
        ],
    )

    ontology_table_spec = NWBDatasetSpec(
        neurodata_type_def='OntologyTable',
        neurodata_type_inc='Data',
        doc=('A table for identifying which objects in a file contain values that correspond to ontology terms or '
             'centrally registered IDs (CRIDs)'),
        dtype=[
            NWBDtypeSpec(
                name='id',
                dtype='uint64',
                doc='The unique identifier in this table.'
            ),
            NWBDtypeSpec(
                name='object_id',
                dtype='text',
                doc='The UUID for the object that uses this ontology term.'
            ),
            NWBDtypeSpec(
                name='field',
                dtype='text',
                doc='The field from the object (specified by object_id) that uses this ontological term.'
            ),
            NWBDtypeSpec(
                name='item',
                dtype='uint64',
                doc='An index into the OntologyMap that contains the term.'
            ),
        ],
        shape=[None],
    )

    ontology_map_spec = NWBDatasetSpec(
        neurodata_type_def='OntologyMap',
        neurodata_type_inc='Data',
        doc=('A table for mapping user terms (i.e., keys) to ontology terms / registry symbols / '
             'centrally registered IDs (CRIDs)'),
        dtype=[
            NWBDtypeSpec(
                name='id',
                dtype='uint64',
                doc='The unique identifier in this table.'
            ),
            NWBDtypeSpec(
                name='key',
                dtype='text',
                doc='The user key that maps to the ontology term / registry symbol.'
            ),
            NWBDtypeSpec(
                name='ontology',
                dtype='text',
                doc='The ontology/registry that the term/symbol comes from.'
            ),
            NWBDtypeSpec(
                name='uri',
                dtype='text',
                doc='The unique resource identifier for the ontology term / registry symbol.'
            ),
        ],
        shape=[None],
    )

    new_data_types = [genotypes_table_spec, alleles_table_spec, genotype_subject_spec, genotype_nwbfile_spec,
                      ontology_table_spec, ontology_map_spec]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
