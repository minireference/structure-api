from django.test import TestCase
# from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
# from ..serializers import BaseNodeSerializer

from djstruct.models import BaseNode


class TestBaseNodePersist(TestCase):

    def test_base_node_create(self):
        n = BaseNode(path='mechanics/kinematics')
        n.save()
        ok_(n.id is not None)
        eq_(n.path, 'mechanics/kinematics')
