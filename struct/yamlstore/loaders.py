import os
import yaml

from djstruct.models import BaseNode
from djstruct.models import DependencyRelation, RelatedRelation, ContainmentRelation

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
        # NOTE: This context handling doesn't work if more than one level of dirs
        #       since contexts dicts do no get "popped" when leaving a dir...
        #       TODO(ivan): fix this and make it general purpose
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

class BaseExplainLevelReference(object):
    """
    A wrapper that accepts either a string or a dict data for the proporty set
    on `self.attribute_name` by the subclasses.
    """
    attribute_name = None

    def __init__(self, data):
        if self.attribute_name is None:
            raise ValueError('Subclass must set self.attribute_name for this to work.')
        if isinstance(data, str):
            setattr(self, self.attribute_name, data)
            setattr(self, 'explain_' + self.attribute_name, None) 
            self.level = None
        elif isinstance(data, dict):
            setattr(self, self.attribute_name, data.get(self.attribute_name))
            setattr(self, 'explain_' + self.attribute_name, data.get('explain', None))
            self.level = data.get('level', None)
        else:
            raise ValueError('data must be string or dict')


class PrerequisteReference(BaseExplainLevelReference):
    def __init__(self, data):
        self.attribute_name = 'prerequisite'
        super(PrerequisteReference, self).__init__(data)

class UsedforReference(BaseExplainLevelReference):
    def __init__(self, data):
        self.attribute_name = 'usedfor'
        super(UsedforReference, self).__init__(data)


class RelatedReference(BaseExplainLevelReference):
    def __init__(self, data):
        self.attribute_name = 'related'
        super(RelatedReference, self).__init__(data)


class ContainsReference(BaseExplainLevelReference):
    def __init__(self, data):
        self.attribute_name = 'contains'
        super(ContainsReference, self).__init__(data)

class IsPartOfReference(BaseExplainLevelReference):
    def __init__(self, data):
        self.attribute_name = 'ispartof'
        super(IsPartOfReference, self).__init__(data)





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
        if 'prerequisites' in datum and datum['prerequisites'] is not None:
            for prereq_str_or_dict in datum['prerequisites']:
                prereq = PrerequisteReference(prereq_str_or_dict)
                self.prerequisites.append(prereq)
        #
        self.usedfors = []
        if 'usedfors' in datum and datum['usedfors'] is not None:
            for usedfor_str_or_dict in datum['usedfors']:
                usedfor = UsedforReference(usedfor_str_or_dict)
                self.usedfors.append(usedfor)
        #
        #
        # process related
        self.relations = []
        if 'relations' in datum and datum['relations'] is not None:
            for relation_str_or_dict in datum['relations']:
                relation = RelatedReference(relation_str_or_dict)
                self.relations.append(relation)
        #
        #
        # process ispartof/contents
        self.contents = []
        if 'contents' in datum and datum['contents'] is not None:
            for child_str_or_dict in datum['contents']:
                child = ContainsReference(child_str_or_dict)
                self.contents.append(child)
        #
        self.ispartofs = []
        if 'ispartof' in datum and datum['ispartof'] is not None:
            for parent_str_or_dict in datum['ispartof']:
                parent = IsPartOfReference(parent_str_or_dict)
                self.ispartofs.append(parent)
        #
        # TODO: handle __class__ --> kind
        # TODO: handle ccmms-specific ones: ccss_guid, ccss_url, asn_url



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
        #
        for prereq_rel in obj.prerequisites:
            all_path_refs.add(prereq_rel.prerequisite)
        for usedfor_rel in obj.usedfors:
            all_path_refs.add(usedfor_rel.usedfor)
        #
        for related_rel in obj.relations:
            all_path_refs.add(related_rel.related)
        #
        for contains_rel in obj.contents:
            all_path_refs.add(contains_rel.contains)
        for ispartof_rel in obj.ispartofs:
            all_path_refs.add(ispartof_rel.ispartof)
    return (all_paths, all_path_refs)


def create_nodes_and_relations(data_objects):
    """
    Creates the actual Node and Relations objects and saves them to the DB.
    """
    all_paths, all_path_refs = extact_paths(data_objects)

    # PASS 1. create nodes
    for obj in data_objects:
        node = BaseNode(
            path=obj.path,
            scope=obj.scope,
        )
        node.save()

    # PASS 2. create relations
    for obj in data_objects:
        node = BaseNode.objects.get(path=obj.path)

        # 2.1 prerequisites
        for prereq in obj.prerequisites:
            prereq_path = prereq.prerequisite
            if prereq_path in all_paths:
                prereq_node = BaseNode.objects.get(path=prereq_path)
                # both ends exist...
                # TODO: first check for existing  ######################################################################
                rel = DependencyRelation(
                        prerequisite=prereq_node,
                        usedfor=node,
                        explain_prerequisite=prereq.explain_prerequisite
                )
                if prereq.level is not None:
                    rel.level = prereq.level
                rel.save()
            else:
                pass
                # print('Skipping prerequisite relation {} --> {}'.format(obj.path, prereq_path))
                # TODO(handle missing referants better)
        # TODO: handle usdedfors  ######################################################################
        
        # 2.2 generic related links
        for related_rel in obj.relations:
            related_path = related_rel.related
            if related_path in all_paths:
                related_node = BaseNode.objects.get(path=related_path)
                # both ends exist...
                # TODO: first check for existing  ######################################################################
                level = related_rel.level or 'All'
                rel = RelatedRelation(
                        left=node,
                        right=related_node,
                        explain_related=related_rel.explain_related,
                        level=level,
                )
                rel.save()
                rel_backward = RelatedRelation(
                        left=related_node,
                        right=node,
                        explain_related=related_rel.explain_related,
                        level=level,
                )
                rel_backward.save()

        # 2.3 containment (a.k.a. topid-suptopic structure)
        for contains_rel in obj.contents:
            child_path = contains_rel.contains
            if child_path in all_paths:
                child_node = BaseNode.objects.get(path=child_path)
                # both ends exist...
                # TODO: first check for existing  ######################################################################
                rel = ContainmentRelation(
                        parent=node,
                        child=child_node,
                        explain_contains=contains_rel.explain_contains
                )
                if contains_rel.level is not None:
                    rel.level = contains_rel.level
                rel.save()
        # TODO: handle is part of  ######################################################################
