from nose.tools import eq_, ok_

from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import DjangoBaseNode
from .serializers import DjangoBaseNodeSerializer



class TestDjangoBaseNodePersist(TestCase):

    def test_base_node_create(self):
        n = DjangoBaseNode(path='mechanics/kinematics')
        n.save()
        ok_(n.id is not None)
        eq_(n.path, 'mechanics/kinematics')

    # def test_path_is_required(self):
    #     pass
    #     n = BaseNode(path=None)
    #     raises...
    #     n.save()


class TestCreateUpdateRetrieveDjangoBaseNode(APITestCase):

    def setUp(self):
        # print 'in setUp ...'
        client = APIClient()

    def _create_test_node(self):
        nodedata = {
            "path": "test/path",
            "scope": "minireftest",
            "version": "0.1",
            "comment": "Le comment",
        }
        url = reverse('djangobasenode-list')
        response = self.client.post(url, nodedata, format='json')
        # print response.status_code, response.data['id'], response
        self._nodeid = response.data['id']
        eq_(response.status_code, status.HTTP_201_CREATED, "Can't create.")

    def test_create_node(self):
        self._create_test_node()

    def test_update_node(self):
        self._create_test_node()
        # GET
        url = reverse('djangobasenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        # print response.status_code, response
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], "test/path")
        # CHANGE
        putdata = response.data
        putdata['path'] = "test/updated_path"
        # PUT
        response = self.client.put(url, putdata, format='json')
        # print response.status_code, response
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], self._nodeid)
        eq_(response.data['path'], "test/updated_path")

    def test_retrieve_node(self):
        self._create_test_node()
        url = reverse('djangobasenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], "test/path")

