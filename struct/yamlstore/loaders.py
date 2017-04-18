import os
import yaml

from djstruct.models import DjangoBaseNode, DjangoDependencyRelation

# DATA DIRECTORY PARSER
################################################################################

def read_data_dir(data_dir, recurse=False):
    """
    Read all yaml files in `data_dir` including dir. ceontext file `context.yml`.
    Returns a list of dict obejcts that correspond graph nodes.
    """
    all_data = []
    contexts = []   # list of dicts that contain context (rightmost has priority)
    for raw_path, subfolders, filenames in os.walk(data_dir):
        # 1. LOAD CONTEXT
        if 'context.yml' in filenames:
            context_yaml_file = os.path.join(raw_path, 'context.yml')
            context_dict = yaml.load(open(context_yaml_file))
            contexts.append(context_dict)
            filenames.remove('context.yml')
        #
        # 2. PROCESS EACH YAML FILE
        for filename in filenames:
            file_key, file_ext = os.path.splitext(filename)
            if file_ext in ['.yml', '.yaml']:
                this_yaml_file = os.path.join(data_dir, filename)
                this_data = yaml.load(open(this_yaml_file))
                #
                for raw_datum in this_data:
                    new_datum = {}
                    for context in contexts:
                        new_datum.update(context)
                    new_datum.update(raw_datum)
                    all_data.append(new_datum)
        #
        if recurse == False:     # read only files in top-level directory
            break
    #
    return all_data



# YAML PARSING HELPER CLASSES
################################################################################

class PrerequisteReference(object):
    """
    A wrapper that accepts either a string or a dict prerequisite data.
    """
    def __init__(self, data):
        if isinstance(data, basestring):
            self.prerequisite = data
            self.explain_prerequisite = None
            self.level = None
        elif isinstance(data, dict):
            self.prerequisite = data.get('prerequisite')
            self.explain_prerequisite = data.get('explain', None)
            self.level = data.get('level', None)
        else:
            raise ValueError('data must be string or dict')


class UsedforReference(object):
    """
    A wrapper that accepts either a string or a dict usedfor data.
    """
    def __init__(self, data):
        if isinstance(data, basestring):
            self.usedfor = data
            self.explain_usedfor = None
            self.level = None
        elif isinstance(data, dict):
            self.usedfor = data.get('usedfor')
            self.explain_usedfor = data.get('explain', None)
            self.level = data.get('level', None)
        else:
            raise ValueError('data must be string or dict')


class RelatedReference(object):
    """
    A wrapper that accepts either a string or a dict relation data.
    """
    def __init__(self, source, data):
        if source is None:
            raise ValueError('must give relation source path')
        self.source = source
        if isinstance(data, basestring):
            self.related = data
            self.explain = None
            self.level = None
        elif isinstance(data, dict):
            self.related = data.get('related')
            self.explain = data.get('explain', None)
            self.level = data.get('level', None)
        else:
            raise ValueError('data must be string or dict')



# MAIN NODE YAML PARSING CLASS
################################################################################

class NodeFromYamlDict(object):
    """
    A class to handle loading a Node from it's YAML serarializaiton.
    Usage:
        node = NodeFromYamlDict(dict)
        node.path / node.description / etc. are now available (or None)
    """
    def __init__(self, datum):
        if not datum['path']:
            raise ValueError('Yaml data must have a `path`.')
        self.path = datum['path']
        if not datum['scope']:
            raise ValueError('Yaml data must have a `scope`.')
        self.scope = datum['scope']
        # what type of Node is it?
        self.node_class = datum.get('__class__', 'Node')
        #
        # aliases
        self.aliases = []
        if 'aliases' in datum and datum['aliases'] is not None:
            for alias in datum['aliases']:
                self.aliases.append(alias)
        #
        # optional properties: level, description, books
        optional_props = ['level', 'description', 'books']
        for prop_name in optional_props:
            if prop_name in datum and datum[prop_name] is not None:
                setattr(self, prop_name, datum[prop_name])   
        #
        # process prereqs and usedfors
        self.prerequisites = []
        self.usedfors = []
        if 'prerequisites' in datum and datum['prerequisites'] is not None:
            for prereq_str_or_dict in datum['prerequisites']:
                prereq = PrerequisteReference(prereq_str_or_dict)
                self.prerequisites.append(prereq)
        if 'usedfors' in datum and datum['usedfors'] is not None:
            for usedfor_str_or_dict in datum['usedfors']:
                usedfor = UsedforReference(usedfor_str_or_dict)
                self.usedfors.append(usedfor)
        #
        # relations
        self.relations = []
        if 'relations' in datum and datum['relations'] is not None:
            for relation_str_or_dict in datum['usedfors']:
                relation = RelatedReference(self.path, relation_str_or_dict)
                self.relations.append(relation)
        # TODO: ispartof/contents 
        # also ccmms-specific ones: ccss_guid, ccss_url, asn_url



# LOADING UTILITY FUNCTIONS 
################################################################################

def dicts_to_objects(all_data):
    """
    Inflate list of data dicts into NodeFromYamlDict objects, including properties
    as `PrerequisteReference`, `UsedforReference`, `RelatedReference`.
    """
    data_objects = []
    for datum in all_data:
        obj = NodeFromYamlDict(datum)
        data_objects.append(obj)
    return data_objects


def extact_paths(data_objects):
    """
    Get a list of all object paths and all the paths that appear in relations.
    Returns a tuple of lists.
    """
    all_paths = set()
    all_path_refs = set()

    for obj in data_objects:
        all_paths.add(obj.path)
        for prereq in obj.prerequisites:
            all_path_refs.add(prereq.prerequisite)
        for ufor in obj.usedfors:
            all_path_refs.add(ufor.usedfor)
        for rel in obj.relations:
            all_path_refs.add(rel.related)
    return (all_paths, all_path_refs)


def create_nodes_and_relations(data_objects):
    """
    Creates the actual Node and Relations objects and saves them to the DB.
    """
    all_paths, all_path_refs = extact_paths(data_objects)

    # PASS 1. create nodes
    for obj in data_objects:
        node = DjangoBaseNode(
            path=obj.path,
            scope='miniref'
        )
        node.save()

    # PASS 2. create relations
    for obj in data_objects:
        node = DjangoBaseNode.objects.get(path=obj.path)
        for prereq in obj.prerequisites:
            prereq_path = prereq.prerequisite
            if prereq.prerequisite in all_paths:
                prereq_node = DjangoBaseNode.objects.get(path=prereq_path)
                # both ends exist...
                rel = DjangoDependencyRelation(
                        prerequisite=prereq_node,
                        usedfor=node,
                        explain_prerequisite=prereq.explain_prerequisite
                )
                if prereq.level is not None:
                    rel.level = prereq.level
                rel.save()

