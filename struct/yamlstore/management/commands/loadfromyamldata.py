from django.core.management.base import BaseCommand, CommandError

from yamlstore.loaders import read_data_dir
from yamlstore.loaders import dicts_to_objects, extact_paths
from yamlstore.loaders import create_nodes_and_relations


class Command(BaseCommand):
    help = 'Load nodes and relations from YAML files in a specified data directory.'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', nargs='+')

    def handle(self, *args, **options):
        """
        Users the helper methods in loaders.py to load all YAML graph data from
        the files in `data_dir`.
        """
        for data_dir in options['data_dir']:
            all_data = read_data_dir(data_dir)
            data_objects = dicts_to_objects(all_data)
            all_paths, all_path_refs = extact_paths(data_objects)
            print('Found {} node paths and {} path refs'.format(len(all_paths), len(all_path_refs)))
            create_nodes_and_relations(data_objects)
            self.stdout.write(
                self.style.SUCCESS('Loaded YAML graph data from dir ' + data_dir)
            )