# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec


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

    ns_builder.include_namespace('core')
    ns_builder.include_type('ExternalResources', namespace='hdmf-experimental')  # TODO migrate to core

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
             'NOTE: If this proposal for extension to NWB gets merged with the core schema, then this type would be '
             'removed and the Subject specification updated instead.'),
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
             'in /general/subject in the NWBFile and 2) placing the new external resources group. '
             'NOTE: If this proposal for extension to NWB gets merged with the core schema, then this type would be '
             'removed and the NWBFile specification updated instead.'),
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
                name='.external_resources',
                neurodata_type_inc='ExternalResources',
                doc='External resources used in this file.',
            ),
        ],
    )

    new_data_types = [genotypes_table_spec, alleles_table_spec, genotype_subject_spec, genotype_nwbfile_spec]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
