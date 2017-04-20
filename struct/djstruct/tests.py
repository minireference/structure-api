from nose.tools import eq_, ok_
from pprint import pprint

from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import BaseNode, DependencyRelation
from .serializers import BaseNodeSerializer



class TestBaseNodePersist(TestCase):

    def test_base_node_create(self):
        n = BaseNode(path='mechanics/kinematics')
        n.save()
        ok_(n.id is not None)
        eq_(n.path, 'mechanics/kinematics')

    # def test_path_is_required(self):
    #     pass
    #     n = BaseNode(path=None)
    #     raises...
    #     n.save()


class TestCreateUpdateRetrieveBaseNode(APITestCase):

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
        url = reverse('basenode-list')
        response = self.client.post(url, nodedata, format='json')
        # print response.status_code, response.data['id'], response
        self._nodeid = response.data['id']
        eq_(response.status_code, status.HTTP_201_CREATED, "Can't create.")

    def test_create_node(self):
        self._create_test_node()

    def test_update_node(self):
        self._create_test_node()
        # GET
        url = reverse('basenode-detail', kwargs={'uuid':self._nodeid})
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
        url = reverse('basenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], "test/path")




class TestCreateUpdateRetrieveBaseNode(APITestCase):

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
        url = reverse('basenode-list')
        response = self.client.post(url, nodedata, format='json')
        # print response.status_code, response.data['id'], response
        self._nodeid = response.data['id']
        eq_(response.status_code, status.HTTP_201_CREATED, "Can't create.")

    def test_create_node(self):
        self._create_test_node()

    def test_update_node(self):
        self._create_test_node()
        # GET
        url = reverse('basenode-detail', kwargs={'uuid':self._nodeid})
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
        url = reverse('basenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], "test/path")


class TestRetrieveRelationships(APITestCase):

    def setUp(self):
        client = APIClient()

    def _create_basenodes(self):
        n1 = BaseNode(path='testmath/quadratic_equation')
        n1.save()
        self._n1 = n1
        n2 = BaseNode(path='testmechanics/kinematics')
        n2.save()
        self._n2 = n2
        n3 = BaseNode(path='testmechanics/projectile_motion')
        n3.save()
        self._n3 = n3

    def _create_relations(self):
        r12 = DependencyRelation(
                prerequisite=self._n1,
                usedfor=self._n2,
                level='UGRAD',
                explain_usedfor='test Solving quadratics is useful in kinematics.', 
                explain_prerequisite='test You need to know how to solve quadratic equations to solve certain kinematics problems.'
        )
        r12.save()
        r23 = DependencyRelation(
                prerequisite=self._n2,
                usedfor=self._n3,
                level='GRAD',
                explain_usedfor='One-dimensional kinematics is used in two-dimensional projectile motion.', 
                explain_prerequisite='You should be familiar with one-dimensional kinamtics before attacking two-dimensional kinematics porblems.'
        )
        r23.save()

    def test_prerequisites_good(self):
        self._create_basenodes()
        self._create_relations()
        url_n2 = reverse('basenode-detail', kwargs={'uuid':self._n2.uuid})
        response = self.client.get(url_n2, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], str(self._n2.uuid))
        eq_(response.data['path'], 'testmechanics/kinematics')
        # prerequsites
        eq_(len(response.data['prerequisites']), 1)
        eq_(response.data['prerequisites'][0]['prerequisite']['id'], str(self._n1.uuid))
        eq_(response.data['prerequisites'][0]['level'], 'UGRAD')
        # usedfors
        eq_(len(response.data['usedfors']), 1)
        eq_(response.data['usedfors'][0]['usedfor']['id'], str(self._n3.uuid))
        eq_(response.data['usedfors'][0]['level'], 'GRAD')



class TestRelationshipTransitivity(TestCase):

    def _create_basenodes(self):
        n1 = BaseNode(path='math/quadratic_equation')
        n1.save()
        self._n1 = n1
        n2 = BaseNode(path='mechanics/kinematics')
        n2.save()
        self._n2 = n2
        n3 = BaseNode(path='mechanics/projectile_motion')
        n3.save()
        self._n3 = n3
        
    def _create_relations(self):
        r12 = DependencyRelation(
                prerequisite=self._n1,
                usedfor=self._n2,
                level='UGRAD',
                explain_usedfor='Solving quadratics is useful in kinematics.', 
                explain_prerequisite='You need to know how to solve quadratic equations to solve certain kinematics problems.'
        )
        r12.save()
        r23 = DependencyRelation(
                prerequisite=self._n2,
                usedfor=self._n3,
                level='UGRAD',
                explain_usedfor='One-dimensional kinematics is used in two-dimensional projectile motion.', 
                explain_prerequisite='You should be familiar with one-dimensional kinamtics before attacking two-dimensional kinematics porblems.'
        )
        r23.save()
                
    def test_transitivy_n1n2n3(self):
        self._create_basenodes()
        self._create_relations()
        
        # forward        
        n_start = self._n1
        n_mid = n_start.usedfors.all()[0]
        n_finish = n_mid.usedfors.all()[0]
        eq_(n_finish, self._n3)
        
        # backward
        n_mid = n_finish.prerequsites.all()[0]
        n_start = n_mid.prerequsites.all()[0]
        eq_(n_start, self._n1)
        



        
class TestDjangoBaseRelationshipPersist(TestCase):

    def _create_basenodes(self):
        n1 = BaseNode(path='math/quadratic_equation')
        n1.save()
        self._n1 = n1
        n2 = BaseNode(path='mechanics/kinematics')
        n2.save()
        self._n2 = n2
        
    def test_baserelation_create(self):
        self._create_basenodes()
        n1 = self._n1
        n2 = self._n2        
        r = DependencyRelation(
                prerequisite=n1,
                usedfor=n2,
                level='UGRAD',
                explain_usedfor='Solving quadratics is useful in kinematics.', 
                explain_prerequisite='You need to know how to solve quadratic equations to solve certain kinematics problems.'
        )
        r.save()
        ok_(r.id is not None)
        eq_(r.level, 'UGRAD')

        eq_(len(n1.prerequsites.all()), 0)
        eq_(len(n1.usedfors.all()), 1)
        eq_(n1.usedfors.all()[0], n2)

        eq_(len(n2.prerequsites.all()), 1)
        eq_(n2.prerequsites.all()[0], n1)
        eq_(len(n2.usedfors.all()), 0)
