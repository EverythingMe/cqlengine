from cqlengine.tests.base import BaseCassEngTestCase

from cqlengine.exceptions import ModelException
from cqlengine.models import Model
from cqlengine import columns

class TestModelClassFunction(BaseCassEngTestCase):
    """
    Tests verifying the behavior of the Model metaclass
    """

    def test_column_attributes_handled_correctly(self):
        """
        Tests that column attributes are moved to a _columns dict
        and replaced with simple value attributes
        """

        class TestModel(Model):
            text = columns.Text()

        #check class attibutes
        self.assertHasAttr(TestModel, '_columns')
        self.assertHasAttr(TestModel, 'id')
        self.assertHasAttr(TestModel, 'text')

        #check instance attributes
        inst = TestModel()
        self.assertHasAttr(inst, 'id')
        self.assertHasAttr(inst, 'text')
        self.assertIsNone(inst.id)
        self.assertIsNone(inst.text)

    def test_db_map(self):
        """
        Tests that the db_map is properly defined
        -the db_map allows columns
        """
        class WildDBNames(Model):
            content = columns.Text(db_field='words_and_whatnot')
            numbers = columns.Integer(db_field='integers_etc')

        db_map = WildDBNames._db_map
        self.assertEquals(db_map['words_and_whatnot'], 'content')
        self.assertEquals(db_map['integers_etc'], 'numbers')

    def test_attempting_to_make_duplicate_column_names_fails(self):
        """
        Tests that trying to create conflicting db column names will fail
        """

        with self.assertRaises(ModelException):
            class BadNames(Model):
                words = columns.Text()
                content = columns.Text(db_field='words')

    def test_column_ordering_is_preserved(self):
        """
        Tests that the _columns dics retains the ordering of the class definition
        """

        class Stuff(Model):
            words = columns.Text()
            content = columns.Text()
            numbers = columns.Integer()

        self.assertEquals(Stuff._columns.keys(), ['id', 'words', 'content', 'numbers'])

    def test_value_managers_are_keeping_model_instances_isolated(self):
        """
        Tests that instance value managers are isolated from other instances
        """
        class Stuff(Model):
            num = columns.Integer()

        inst1 = Stuff(num=5)
        inst2 = Stuff(num=7)

        self.assertNotEquals(inst1.num, inst2.num)
        self.assertEquals(inst1.num, 5)
        self.assertEquals(inst2.num, 7)

    def test_normal_fields_can_be_defined_between_primary_keys(self):
        """
        Tests tha non primary key fields can be defined between primary key fields
        """

    def test_meta_data_is_not_inherited(self):
        """
        Test that metadata defined in one class, is not inherited by subclasses
        """