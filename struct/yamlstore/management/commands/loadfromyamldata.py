from django.core.management.base import BaseCommand, CommandError
# from djstruct.models import DjangoBaseNode, DjangoDependencyRelation

from yamlstore.loaders import read_data_dir
from yamlstore.loaders import dicts_to_objects, extact_paths
from yamlstore.loaders import create_nodes_and_relations


class Command(BaseCommand):
    help = 'Load nodes and relations from YAML files in a specified data directory.'


    def add_arguments(self, parser):
        parser.add_argument('data_dir', nargs='+')

    def handle(self, *args, **options):
        
        for data_dir in options['data_dir']:
            all_data = read_data_dir(data_dir)
            data_objects = dicts_to_objects(all_data)
            all_paths, all_path_refs = extact_paths(data_objects)
            create_nodes_and_relations(data_objects)
            self.stdout.write(
                self.style.SUCCESS('Loaded YAML data from dir ' + data_dir)
            )