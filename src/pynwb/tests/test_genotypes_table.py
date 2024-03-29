import datetime
from dateutil.tz import tzlocal
import pandas as pd
import numpy as np
from hdmf.common import VectorData
from pynwb import NWBHDF5IO, validate as pynwb_validate
from pynwb.testing import TestCase, remove_test_file
from ndx_external_resources import ERNWBFile

from ndx_genotype import GenotypeSubject, GenotypesTable, AllelesTable


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

    def test_get_allele_index(self):
        at = AllelesTable()
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        index = at.get_allele_index(symbol='Vipr2-IRES2-Cre')
        index_value = np.where(np.array(at.symbol.data) == 'Vipr2-IRES2-Cre')[0]
        self.assertEqual(index, index_value)

    def set_up_genotypes_table(self, kwargs):
        nwbfile = ERNWBFile(
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
        return nwbfile, gt

    def test_add_external_resource(self):
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        nwbfile, gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        at.add_external_resource(
                                    column='symbol',
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
        # This test checks the ValueError where if there is no GenotypeTable linked, then we can't add ER.
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        at = AllelesTable()
        with self.assertRaises(ValueError):
            at.add_external_resource(
                column='flanked_sequence',
                key=key,
                resource_name=resource_name,
                resource_uri=resource_uri,
                entity_id=entity_id,
                entity_uri=entity_uri
            )

    def test_check_field(self):
        key = 'key'
        resource_name = 'resource_name'
        resource_uri = 'resource_uri'
        entity_id = 'entity_id'
        entity_uri = 'entity_uri'

        _, gt = self.set_up_genotypes_table({})
        at = gt.alleles_table
        at.add_allele(symbol='Vipr2-IRES2-Cre')
        with self.assertRaises(ValueError):
            at.add_external_resource(
                column='not_a_column',
                key=key,
                resource_name=resource_name,
                resource_uri=resource_uri,
                entity_id=entity_id,
                entity_uri=entity_uri
            )


class TestGenotypesTable(TestCase):

    def test_constructor_basic(self):
        """Test that the constructor for GenotypesTable sets values as expected."""
        gt = GenotypesTable(
            process='PCR',
            process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
            assembly='GRCm38.p6',
            annotation='NCBI Mus musculus Annotation Release 108',
        )
        self.assertEqual(gt.name, 'genotypes_table')
        self.assertEqual(gt.process, 'PCR')
        self.assertEqual(gt.process_url, 'https://dx.doi.org/10.17504/protocols.io.yjifuke')
        self.assertEqual(gt.assembly, 'GRCm38.p6')
        self.assertEqual(gt.annotation, 'NCBI Mus musculus Annotation Release 108')
        self.assertIsInstance(gt.alleles_table, AllelesTable)

    def set_up_genotypes_table(self, kwargs):
        nwbfile = ERNWBFile(
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
        return nwbfile, gt

    def test_add_external_resource(self):
        nwbfile, gt = self.set_up_genotypes_table({})
        gt.add_allele(symbol='Vip-IRES-Cre')
        gt.add_allele(symbol='wt')
        gt.add_genotype(
            locus='Vip',
            allele1='Vip-IRES-Cre',
            allele2='wt',
            locus_resource_name='locus_resource_name',
            locus_resource_uri='locus_resource_uri',
            locus_entity_id='locus_entity_id',
            locus_entity_uri='locus_entity_uri'
        )
        self.assertEqual(nwbfile.external_resources.keys.data, [('Vip',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'locus_entity_id', 'locus_entity_uri')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('locus_resource_name',  'locus_resource_uri')])

    def test_external_resource_warning(self):
        _, gt = self.set_up_genotypes_table({})
        gt.add_allele(symbol='Vip-IRES-Cre')
        gt.add_allele(symbol='wt')
        gt.add_genotype(
            locus='Vip',
            allele1='Vip-IRES-Cre',
            allele2='wt'
        )
        msg = "User did not provide ExternalResources parameters. No external resource was created."
        with self.assertWarnsWith(UserWarning, msg):
            gt.add_genotype(
                locus='Vip',
                allele1='Vip-IRES-Cre',
                allele2='wt'
            )

    def test_add_minimal_with_allele_index(self):
        """Test the constructor for GenotypesTable when passed indices into AllelesTable."""
        _, gt = self.set_up_genotypes_table({})
        gt.add_allele(symbol='Vip-IRES-Cre')  # TODO warn if there is no external resource / identifier
        gt.add_allele(symbol='wt')
        gt.add_genotype(
            locus='Vip',  # TODO warn if there is no external resource / identifier
            allele1=0,
            allele2=1,
        )

        self._test_minimal_helper(gt)

    def test_add_minimal_with_allele_symbol(self):
        """Test that the constructor for GenotypesTable sets values as expected."""
        _, gt = self.set_up_genotypes_table({})
        gt.add_allele(symbol='Vip-IRES-Cre')  # TODO warn if there is no external resource / identifier
        gt.add_allele(symbol='wt')
        gt.add_genotype(
            locus='Vip',  # TODO warn if there is no external resource / identifier
            allele1='Vip-IRES-Cre',
            allele2='wt',
        )

        self._test_minimal_helper(gt)

    def _test_minimal_helper(self, gt):
        exp = pd.DataFrame({'locus': ['Vip'], 'allele1': ['Vip-IRES-Cre'], 'allele2': ['wt']},
                           index=pd.Index(name='id', data=[0]))
        pd.testing.assert_frame_equal(gt.to_dataframe(), exp)

        # test that allele1 and allele2 values are indices internally
        exp = pd.DataFrame({'locus': ['Vip'], 'allele1': [0], 'allele2': [1]}, index=pd.Index(name='id', data=[0]))
        pd.testing.assert_frame_equal(gt.get(0, index=True), exp)

        # get the locus column contents
        self.assertEqual(gt[:, 'locus'], ['Vip'])

        # get allele1 column contents -- should be a dataframe with subset of alleles table
        exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre']}, index=pd.Index(name='id', data=[0]))
        pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)

        # get allele2 column contents -- should be a dataframe with subset of alleles table
        exp = pd.DataFrame({'symbol': ['wt']}, index=pd.Index(name='id', data=[1]))
        pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)

    def test_add_typical(self):
        nwbfile, gt = self.set_up_genotypes_table(dict(process='PCR'))
        gt.add_allele(symbol='Vip-IRES-Cre')
        gt.add_allele(symbol='wt')
        gt.add_allele(symbol='Ai14(RCL-tdT)')
        gt.add_genotype(
            locus='Vip',
            allele1='Vip-IRES-Cre',
            allele2='wt',
            locus_resource_name='locus_resource_name',
            locus_resource_uri='locus_resource_uri',
            locus_entity_id='locus_entity_id_1',
            locus_entity_uri='locus_entity_uri_1'
        )
        gt.add_genotype(
            locus='ROSA26',
            allele1='Ai14(RCL-tdT)',
            allele2='wt',
            locus_resource_name='locus_resource_name',
            locus_resource_uri='locus_resource_uri',
            locus_entity_id='locus_entity_id_2',
            locus_entity_uri='locus_entity_uri_2'
        )

        self.assertEqual(gt[:, 'locus'], ['Vip', 'ROSA26'])
        exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre', 'Ai14(RCL-tdT)']}, index=pd.Index(name='id', data=[0, 2]))
        pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)
        exp = pd.DataFrame({'symbol': ['wt', 'wt']}, index=pd.Index(name='id', data=[1, 1]))
        pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)

        self.assertEqual(nwbfile.external_resources.keys.data, [('Vip',), ('ROSA26',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'locus_entity_id_1', 'locus_entity_uri_1'),
                                                                    (1, 0, 'locus_entity_id_2', 'locus_entity_uri_2')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('locus_resource_name',  'locus_resource_uri')])

    def test_add_full(self):
        nwbfile, gt = self.set_up_genotypes_table(dict(
            process='PCR',
            process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
            assembly='GRCm38.p6',
            annotation='NCBI Mus musculus Annotation Release 108',
        ))
        gt.add_allele(symbol='Vip-IRES-Cre')
        gt.add_allele(symbol='wt')
        gt.add_allele(symbol='Ai14(RCL-tdT)')
        gt.add_allele(symbol='allele3')
        gt.add_genotype(
            locus='Vip',
            allele1='Vip-IRES-Cre',
            allele2='wt',
            allele3='wt',
            locus_resource_name='locus_resource_name',
            locus_resource_uri='locus_resource_uri',
            locus_entity_id='locus_entity_id_1',
            locus_entity_uri='locus_entity_uri_1')
        gt.add_genotype(
            locus='ROSA26',
            allele1='Ai14(RCL-tdT)',
            allele2='wt',
            allele3='allele3',
            locus_resource_name='locus_resource_name',
            locus_resource_uri='locus_resource_uri',
            locus_entity_id='locus_entity_id_2',
            locus_entity_uri='locus_entity_uri_2')

        self.assertEqual(gt[:, 'locus'], ['Vip', 'ROSA26'])
        exp = pd.DataFrame({'symbol': ['Vip-IRES-Cre', 'Ai14(RCL-tdT)']}, index=pd.Index(name='id', data=[0, 2]))
        pd.testing.assert_frame_equal(gt[:, 'allele1'], exp)
        exp = pd.DataFrame({'symbol': ['wt', 'wt']}, index=pd.Index(name='id', data=[1, 1]))
        pd.testing.assert_frame_equal(gt[:, 'allele2'], exp)
        exp = pd.DataFrame({'symbol': ['wt', 'allele3']}, index=pd.Index(name='id', data=[1, 3]))
        pd.testing.assert_frame_equal(gt[:, 'allele3'], exp)

        self.assertEqual(nwbfile.external_resources.keys.data, [('Vip',), ('ROSA26',)])
        self.assertEqual(nwbfile.external_resources.entities.data, [(0, 0, 'locus_entity_id_1', 'locus_entity_uri_1'),
                                                                    (1, 0, 'locus_entity_id_2', 'locus_entity_uri_2')])
        self.assertEqual(nwbfile.external_resources.resources.data, [('locus_resource_name',  'locus_resource_uri')])


class TestGenotypesTableRoundtrip(TestCase):
    """Simple roundtrip test for GenotypesTable."""

    def setUp(self):
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def set_up_genotypes_table(self, kwargs):
        self.nwbfile = ERNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.nwbfile.subject = GenotypeSubject(
            subject_id='3',
            genotype='Rorb-IRES2-Cre/wt',
        )
        gt = GenotypesTable(**kwargs)
        # GenotypesTable must be descendant of NWBFile before add_genotype works
        self.nwbfile.subject.genotypes_table = gt
        return gt

    def roundtrip(self, genotypes_table):
        """
        Add a GenotypeTable to an NWBFile, write it to file, read the file, and test that the GenotypeTable from the
        file matches the original GenotypeTable.
        """
        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(genotypes_table, read_nwbfile.subject.genotypes_table)
            errors = pynwb_validate(io, namespace='ndx-genotype')
            if errors:
                for err in errors:
                    raise Exception(err)

    def test_roundtrip_minimal(self):
        # NOTE: writing an empty table is not allowed and raises an error
        gt = self.set_up_genotypes_table(dict())
        gt.add_allele('Rorb-IRES2-Cre')
        gt.add_allele('wt')
        gt.add_allele('None')
        gt.add_genotype(
            locus='Rorb',
            allele1='Rorb-IRES2-Cre',
            allele2='wt',
            allele3='None'
        )
        self.roundtrip(gt)

    def test_roundtrip_typical(self):
        gt = self.set_up_genotypes_table(dict(
            process='PCR',
        ))
        gt.add_allele('Rorb-IRES2-Cre')
        gt.add_allele('wt')
        gt.add_allele('Rorb-allele1_symbol-Cre')
        gt.add_allele('allele2_symbol')
        gt.add_allele('None')
        gt.add_genotype(
            locus='Rorb',
            allele1='Rorb-IRES2-Cre',
            allele2='wt',
            allele3='None'
        )
        gt.add_genotype(
            locus='locus_symbol',
            allele1='Rorb-allele1_symbol-Cre',
            allele2='allele2_symbol',
            allele3='None'
        )
        self.roundtrip(gt)

    def test_roundtrip_full(self):
        gt = self.set_up_genotypes_table(dict(
            process='PCR',
            process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
            assembly='GRCm38.p6',
            annotation='NCBI Mus musculus Annotation Release 108',
        ))
        gt.add_allele('Rorb-IRES2-Cre')
        gt.add_allele('wt')
        gt.add_allele('allele1_symbol')
        gt.add_allele('allele2_symbol')
        gt.add_allele('allele3_symbol')
        gt.add_allele('None')

        gt.add_genotype(
            locus='Rorb2',
            allele1='Rorb-IRES2-Cre',
            allele2='wt',
            allele3='None'
        )
        gt.add_genotype(
            locus='locus_symbol',
            allele1='allele1_symbol',
            allele2='allele2_symbol',
            allele3='allele3_symbol'
        )
        self.roundtrip(gt)


class TestGenotypeSubjectConstructor(TestCase):

    def test_constructor(self):
        """Test that the constructor for GenotypeSubject sets values as expected."""
        gt = GenotypesTable()

        subject = GenotypeSubject(
            age='P50D',
            description='Mouse',
            genotype='Rorb-IRES2-Cre/wt',
            genotypes_table=gt,
            sex='M',
            species='Mus musculus',
            subject_id='3',
            weight='2 lbs',
            date_of_birth=datetime.datetime(2017, 5, 1, 12, tzinfo=tzlocal())
        )

        self.assertIs(subject.genotypes_table, gt)


class TestGenotypeSubjectRoundtrip(TestCase):
    """Simple roundtrip test for GenotypeSubject."""

    def setUp(self):
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a GenotypeSubject with a GenotypesTable to an NWBFile, write it to file, read the file, and test that the
        GenotypeSubject from the file matches the original GenotypeSubject.
        """
        self.nwbfile = ERNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.nwbfile.subject = GenotypeSubject(
            age='P50D',
            description='Mouse',
            genotype='Rorb-IRES2-Cre/wt',
            genotypes_table=GenotypesTable(),
            sex='M',
            species='Mus musculus',
            subject_id='3',
            weight='2 lbs',
            date_of_birth=datetime.datetime(2017, 5, 1, 12, tzinfo=tzlocal())
        )
        self.nwbfile.subject.genotypes_table.add_allele('Rorb-IRES2-Cre')
        self.nwbfile.subject.genotypes_table.add_allele('wt')
        self.nwbfile.subject.genotypes_table.add_allele('None')
        self.nwbfile.subject.genotypes_table.add_genotype(
            locus='Rorb',
            allele1='Rorb-IRES2-Cre',
            allele2='wt',
            allele3='None'
        )

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(self.nwbfile.subject, read_nwbfile.subject)
            errors = pynwb_validate(io, namespace='ndx-genotype')
            if errors:
                for err in errors:
                    raise Exception(err)
