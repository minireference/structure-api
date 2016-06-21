
import os
from nose.tools import eq_, ok_
import random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TestCase
from neolixir import metadata
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, APISimpleTestCase

from .models import NeolixirBaseNode, NeolixirDependencyRelation


class TestRetrieveRelationships(APISimpleTestCase):

    def setUp(self):
        self._delete_all_testnodes()
        client = APIClient()

    def tearDown(self):
        self._delete_all_testnodes()
        
    def _delete_all_testnodes(self):
        all_nodes = NeolixirBaseNode.query.all()
        test_nodes = [n for n in all_nodes if n.path.startswith('test/') ]
        for tn in test_nodes:
            tn.delete()
        metadata.session.commit()    

    def _create_basenodes(self):
        n1 = NeolixirBaseNode(path='test/math/quadratic_equation')
        n1.save()
        self._n1 = n1
        n2 = NeolixirBaseNode(path='test/mechanics/kinematics')
        n2.save()
        self._n2 = n2
        n3 = NeolixirBaseNode(path='test/mechanics/projectile_motion')
        n3.save()
        self._n3 = n3

    def _create_relations(self):
        r12 = self._n1.usedfors.append(self._n2)
        r12.level='UGRAD'
        r12.explain_usedfor='test Solving quadratics is useful in kinematics.'
        r12.explain_prerequisite='test You need to know how to solve quadratic equations to solve certain kinematics problems.'
        r12.save()
        
        r23 = self._n2.usedfors.append(self._n3)
        r23.level='GRAD'
        r23.explain_usedfor='One-dimensional kinematics is used in two-dimensional projectile motion.'
        r23.explain_prerequisite='You should be familiar with one-dimensional kinamtics before attacking two-dimensional kinematics porblems.'
        r23.save()

    def test_middle_prerequisites_and_usedfors_good(self):
        self._create_basenodes()
        self._create_relations()
        url_n2 = reverse('neolixirbasenode-detail', kwargs={'uuid':self._n2.uuid})
        response = self.client.get(url_n2, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], str(self._n2.uuid))
        eq_(response.data['path'], 'test/mechanics/kinematics')
        # prerequsites
        eq_(len(response.data['prerequisites']), 1)
        eq_(response.data['prerequisites'][0]['prerequisite']['id'], str(self._n1.uuid))
        eq_(response.data['prerequisites'][0]['level'], 'UGRAD')
        # usedfors
        eq_(len(response.data['usedfors']), 1)
        eq_(response.data['usedfors'][0]['usedfor']['id'], str(self._n3.uuid))
        eq_(response.data['usedfors'][0]['level'], 'GRAD')

    def test_third_prerequisites_good(self):
        self._create_basenodes()
        self._create_relations()
        url_n3 = reverse('neolixirbasenode-detail', kwargs={'uuid':self._n3.uuid})
        response = self.client.get(url_n3, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], str(self._n3.uuid))
        eq_(response.data['path'], 'test/mechanics/projectile_motion')
        # prerequsites
        eq_(len(response.data['prerequisites']), 1)
        eq_(response.data['prerequisites'][0]['prerequisite']['id'], str(self._n2.uuid))
        eq_(response.data['prerequisites'][0]['level'], 'GRAD')
        # no usedfors
        eq_(len(response.data['usedfors']), 0)

    def test_first_usedfors_good(self):
        self._create_basenodes()
        self._create_relations()
        url_n1 = reverse('neolixirbasenode-detail', kwargs={'uuid':self._n1.uuid})
        response = self.client.get(url_n1, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], str(self._n1.uuid))
        eq_(response.data['path'], 'test/math/quadratic_equation')
        # no prerequsites
        eq_(len(response.data['prerequisites']), 0)
        # usedfors
        eq_(len(response.data['usedfors']), 1)
        eq_(response.data['usedfors'][0]['usedfor']['id'], str(self._n2.uuid))
        eq_(response.data['usedfors'][0]['level'], 'UGRAD')



class TestBasicCreateNeolixirBaseNodeAndRels(SimpleTestCase):
    
    def setUp(self):
        self._delete_all_testnodes()

    def tearDown(self):
        self._delete_all_testnodes()
        
    def _delete_all_testnodes(self):
        all_nodes = NeolixirBaseNode.query.all()
        test_nodes = [n for n in all_nodes if n.path.startswith('test/') ]
        for tn in test_nodes:
            tn.delete()
        metadata.session.commit()    

    def test_create_nodes_and_reln(self):
        phys = NeolixirBaseNode(path='test/physics')
        phys.save()
        ok_(phys.id)
        
        math = NeolixirBaseNode(path='test/math')
        math.save()
        ok_(math.id)
        
        rel = phys.prerequisites.append(math)
        rel.save()
        ok_(rel.id)
        
        # check endpoints
        eq_(rel._start, phys)
        eq_(rel._end, math)
        # check both directions
        eq_(len(phys.prerequisites), 1)
        eq_(len(math.usedfors), 1)



class TestCreateUpdateRetrieveNeolixirBaseNode(APISimpleTestCase):

    def setUp(self):
        self._delete_all_testnodes()
        # print 'in setUp ...'
        client = APIClient()
        # http://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
        # admin = User.objects.get(id=1)
        # client.force_login(urlresolvers

    def tearDown(self):
        self._delete_all_testnodes()
        
    def _delete_all_testnodes(self):
        all_nodes = NeolixirBaseNode.query.all()
        test_nodes = [n for n in all_nodes if n.path.startswith('test/') ]
        for tn in test_nodes:
            tn.delete()
        metadata.session.commit()

    def _create_test_node(self):
        nonce = str(random.randint(200,300))
        self._newpath = "test/path" + nonce
        nodedata = {
            "path": self._newpath,
            "scope": "minireftest",
            "version": "0.1",
            "comment": "Le comment",
        }
        url = reverse('neolixirbasenode-list')
        response = self.client.post(url, nodedata, format='json')
        # print response.status_code, response.data['id'], response
        # print response.data
        self._nodeid = response.data['id']
        eq_(response.status_code, status.HTTP_201_CREATED, "Can't create.")

    def test_create_node(self):
        self._create_test_node()

    def test_update_node(self):
        self._create_test_node()
        # GET
        url = reverse('neolixirbasenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        # print response.status_code, response
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], self._newpath)
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
        url = reverse('neolixirbasenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], self._newpath)


