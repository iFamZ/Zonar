import unittest
from unittest import mock
import os, tempfile, shutil, json, io
from utility.publisher import Publisher

# instead of calling publish - mock that to call a different function which writes that message
# to a text file so we can compare it later

class TestPublisher(unittest.TestCase):
    '''
    This unittest covers the Publisher class
    :param: mock command for Publisher
    :return: it will check if the mock command has been called
    '''

    def setUp(self) -> None:
        self.assets = os.path.join('utility', 'tests', 'assets')
        self.test_dir = tempfile.mkdtemp(suffix='test_publisher')
        self.output_file = os.path.join(self.test_dir, 'output_file.txt')

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def new_publish(self, data: dict):
        with open(self.output_file, 'a') as file:
            print('data: {}'.format(data) )
            file.write('{}\n'.format(str(data)))

    def run_translate(self, input_stream, expected_output_file) -> bool:
        '''
        this function takes in an input stream and an expected output and checks that they match
        '''
        publisher = Publisher()
        with mock.patch.object(Publisher, 'publish', new=self.new_publish), mock.patch.object(Publisher, '_print_error', new=self.new_publish):
            publisher.translate(input_stream)
        publisher.translate(input_stream)
        self.assert_files_match(expected_output_file)

    def assert_files_match(self, expected_output_file) -> None:
        with open(self.output_file) as f:
            output_list = f.readlines()
        with open(expected_output_file) as f:
            expected_list = f.readlines()
        self.assertListEqual(output_list, expected_list)

    def get_input_data(self, asset_name: str) -> dict:
        with open(os.path.join(self.assets, asset_name)) as f:
            input_json = json.load(f)
        return input_json

    def test_translate_normal(self) -> None:
        '''
        tests that the basic normal functionality of translate is working as expected
        '''
        input_stream = self.get_input_data('normal_stream.json')['data']
        expected_output_file = os.path.join(self.assets, 'normal_stream_expected.txt')
        self.run_translate(input_stream, expected_output_file)

    def test_translate_no_publish(self) -> None:
        '''
        tests that the no publish functionality of translate is working as expected
        - we have nothing published because there is no latitude and longitude match
        '''
        print('running no publish')
        input_stream = self.get_input_data('no_publish.json')['data']
        publisher = Publisher()
        publisher.translate(input_stream)
        self.assertEqual(len(os.listdir(self.test_dir)), 0)

    def test_translate_out_of_order(self) -> None:
        print('running out of order')
        input_stream = self.get_input_data('out_of_order.json')['data']
        expected_output_file = os.path.join(self.assets, 'out_of_order_expected.txt')
        self.run_translate(input_stream, expected_output_file)

    def test_translate_overwrite_timestamp(self) -> None:
        print('running overwrite timestamp')
        input_stream = self.get_input_data('overwrite_old_timestamp_data.json')['data']
        expected_output_file = os.path.join(self.assets, 'overwrite_old_timestamp_data_expected.txt')
        self.run_translate(input_stream, expected_output_file)

    def test_translate_speed_first(self) -> None:
        print('running speed first')
        input_stream = self.get_input_data('speed_first.json')['data']
        expected_output_file = os.path.join(self.assets, 'speed_first_expected.txt')
        self.run_translate(input_stream, expected_output_file)

    def test_translate_corrupted_data(self) -> None:
        print('running corrupted data')
        input_stream = self.get_input_data('corrupted_data.json')['data']
        expected_output_file = os.path.join(self.assets, 'corrupted_data_expected.txt')
        self.run_translate(input_stream, expected_output_file)

    def test_translate_interrupted_data(self) -> None:
        print('running interrupted data')
        publisher = Publisher()
        input_stream1 = self.get_input_data('interrupted_data_p1.json')['data']
        expected_output_file1 = os.path.join(self.assets, 'interrupted_data_p1_expected.txt')
        input_stream2 = self.get_input_data('interrupted_data_p2.json')['data']
        expected_output_file2 = os.path.join(self.assets, 'interrupted_data_p2_expected.txt')
        with mock.patch.object(Publisher, 'publish', new=self.new_publish), mock.patch.object(Publisher, '_print_error', new=self.new_publish):
            publisher.translate(input_stream1)
            self.assert_files_match(expected_output_file1)
            publisher.translate(input_stream2)
            self.assert_files_match(expected_output_file2)