import datetime
import numpy as np

from pynwb import NWBHDF5IO, TimeSeries, validate as pynwb_validate
from pynwb.core import DynamicTable
from pynwb.testing import TestCase, remove_test_file

from ndx_genotype import GenotypeNWBFile, OntologyTable, OntologyMap


class TestNWBFileConstructor(TestCase):

    def test_constructor_basic(self):
        """Test that the constructor for GenotypesTable sets values as expected."""
        nwbfile = GenotypeNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.assertIsInstance(nwbfile.ontology_objects, OntologyTable)
        self.assertIsInstance(nwbfile.ontology_terms, OntologyMap)
        self.assertEqual(len(nwbfile.ontology_objects), 0)
        self.assertEqual(len(nwbfile.ontology_terms), 0)


class TestOntologies(TestCase):

    def test_basic(self):
        """Test adding rows to the ontology_terms and ontology_objects tables."""
        nwbfile = GenotypeNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )

        container = TimeSeries(
            name='test_ts',
            data=[1, 2, 3],
            unit='si_unit',
            timestamps=[0.1, 0.2, 0.3],
        )
        nwbfile.add_acquisition(container)

        table = DynamicTable(name='test_table', description='test table description')
        table.add_column(name='test_col', description='test column description')
        table.add_row(test_col='Mouse')

        nwbfile.add_acquisition(table)

        nwbfile.ontology_terms.add_row(
            id=np.uint64(1),
            key='meter',
            ontology='si_ontology',
            uri='si_ontology:m',
        )
        nwbfile.ontology_objects.add_row(
            id=np.uint64(5),
            object_id=container.object_id,
            field='unit',
            item=np.uint64(1),
        )
        nwbfile.ontology_terms.add_row(
            id=np.uint64(2),
            key='Mouse',
            ontology='species_ontology',
            uri='species_ontology:Mus musculus',
        )
        nwbfile.ontology_objects.add_row(
            id=np.uint64(6),
            object_id=table.object_id,
            field='test_col',
            item=np.uint64(2),
        )

        self.assertEqual(len(nwbfile.ontology_objects), 2)
        self.assertEqual(len(nwbfile.ontology_terms), 2)
        self.assertTupleEqual(nwbfile.ontology_objects[0], (np.uint64(5), container.object_id, 'unit', np.uint64(1)))
        self.assertTupleEqual(nwbfile.ontology_objects[1], (np.uint64(6), table.object_id, 'test_col', np.uint64(2)))
        self.assertTupleEqual(nwbfile.ontology_terms[0], (np.uint64(1), 'meter', 'si_ontology', 'si_ontology:m'))
        self.assertTupleEqual(nwbfile.ontology_terms[1], (np.uint64(2), 'Mouse', 'species_ontology',
                                                          'species_ontology:Mus musculus'))


class TestOntologiesRoundTrip(TestCase):

    def setUp(self):
        self.nwbfile = GenotypeNWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_empty(self):
        """Test writing and reading empty ontology_terms and ontology_objects tables."""

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertEqual(len(self.nwbfile.ontology_objects), 0)
            self.assertEqual(len(self.nwbfile.ontology_terms), 0)
            self.assertContainerEqual(self.nwbfile.ontology_objects, read_nwbfile.ontology_objects)
            self.assertContainerEqual(self.nwbfile.ontology_terms, read_nwbfile.ontology_terms)

    def test_roundtrip(self):
        """Test writing and reading the ontology_terms and ontology_objects tables."""

        container = TimeSeries(
            name='test_ts',
            data=[1, 2, 3],
            unit='si_unit',
            timestamps=[0.1, 0.2, 0.3],
        )
        self.nwbfile.add_acquisition(container)

        table = DynamicTable(name='test_table', description='test table description')
        table.add_column(name='test_col', description='test column description')
        table.add_row(test_col='Mouse')

        self.nwbfile.add_acquisition(table)

        self.nwbfile.ontology_terms.add_row(
            id=np.uint64(1),
            key='meter',
            ontology='si_ontology',
            uri='si_ontology:m',
        )
        self.nwbfile.ontology_objects.add_row(
            id=np.uint64(5),
            object_id=container.object_id,
            field='unit',
            item=np.uint64(1),
        )
        self.nwbfile.ontology_terms.add_row(
            id=np.uint64(2),
            key='Mouse',
            ontology='species_ontology',
            uri='species_ontology:Mus musculus',
        )
        self.nwbfile.ontology_objects.add_row(
            id=np.uint64(6),
            object_id=table.object_id,
            field='test_col',
            item=np.uint64(2),
        )

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(self.nwbfile.ontology_objects, read_nwbfile.ontology_objects)
            self.assertContainerEqual(self.nwbfile.ontology_terms, read_nwbfile.ontology_terms)
            errors = pynwb_validate(io, namespace='ndx-genotype')
            if errors:
                for err in errors:
                    raise Exception(err)
