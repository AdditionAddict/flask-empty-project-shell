import unittest
import os
import json
from flask import current_app

import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app import create_app, db

class APITestCase(unittest.TestCase):
    """This class represents the API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.bucketlist = {
            'name': 'Oranges',
            'category': 'Food',
            'description': 'Round citrus fruit',
            'price': 5.59
        }
        db.create_all()


    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_api_creation(self):
        """Test API can create a product (POST request)"""
        res = self.client.post('/api/v1/products/',
            data=json.dumps(self.bucketlist),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('Round citrus fruit', str(res.data))

    def test_api_can_get_all_products(self):
        """Test API can get a product (GET request)."""
        res = self.client.post('/api/v1/products/',
            data=json.dumps(self.bucketlist),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/api/v1/products/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Round citrus fruit', str(res.data))


    # not implemented
    # def test_api_can_get_product_by_id(self):
    #     """Test API can get a single product by using it's id."""
    #     rv = self.client.post('/api/v1/products/',
    #         data=json.dumps(self.bucketlist),
    #         content_type='application/json')
    #     self.assertEqual(rv.status_code, 201)
    #     result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
    #     print('id',result_in_json['product_id'])
    #     result = self.client.get(
    #         '/api/v1/products/{}'.format(result_in_json['product_id']))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('Round citrus fruit', str(result.data))

    def test_product_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        rv = self.client.post('/api/v1/products/',
            data=json.dumps(self.bucketlist),
            content_type='application/json')
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put(
            '/api/v1/products/1',
            data = json.dumps({
                'name': 'Oranges',
                'category': 'Food',
                'description': 'Round bright citrus fruit',
                'price': 5.59
            }), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/api/v1/products/')
        self.assertIn('Round bright', str(results.data))

    def test_product_deletion(self):
        """Test API can delete an existing product. (DELETE request)."""
        rv = self.client.post('/api/v1/products/',
            data=json.dumps(self.bucketlist),
            content_type='application/json')
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/api/v1/products/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/api/v1/products')
        self.assertTrue('Round bright' not in str(result.data))
        #self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
