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
        version="""0.1.0""",
        author=list(map(str.strip, """Ryan Ly, Oliver Ruebel, Pam Baker, Lydia Ng""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('NWBFile', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('Data', namespace='core')
    ns_builder.include_type('Container', namespace='core')

    crid_vectordata_spec = NWBDatasetSpec(
        neurodata_type_def='CRIDVectorData',
        neurodata_type_inc='VectorData',
        doc='A table column to hold Central Registry ID (CRID) values.',
        dtype=[
            NWBDtypeSpec(
                name='registry',
                doc='Name of the registry. Should be either "MGI", "NCBI", or "Ensembl"',
                dtype='text',
            ),
            NWBDtypeSpec(
                name='symbol',
                doc='Symbol (key) of the locus in the registry.',
                dtype='text',
            )
        ],
        shape=[None],
    )

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
                name='locus_symbol',
                neurodata_type_inc='VectorData',
                doc='Symbol/name of the locus, e.g., Rorb.',
                dtype='text',
            ),
            NWBDatasetSpec(
                name='locus_type',
                neurodata_type_inc='VectorData',
                doc='Type of the locus, e.g., Gene, Transgene, Unclassified other.',
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='locus_crid',
                neurodata_type_inc='CRIDVectorData',
                doc=('Central Registry ID (CRID) of the locus, e.g., MGI 1343464 => registry: MGI, symbol: 1343464. '
                     'Multiple CRIDs can be associated with each locus. At least one must be provided.'),
            ),
            NWBDatasetSpec(
                name='locus_crid_index',
                neurodata_type_inc='VectorIndex',
                doc='Index for the locus_crid dataset',
            ),
            NWBDatasetSpec(
                name='allele1_symbol',
                neurodata_type_inc='VectorData',
                doc=('Symbol/name of the first allele, e.g., Rorb-IRES2-Cre. '
                     '"wt" should be used to represent wild-type.'),
                dtype='text',
            ),
            NWBDatasetSpec(
                name='allele1_type',
                neurodata_type_inc='VectorData',
                doc=('Type of the first allele, e.g., Targeted (Recombinase), '
                     'Transgenic (Null/knockout, Transactivator), Targeted (Conditional ready, Inducible, Reporter).'
                     '"Wild Type" should be used to represent wild-type. Allele types can be found at: '
                     'http://www.informatics.jax.org/userhelp/ALLELE_phenotypic_categories_help.shtml#method'),
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele1_crid',
                neurodata_type_inc='CRIDVectorData',
                doc=('Central Registry ID (CRID) of the first allele, e.g., MGI 1343464 => registry: MGI, '
                     'symbol: 1343464. Multiple CRIDs can be associated with each allele.'),
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele1_crid_index',
                neurodata_type_inc='VectorIndex',
                doc='Index for the allele1_crid dataset',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele2_symbol',
                neurodata_type_inc='VectorData',
                doc=('Smybol/name of the second allele, e.g., Rorb-IRES2-Cre. '
                     '"wt" should be used to represent wild-type.'),
                dtype='text',
            ),
            NWBDatasetSpec(
                name='allele2_type',
                neurodata_type_inc='VectorData',
                doc=('Type of the second allele, e.g., Targeted (Recombinase), '
                     'Transgenic (Null/knockout, Transactivator), Targeted (Conditional ready, Inducible, Reporter).'
                     '"Wild Type" should be used to represent wild-type. Allele types can be found at: '
                     'http://www.informatics.jax.org/userhelp/ALLELE_phenotypic_categories_help.shtml#method'),
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele2_crid',
                neurodata_type_inc='CRIDVectorData',
                doc=('Central Registry ID (CRID) of the second allele, e.g., MGI 1343464 => registry: MGI, '
                     'symbol: 1343464. Multiple CRIDs can be associated with each allele.'),
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele2_crid_index',
                neurodata_type_inc='VectorIndex',
                doc='Index for the allele2_crid dataset',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele3_symbol',
                neurodata_type_inc='VectorData',
                doc=('Symbol/name of the third allele, e.g., Rorb-IRES2-Cre. '
                     '"wt" should be used to represent wild-type.'),
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele3_type',
                neurodata_type_inc='VectorData',
                doc=('Type of the third allele, e.g., Targeted (Recombinase), '
                     'Transgenic (Null/knockout, Transactivator), Targeted (Conditional ready, Inducible, Reporter).'
                     '"Wild Type" should be used to represent wild-type. Allele types can be found at: '
                     'http://www.informatics.jax.org/userhelp/ALLELE_phenotypic_categories_help.shtml#method'),
                dtype='text',
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele3_crid',
                neurodata_type_inc='CRIDVectorData',
                doc=('Central Registry ID (CRID) of the third allele, e.g., MGI 1343464 => registry: MGI, '
                     'symbol: 1343464. Multiple CRIDs can be associated with each allele.'),
                quantity='?',
            ),
            NWBDatasetSpec(
                name='allele3_crid_index',
                neurodata_type_inc='VectorIndex',
                doc='Index for the allele3_crid dataset',
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
        groups=[NWBGroupSpec(
            name='genotypes_table',
            neurodata_type_inc='GenotypeTable',
            doc='Structured genotype information for the subject.',
            quantity='?',
        )],
    )

    genotype_nwbfile_spec = NWBGroupSpec(
        neurodata_type_def='GenotypeNWBFile',
        neurodata_type_inc='NWBFile',
        doc=('Extension of the NWBFile class to allow placing the new GenotypeSubject type '
             'in /general/subject in the NWBFile. NOTE: If this proposal for extension '
             'to NWB gets merged with the core schema, then this type would be removed and the '
             'NWBFile specification updated instead.'),
        groups=[NWBGroupSpec(
            name='general',  # override existing general group
            doc='Expanded definition of general from NWBFile.',
            groups=[NWBGroupSpec(
                name='subject',  # override existing subject type
                neurodata_type_inc='GenotypeSubject',
                doc='Subject information with structured genotype information.',
                quantity='?',
            )],
        )],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [crid_vectordata_spec, genotypes_table_spec, genotype_subject_spec, genotype_nwbfile_spec]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
