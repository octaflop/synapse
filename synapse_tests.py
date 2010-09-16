#!/usr/bin/env python
# -*- encoding:utf-8 -*-

"""
The primary tests for synapse.

Divided into:
    * Views: What the user should see and shouldn't.
    * Models: All that database stuff.
"""

import os
import app as synapse
import unittest
import tempfile ## may be redundant


class SynapseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = synapse.app.test_client()

    def tearDown(self):
        pass

    # test empty
    def test_empty_db(self):
        rv = self.app.get('/')
        assert '' in rv.data

    # test post
    def test_post(self):
        rv = self.app.post('/admin/add/text', data=dict(
            title = 'Hellz',
            text = '**bellz**'
            ), follow_redirects=True)
        assert 'Hellz' in rv.data
        assert '<b>bellz</b>' in rv.data

    def register(self, username, password):
        return self.app.post('/admin/add/user', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login(u'cogno', u'powers')
        print rv
        assert '200 OK' in rv.data

    def test_false_login(self):
        rv = self.login('admin', 'default')
        assert 'Invalid!' in rv.data

if __name__ == "__main__":
    unittest.main()
