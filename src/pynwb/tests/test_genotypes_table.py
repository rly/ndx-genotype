import datetime
from dateutil.tz import tzlocal
import pandas as pd
import numpy as np

from hdmf.common import VectorData, ExternalResources

from pynwb import NWBHDF5IO, validate as pynwb_validate
from pynwb.testing import TestCase, remove_test_file
from hdmf.utils import docval, get_docval, getargs, popargs, call_docval_func, AllowPositional

from ndx_genotype import GenotypeNWBFile, GenotypeSubject, GenotypesTable, AllelesTable


class TestAllelesTable(TestCase):

    def test_empty_table(self):
        at = AllelesTable()

        self.assertEqual(at.name, 'alleles_table')
        self.assertEqual(at.description, 'Structured allele information')
        self.assertEqual(at.colnames, ('symbol',))

    def test_add_allele(self):
        at = AllelesTable()
        at.add_allele(symbol='Vipr2-IRES2-Cre')

        self.assertIsInstance(at.symbol, VectorData)
        self.assertEqual(at.symbol.data, ['Vipr2-IRES2-Cre'])

    def test_get_allele_index(self): #Todo: change assert to check for value
        at = AllelesTable()
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        index = at.get_allele_index(symbol='Vipr2-IRES2-Cre')
        self.assertEqual(len(at.symbol.data), 1)

    def set_up_genotypes_table(self, kwargs):
        nwbfile = GenotypeNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        nwbfile.subject = GenotypeSubject(
            subject_id='3',
            genotype='Vip-IRES-Cre/wt',
        )
        gt = GenotypesTable(**kwargs)
        nwbfile.subject.genotypes_table = gt  # GenotypesTable must be descendant of NWBFile before add_genotype works
        # TODO remove this dependency
        return gt

    def test_symbol_external_resource(self):
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'



        gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        nwbfile = at.get_ancestor(data_type='GenotypeNWBFile')
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.symbol_external_resource(container=self,
                                    field='symbol',
                                    key=key,
                                    resource_name=resource_name,
                                    resource_uri=resource_uri,
                                    entity_id=entity_id,
                                    entity_uri=entity_uri
                                    )
        self.assertEqual(nwbfile.external_resources.keys.data, [('key',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'entity_id', 'entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('resource_name',  'resource_uri')])

    def test_generation_method_external_resource(self):
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        nwbfile = at.get_ancestor(data_type='GenotypeNWBFile')
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.generation_method_external_resource(container=self,
                                    field='generation_method',
                                    key=key,
                                    resource_name=resource_name,
                                    resource_uri=resource_uri,
                                    entity_id=entity_id,
                                    entity_uri=entity_uri
                                    )
        self.assertEqual(nwbfile.external_resources.keys.data, [('key',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'entity_id', 'entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('resource_name',  'resource_uri')])

    def test_recombinase_external_resource(self):
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        nwbfile = at.get_ancestor(data_type='GenotypeNWBFile')
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.recombinase_external_resource(container=self,
                                    field='recombinase',
                                    key=key,
                                    resource_name=resource_name,
                                    resource_uri=resource_uri,
                                    entity_id=entity_id,
                                    entity_uri=entity_uri
                                    )
        self.assertEqual(nwbfile.external_resources.keys.data, [('key',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'entity_id', 'entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('resource_name',  'resource_uri')])

    def test_reporter_external_resource(self):
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        nwbfile = at.get_ancestor(data_type='GenotypeNWBFile')
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.reporter_external_resource(container=self,
                                    field='reporter',
                                    key=key,
                                    resource_name=resource_name,
                                    resource_uri=resource_uri,
                                    entity_id=entity_id,
                                    entity_uri=entity_uri
                                    )
        self.assertEqual(nwbfile.external_resources.keys.data, [('key',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'entity_id', 'entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('resource_name',  'resource_uri')])

    def test_promoter_external_resource(self):
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        nwbfile = at.get_ancestor(data_type='GenotypeNWBFile')
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.promoter_external_resource(container=self,
                                    field='promoter',
                                    key=key,
                                    resource_name=resource_name,
                                    resource_uri=resource_uri,
                                    entity_id=entity_id,
                                    entity_uri=entity_uri
                                    )
        self.assertEqual(nwbfile.external_resources.keys.data, [('key',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'entity_id', 'entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('resource_name',  'resource_uri')])

    def test_flanked_sequence_external_resource(self):
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        nwbfile = at.get_ancestor(data_type='GenotypeNWBFile')
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.flanked_sequence_external_resource(container=self,
                                    field='flanked_sequence',
                                    key=key,
                                    resource_name=resource_name,
                                    resource_uri=resource_uri,
                                    entity_id=entity_id,
                                    entity_uri=entity_uri
                                    )
        self.assertEqual(nwbfile.external_resources.keys.data, [('key',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'entity_id', 'entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('resource_name',  'resource_uri')])

    def test_alleles_table_without_genotype_table_external_resources(self):
        #TODO: This test checks the ValueError where if there is no GenotypeTable linked, then we can't add ER.
        container = self
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        at = AllelesTable()
        with self.assertRaises(ValueError):
            at.flanked_sequence_external_resource(container=self,
                                                field='flanked_sequence',
                                                key=key,
                                                resource_name=resource_name,
                                                resource_uri=resource_uri,
                                                entity_id=entity_id,
                                                entity_uri=entity_uri
                                                )
# class TestGenotypesTable(TestCase):
#
#     def test_constructor_basic(self):
#         """Test that the constructor for GenotypesTable sets values as expected."""
#         gt = GenotypesTable(
#             process='PCR',
#             process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
#             assembly='GRCm38.p6',
#             annotation='NCBI Mus musculus Annotation Release 108',
#         )
#         self.assertEqual(gt.name, 'genotypes_table')
#         self.assertEqual(gt.process, 'PCR')
#         self.assertEqual(gt.process_url, 'https://dx.doi.org/10.17504/protocols.io.yjifuke')
#         self.assertEqual(gt.assembly, 'GRCm38.p6')
#         self.assertEqual(gt.annotation, 'NCBI Mus musculus Annotation Release 108')
#         self.assertIsInstance(gt.alleles_table, AllelesTable)
#
    def set_up_genotypes_table(self, kwargs):
        nwbfile = GenotypeNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        nwbfile.subject = GenotypeSubject(
            subject_id='3',
            genotype='Vip-IRES-Cre/wt',
        )
        gt = GenotypesTable(**kwargs)
        nwbfile.subject.genotypes_table = gt  # GenotypesTable must be descendant of NWBFile before add_genotype works
        # TODO remove this dependency
        return gt
#
#     def test_add_minimal_with_allele_index(self):
#         """Test that the constructor for GenotypesTable sets values as expected."""
#         gt = self.set_up_genotypes_table({})
#         allele1_ind = gt.add_allele(symbol='Vip-IRES-Cre')
#         allele2_ind = gt.add_allele(symbol='wt')
#         gt.add_genotype(
#             locus='Vip',
#             allele1=allele1_ind,
#             allele2=allele2_ind,
#         )
#         self.assertEqual(gt[:, 'locus'], ['Vip'])
#         exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre']}, index=pd.Index(name='id', data=[0]))
#         pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)  # TODO requires HDMF #579
#         exp = pd.DataFrame({'symbol': ['wt']}, index=pd.Index(name='id', data=[1]))
#         pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)
#
#     def test_add_minimal_with_allele_symbol(self):
#         """Test that the constructor for GenotypesTable sets values as expected."""
#         gt = self.set_up_genotypes_table({})
#         gt.add_allele(symbol='Vip-IRES-Cre')  # TODO warn if there is no external resource / identifier
#         gt.add_allele(symbol='wt')
#         gt.add_genotype(
#             locus='Vip',  # TODO warn if there is no external resource / identifier
#             allele1='Vip-IRES-Cre',
#             allele2='wt',
#         )
#         self.assertEqual(gt[:, 'locus'], ['Vip'])
#         exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre']}, index=pd.Index(name='id', data=[0]))
#         pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)  # TODO requires HDMF #579
#         exp = pd.DataFrame({'symbol': ['wt']}, index=pd.Index(name='id', data=[1]))
#         pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)

#     def test_add_typical(self):
#         gt = self.set_up_genotypes_table(dict(process='PCR'))
#         gt.add_allele(
#             symbol='Vip-IRES-Cre'
#         )
#         gt.add_allele(symbol='wt')
#         gt.add_allele(symbol='Ai14(RCL-tdT)')
#         gt.add_genotype(
#             locus='Vip',
#             allele1='Vip-IRES-Cre',
#             allele2='wt',
#         )
#         gt.add_genotype(
#             locus='ROSA26',
#             allele1='Ai14(RCL-tdT)',
#             allele2='wt',
#         )
#         self.assertEqual(gt[:, 'locus'], ['Vip', 'ROSA26'])
#         exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre', 'Ai14(RCL-tdT)']}, index=pd.Index(name='id', data=[0, 2]))
#         pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)  # TODO requires HDMF #579
#         exp = pd.DataFrame({'symbol': ['wt', 'wt']}, index=pd.Index(name='id', data=[1, 1]))
#         pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)
#
#         # TODO add external resources
#
#     def test_add_full(self):
#         gt = self.set_up_genotypes_table(dict(
#             process='PCR',
#             process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
#             assembly='GRCm38.p6',
#             annotation='NCBI Mus musculus Annotation Release 108',
#         ))
#         gt.add_allele(symbol='Vip-IRES-Cre')
#         gt.add_allele(symbol='wt')
#         gt.add_allele(symbol='Ai14(RCL-tdT)')
#         gt.add_allele(symbol='allele3')
#         gt.add_genotype(
#             locus='Vip',
#             allele1='Vip-IRES-Cre',
#             allele2='wt',
#             allele3='wt',
#             # NOTE if allele3 is provided for any genotype, then a non-None allele3 value must be provided for all
#             # genotypes...
#         )
#         gt.add_genotype(
#             locus='ROSA26',
#             allele1='Ai14(RCL-tdT)',
#             allele2='wt',
#             allele3='allele3',
#         )
#
#         self.assertEqual(gt[:, 'locus'], ['Vip', 'ROSA26'])
#         exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre', 'Ai14(RCL-tdT)']}, index=pd.Index(name='id', data=[0, 2]))
#         pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)  # TODO requires HDMF #579
#         exp = pd.DataFrame({'symbol': ['wt', 'wt']}, index=pd.Index(name='id', data=[1, 1]))
#         pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)
#         exp = pd.DataFrame({'symbol': ['wt', 'allele3']}, index=pd.Index(name='id', data=[1, 3]))
#         pd.testing.assert_frame_equal(gt[:, 'allele3'], exp)
#
#         # TODO add external resources
#
#
# class TestGenotypesTableRoundtrip(TestCase):
#     """Simple roundtrip test for GenotypesTable."""
#
#     def setUp(self):
#         self.path = 'test.nwb'
#
#     def tearDown(self):
#         remove_test_file(self.path)
#
#     def set_up_genotypes_table(self, kwargs):
#         self.nwbfile = GenotypeNWBFile(
#             session_description='session_description',
#             identifier='identifier',
#             session_start_time=datetime.datetime.now(datetime.timezone.utc)
#         )
#         self.nwbfile.subject = GenotypeSubject(
#             subject_id='3',
#             genotype='Rorb-IRES2-Cre/wt',
#         )
#         gt = GenotypesTable(**kwargs)
#         # GenotypesTable must be descendant of NWBFile before add_genotype works
#         self.nwbfile.subject.genotypes_table = gt
#         return gt
#
#     def roundtrip(self, genotypes_table):
#         """
#         Add a GenotypeTable to an NWBFile, write it to file, read the file, and test that the GenotypeTable from the
#         file matches the original GenotypeTable.
#         """
#         with NWBHDF5IO(self.path, mode='w') as io:
#             io.write(self.nwbfile)
#
#         with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
#             read_nwbfile = io.read()
#             self.assertContainerEqual(genotypes_table, read_nwbfile.subject.genotypes_table)
#             errors = pynwb_validate(io, namespace='ndx-genotype')
#             if errors:
#                 for err in errors:
#                     raise Exception(err)
#
#     def test_roundtrip_minimal(self):
#         # NOTE: writing an empty table is not allowed and raises an error
#         gt = self.set_up_genotypes_table(dict())
#         gt.add_genotype(
#             locus_symbol='Rorb',
#             locus_crid=[('MGI', '1343464')],
#             allele1_symbol='Rorb-IRES2-Cre',
#             allele2_symbol='wt',
#         )
#         self.roundtrip(gt)
#
#     def test_roundtrip_typical(self):
#         gt = self.set_up_genotypes_table(dict(
#             process='PCR',
#         ))
#         gt.add_genotype(
#             locus_symbol='Rorb',
#             locus_crid=[('MGI', '1343464'), ('NCBI Gene', '225998')],
#             allele1_symbol='Rorb-IRES2-Cre',
#             allele1_crid=[('MGI', '5507855')],
#             allele2_symbol='wt',
#         )
#         gt.add_genotype(
#             locus_symbol='locus_symbol',
#             locus_crid=[('MGI', '1')],
#             allele1_symbol='Rorb-allele1_symbol-Cre',
#             allele1_crid=[('MGI', '2'), ('NCBI Gene', '3')],
#             allele2_symbol='allele2_symbol',
#         )
#         self.roundtrip(gt)
#
#     def test_roundtrip_full(self):
#         gt = self.set_up_genotypes_table(dict(
#             process='PCR',
#             process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
#             assembly='GRCm38.p6',
#             annotation='NCBI Mus musculus Annotation Release 108',
#         ))
#         gt.add_genotype(
#             locus_symbol='Rorb2',
#             locus_type='Gene',
#             locus_crid=[('MGI', '1343464'), ('NCBI Gene', '225998')],
#             allele1_symbol='Rorb-IRES2-Cre',
#             allele1_type='Targeted (Recombinase)',
#             allele1_crid=[('MGI', '5507855')],
#             allele2_symbol='wt',
#             allele2_type='Wild Type',
#             allele2_crid=[],
#             allele3_symbol='None',
#             allele3_type='None',
#             allele3_crid=[],
#         )
#         gt.add_genotype(
#             locus_symbol='locus_symbol',
#             locus_type='locus_type',
#             locus_crid=[('MGI', '1')],
#             allele1_symbol='allele1_symbol',
#             allele1_type='allele1_type',
#             allele1_crid=[('MGI', '3')],
#             allele2_symbol='allele2_symbol',
#             allele2_type='allele2_type',
#             allele2_crid=[('MGI', '4'), ('NCBI Gene', '5')],
#             allele3_symbol='allele3_symbol',
#             allele3_type='allele3_type',
#             allele3_crid=[('MGI', '6'), ('NCBI Gene', '7'), ('Ensembl', '8')],
#         )
#         self.roundtrip(gt)
#
#
# class TestGenotypeSubjectConstructor(TestCase):
#
#     def test_constructor(self):
#         """Test that the constructor for GenotypeSubject sets values as expected."""
#         gt = GenotypesTable()
#
#         subject = GenotypeSubject(
#             age='P50D',
#             description='Mouse',
#             genotype='Rorb-IRES2-Cre/wt',
#             genotypes_table=gt,
#             sex='M',
#             species='Mus musculus',
#             subject_id='3',
#             weight='2 lbs',
#             date_of_birth=datetime.datetime(2017, 5, 1, 12, tzinfo=tzlocal())
#         )
#
#         self.assertIs(subject.genotypes_table, gt)
#
#
# class TestGenotypeSubjectRoundtrip(TestCase):
#     """Simple roundtrip test for GenotypeSubject."""
#
#     def setUp(self):
#         self.path = 'test.nwb'
#
#     def tearDown(self):
#         remove_test_file(self.path)
#
#     def test_roundtrip(self):
#         """
#         Add a GenotypeSubject with a GenotypesTable to an NWBFile, write it to file, read the file, and test that the
#         GenotypeSubject from the file matches the original GenotypeSubject.
#         """
#         self.nwbfile = GenotypeNWBFile(
#             session_description='session_description',
#             identifier='identifier',
#             session_start_time=datetime.datetime.now(datetime.timezone.utc)
#         )
#         self.nwbfile.subject = GenotypeSubject(
#             age='P50D',
#             description='Mouse',
#             genotype='Rorb-IRES2-Cre/wt',
#             genotypes_table=GenotypesTable(),
#             sex='M',
#             species='Mus musculus',
#             subject_id='3',
#             weight='2 lbs',
#             date_of_birth=datetime.datetime(2017, 5, 1, 12, tzinfo=tzlocal())
#         )
#         self.nwbfile.subject.genotypes_table.add_genotype(
#             locus_symbol='Rorb',
#             locus_crid=[('MGI', '1343464')],
#             allele1_symbol='Rorb-IRES2-Cre',
#             allele2_symbol='wt',
#         )
#
#         with NWBHDF5IO(self.path, mode='w') as io:
#             io.write(self.nwbfile)
#
#         with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
#             read_nwbfile = io.read()
#             self.assertContainerEqual(self.nwbfile.subject, read_nwbfile.subject)
#             errors = pynwb_validate(io, namespace='ndx-genotype')
#             if errors:
#                 for err in errors:
#                     raise Exception(err)
