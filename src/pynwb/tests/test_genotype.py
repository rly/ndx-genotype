import datetime
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO, validate as pynwb_validate
from pynwb.testing import TestCase, remove_test_file

from ndx_genotype import GenotypeNWBFile, GenotypeSubject, GenotypesTable


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

    def set_up_genotypes_table(self, kwargs):
        nwbfile = GenotypeNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        nwbfile.subject = GenotypeSubject(
            subject_id='3',
            genotype='Rorb-IRES2-Cre/wt',
        )
        gt = GenotypesTable(**kwargs)
        nwbfile.subject.genotypes_table = gt  # GenotypesTable must be descendant of NWBFile before add_genotype works
        # TODO remove this dependency
        return gt

    def test_add_minimal(self):
        """Test that the constructor for GenotypesTable sets values as expected."""
        gt = self.set_up_genotypes_table({})
        gt.add_genotype(
            locus_symbol='Rorb',
            locus_crid=[('MGI', '1343464')],
            allele1_symbol='Rorb-IRES2-Cre',
        )
        self.assertEqual(gt[:, 'locus_symbol'], ['Rorb'])
        self.assertEqual(gt[:, 'allele1_symbol'], ['Rorb-IRES2-Cre'])
        self.assertTupleEqual(gt.get_locus_crid(0), (('MGI', '1343464'), ))

    def test_add_typical(self):
        gt = self.set_up_genotypes_table(dict(process='PCR'))
        gt.add_genotype(
            locus_symbol='Rorb',
            locus_crid=[('MGI', '1343464'), ('NCBI Gene', '225998')],
            allele1_symbol='Rorb-IRES2-Cre',
            allele1_crid=[('MGI', '5507855')],
            allele2_symbol='wt',
        )
        gt.add_genotype(
            locus_symbol='locus_symbol',
            locus_crid=[('MGI', '1')],
            allele1_symbol='allele1_symbol',
            allele1_crid=[('MGI', '2'), ('NCBI Gene', '3')],
            allele2_symbol='allele2_symbol',
        )
        self.assertEqual(gt[:, 'locus_symbol'], ['Rorb', 'locus_symbol'])
        self.assertEqual(gt[:, 'allele1_symbol'], ['Rorb-IRES2-Cre', 'allele1_symbol'])
        self.assertTupleEqual(gt.get_locus_crid(0), (('MGI', '1343464'), ('NCBI Gene', '225998')))
        self.assertTupleEqual(gt.get_locus_crid(1), (('MGI', '1'), ))
        self.assertTupleEqual(gt.get_allele1_crid(0), (('MGI', '5507855'), ))
        self.assertTupleEqual(gt.get_allele1_crid(1), (('MGI', '2'), ('NCBI Gene', '3')))

    def test_add_full(self):
        gt = self.set_up_genotypes_table(dict(
            process='PCR',
            process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
            assembly='GRCm38.p6',
            annotation='NCBI Mus musculus Annotation Release 108',
        ))
        gt.add_genotype(
            locus_symbol='Rorb2',
            locus_type='Gene',
            locus_crid=[('MGI', '1343464'), ('NCBI Gene', '225998')],
            allele1_symbol='Rorb-IRES2-Cre',
            allele1_type='Targeted (Recombinase)',
            allele1_crid=[('MGI', '5507855')],
            allele2_symbol='wt',
            allele2_type='Wild Type',
            allele2_crid=[],
            allele3_symbol='None',  # TODO handle case where one gene has more alleles than the others
            allele3_type='None',
            allele3_crid=[],
        )
        gt.add_genotype(
            locus_symbol='locus_symbol',
            locus_type='locus_type',
            locus_crid=[('MGI', '1')],
            allele1_symbol='allele1_symbol',
            allele1_type='allele1_type',
            allele1_crid=[('MGI', '3')],
            allele2_symbol='allele2_symbol',
            allele2_type='allele2_type',
            allele2_crid=[('MGI', '4'), ('NCBI Gene', '5')],
            allele3_symbol='allele3_symbol',
            allele3_type='allele3_type',
            allele3_crid=[('MGI', '6'), ('NCBI Gene', '7'), ('Ensembl', '8')],
        )
        self.assertEqual(gt[:, 'locus_symbol'], ['Rorb2', 'locus_symbol'])
        self.assertEqual(gt[:, 'locus_type'], ['Gene', 'locus_type'])
        self.assertEqual(gt[:, 'allele1_symbol'], ['Rorb-IRES2-Cre', 'allele1_symbol'])
        self.assertEqual(gt[:, 'allele1_type'], ['Targeted (Recombinase)', 'allele1_type'])
        self.assertEqual(gt[:, 'allele2_symbol'], ['wt', 'allele2_symbol'])
        self.assertEqual(gt[:, 'allele2_type'], ['Wild Type', 'allele2_type'])
        self.assertEqual(gt[:, 'allele3_symbol'], ['None', 'allele3_symbol'])
        self.assertEqual(gt[:, 'allele3_type'], ['None', 'allele3_type'])
        self.assertTupleEqual(gt.get_locus_crid(0), (('MGI', '1343464'), ('NCBI Gene', '225998')))
        self.assertTupleEqual(gt.get_locus_crid(1), (('MGI', '1'), ))
        self.assertTupleEqual(gt.get_allele1_crid(0), (('MGI', '5507855'), ))
        self.assertTupleEqual(gt.get_allele1_crid(1), (('MGI', '3'), ))
        self.assertTupleEqual(gt.get_allele2_crid(0), tuple())
        self.assertTupleEqual(gt.get_allele2_crid(1), (('MGI', '4'), ('NCBI Gene', '5')))
        self.assertTupleEqual(gt.get_allele3_crid(0), tuple())
        self.assertTupleEqual(gt.get_allele3_crid(1), (('MGI', '6'), ('NCBI Gene', '7'), ('Ensembl', '8')))

    def test_constructor_bad_crid(self):
        gt = GenotypesTable()

        msg = 'allele1_crid must be an array/list/tuple with tuples of length 2.'
        with self.assertRaisesWith(ValueError, msg):
            gt.add_genotype(
                locus_symbol='Rorb',
                locus_crid=[('MGI', '1')],
                allele1_symbol='Rorb-IRES2-Cre',
                allele2_symbol='wt',
                allele1_crid=[('MGI', '3', 1)],
            )

        msg = ('locus_crid must be an array/list/tuple with tuples where the first element (registry) '
               'is one of: "MGI", "NCBI Gene", or "Ensembl".')
        with self.assertRaisesWith(ValueError, msg):
            gt.add_genotype(
                locus_symbol='Rorb',
                locus_crid=[('REGISTRY', '1')],
                allele1_symbol='Rorb-IRES2-Cre',
                allele2_symbol='wt',
            )

        msg = ('allele2_crid must be an array/list/tuple with tuples where the second element (symbol) is a string.')
        with self.assertRaisesWith(ValueError, msg):
            gt.add_genotype(
                locus_symbol='Rorb',
                locus_crid=[('MGI', '1')],
                allele1_symbol='Rorb-IRES2-Cre',
                allele2_symbol='wt',
                allele2_crid=[('MGI', 3)]
            )

        msg = ('allele3_crid must be an array/list/tuple with tuples where the second element (symbol) is a string.')
        with self.assertRaisesWith(ValueError, msg):
            gt.add_genotype(
                locus_symbol='Rorb',
                locus_crid=[('MGI', '1')],
                allele1_symbol='Rorb-IRES2-Cre',
                allele2_symbol='wt',
                allele3_symbol='wt',
                allele3_crid=[('MGI', 3)]
            )

        msg = ('allele3_symbol must be provided if allele3_type or allele3_crid are provided.')
        with self.assertRaisesWith(ValueError, msg):
            gt.add_genotype(
                locus_symbol='Rorb',
                locus_crid=[('MGI', '1')],
                allele1_symbol='Rorb-IRES2-Cre',
                allele2_symbol='wt',
                allele3_crid=[('MGI', '3')]
            )


class TestGenotypesTableRoundtrip(TestCase):
    """Simple roundtrip test for GenotypesTable."""

    def setUp(self):
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def set_up_genotypes_table(self, kwargs):
        self.nwbfile = GenotypeNWBFile(
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
            self.assertContainerEqual(self.nwbfile.ontology_objects, read_nwbfile.ontology_objects)
            self.assertContainerEqual(self.nwbfile.ontology_terms, read_nwbfile.ontology_terms)
            errors = pynwb_validate(io, namespace='ndx-genotype')
            if errors:
                for err in errors:
                    raise Exception(err)

    def test_roundtrip_minimal(self):
        # NOTE: writing an empty table is not allowed and raises an error
        gt = self.set_up_genotypes_table(dict())
        gt.add_genotype(
            locus_symbol='Rorb',
            locus_crid=[('MGI', '1343464')],
            allele1_symbol='Rorb-IRES2-Cre',
            allele2_symbol='wt',
        )
        self.roundtrip(gt)

    def test_roundtrip_typical(self):
        gt = self.set_up_genotypes_table(dict(
            process='PCR',
        ))
        gt.add_genotype(
            locus_symbol='Rorb',
            locus_crid=[('MGI', '1343464'), ('NCBI Gene', '225998')],
            allele1_symbol='Rorb-IRES2-Cre',
            allele1_crid=[('MGI', '5507855')],
            allele2_symbol='wt',
        )
        gt.add_genotype(
            locus_symbol='locus_symbol',
            locus_crid=[('MGI', '1')],
            allele1_symbol='Rorb-allele1_symbol-Cre',
            allele1_crid=[('MGI', '2'), ('NCBI Gene', '3')],
            allele2_symbol='allele2_symbol',
        )
        self.roundtrip(gt)

    def test_roundtrip_full(self):
        gt = self.set_up_genotypes_table(dict(
            process='PCR',
            process_url='https://dx.doi.org/10.17504/protocols.io.yjifuke',
            assembly='GRCm38.p6',
            annotation='NCBI Mus musculus Annotation Release 108',
        ))
        gt.add_genotype(
            locus_symbol='Rorb2',
            locus_type='Gene',
            locus_crid=[('MGI', '1343464'), ('NCBI Gene', '225998')],
            allele1_symbol='Rorb-IRES2-Cre',
            allele1_type='Targeted (Recombinase)',
            allele1_crid=[('MGI', '5507855')],
            allele2_symbol='wt',
            allele2_type='Wild Type',
            allele2_crid=[],
            allele3_symbol='None',
            allele3_type='None',
            allele3_crid=[],
        )
        gt.add_genotype(
            locus_symbol='locus_symbol',
            locus_type='locus_type',
            locus_crid=[('MGI', '1')],
            allele1_symbol='allele1_symbol',
            allele1_type='allele1_type',
            allele1_crid=[('MGI', '3')],
            allele2_symbol='allele2_symbol',
            allele2_type='allele2_type',
            allele2_crid=[('MGI', '4'), ('NCBI Gene', '5')],
            allele3_symbol='allele3_symbol',
            allele3_type='allele3_type',
            allele3_crid=[('MGI', '6'), ('NCBI Gene', '7'), ('Ensembl', '8')],
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
        self.nwbfile = GenotypeNWBFile(
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
        self.nwbfile.subject.genotypes_table.add_genotype(
            locus_symbol='Rorb',
            locus_crid=[('MGI', '1343464')],
            allele1_symbol='Rorb-IRES2-Cre',
            allele2_symbol='wt',
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
