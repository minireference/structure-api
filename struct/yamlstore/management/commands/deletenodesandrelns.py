from django.core.management.base import BaseCommand, CommandError
from djstruct.models import DjangoBaseNode, DjangoDependencyRelation

class Command(BaseCommand):
    help = 'Delete all `Node`s and `Relations` from the database. (USED ONLY IN DEV)'

    def handle(self, *args, **options):
        for oldnode in DjangoBaseNode.objects.all():
            oldnode.delete()
        for oldreln in DjangoDependencyRelation.objects.all():
            oldreln.delete()
        
        self.stdout.write(self.style.SUCCESS('All Nodes and Relations deleted'))
