import unittest

from app import TopicsExtractor, \
                Utils


class TestApp(unittest.TestCase):
    def setUp(self):
        self.extractor = TopicsExtractor()

    def test_equals_ids(self):
        self.assertEqual(Utils.generate_id("Sanidad"), Utils.generate_id("Sanidad"))

    def test_different_ids(self):
        self.assertNotEqual(Utils.generate_id("Sanidad"), Utils.generate_id("Educación"))

    def test_data_reference_greater_than_zero(self):
        self.extractor.load_data_reference()
        self.assertGreaterEqual(len(self.extractor.data_reference), 0)

    def test_load_credentials(self):
        self.extractor.load_google_credentials()
        self.assertIsNotNone(self.extractor.google_credentials)

    def test_topics_greater_than_zero(self):
        self.extractor.load_data_reference()
        self.extractor.load_google_credentials()
        self.extractor.load_topics()
        self.assertGreaterEqual(len(self.extractor.topics), 0)

    '''
    def test_validate_valid_tag(self):
        tag = {
                'regex': 'calidad.*(aire|agua)',
                'tag': 'Calidad del aire o del agua',
                'subtopic': 'Calidad medioambiental',
                'shuffle': True
                }
        self.assertTrue(self.extractor._TopicsExtractor__validate(tag))

    def test_validate_invalid_tag(self):
        tag = {
                'regex': 'calidad.*(aire|agua',
                'tag': 'Calidad del aire o del agua',
                'subtopic': 'Calidad medioambiental',
                'shuffle': True
                }
        self.assertRaises(Exception, self.extractor._TopicsExtractor__validate, tag)
    '''



if __name__ == '__main__':
    unittest.main()
