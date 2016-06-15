from django.utils import six
from django.db.models import sql


REPR_OUTPUT_SIZE = 20


# WIP!!!!!
class CustomQuerySet(object):
    """
    Represents a lazy database lookup for a set of objects.
    
    We perform data access manually to probe the minimum "quacks like a QuerySet" API
    needed to have a custom data acccess object (DAO).
    """
    
    def __init__(self, model=None, query=None, using=None, hints=None):
        print "hit __init__"
        self.model = model
        self._db = using
        self._hints = hints or {}
        self.query = query or sql.Query(self.model)
        self._result_cache = None
        self._sticky_filter = False
        self._for_write = False
        self._prefetch_related_lookups = []
        self._prefetch_done = False
        self._known_related_objects = {}  # {rel_field, {pk: rel_obj}}
        self._fields = None

    # def as_manager(cls):
    #     # Address the circular dependency between `Queryset` and `Manager`.
    #     from django.db.models.manager import Manager
    #     manager = Manager.from_queryset(cls)()
    #     manager._built_with_as_manager = True
    #     return manager
    # as_manager.queryset_only = True
    # as_manager = classmethod(as_manager)

    def __repr__(self):
        data = list(self)[:REPR_OUTPUT_SIZE + 1]
        if len(data) > REPR_OUTPUT_SIZE:
            data[-1] = "...(remaining elements truncated)..."
        return '<CustomQuerySet %r>' % data

    def __len__(self):
        self._fetch_all()
        return len(self._result_cache)

    def __iter__(self):
        """
        The queryset iterator protocol uses three nested iterators in the
        default case:
            1. sql.compiler:execute_sql()
               - Returns 100 rows at time (constants.GET_ITERATOR_CHUNK_SIZE)
                 using cursor.fetchmany(). This part is responsible for
                 doing some column masking, and returning the rows in chunks.
            2. sql/compiler.results_iter()
               - Returns one row at time. At this point the rows are still just
                 tuples. In some cases the return values are converted to
                 Python values at this location.
            3. self.iterator()
               - Responsible for turning the rows into model objects.
        """
        self._fetch_all()
        return iter(self._result_cache)

    def __getitem__(self, k):
        """
        Retrieves an item or slice from the set of results.
        """
        if not isinstance(k, (slice,) + six.integer_types):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."
    
        if self._result_cache is None:
            self._fetch_all()
        return self._result_cache[k]


    # def iterator(self):
    #     """
    #     An iterator over the results from applying this QuerySet to the database.
    #     """
    #     return iter(self)

    def count(self):
        if self._result_cache is None:
            self._fetch_all()
        return len(self._result_cache)

    def get(self, *args, **kwargs):
        """
        ASSUME ONLY ONE ARG0 given, and ARG0 is index into array...
        Performs the query and returns a single object matching the given
        keyword arguments.
        """
        print args
        print kwargs
        if self._result_cache is None:
            self._fetch_all()
        # UGLY HACK TO FIX LATER>>>>>>>>>>>>>>
        if kwargs.has_key('pk'):
            results = [ n for n in self._result_cache if str(n.id) == kwargs['pk'] ]
        elif kwargs.has_key('id'):
            results = [ n for n in self._result_cache if str(n.id) == str(kwargs['id']) ]
        else:
            print "BIG PROBLEM ..."
            raise self.model.DoesNotExist("No PK specified")
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<< /UGLY HACK TO FIX LATER
        num = len(results)
        if num == 1:
            return results[0]
        if not num:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name
            )
        raise self.model.MultipleObjectsReturned(
            "get() returned more than one %s -- it returned %s!" %
            (self.model._meta.object_name, num)
        )


    # def create(self, **kwargs):
    #     """
    #     Creates a new object with the given kwargs, saving it to the database
    #     and returning the created object.
    #     """
    #     obj = self.model(**kwargs)
    #     self._for_write = True
    #     obj.save(force_insert=True, using=self.db)
    #     return obj

    # def get_or_create(self, defaults=None, **kwargs):
    #     """
    #     Looks up an object with the given kwargs, creating one if necessary.
    #     Returns a tuple of (object, created), where created is a boolean
    #     specifying whether an object was created.
    #     """
    #     lookup, params = self._extract_model_params(defaults, **kwargs)
    #     # The get() needs to be targeted at the write database in order
    #     # to avoid potential transaction consistency problems.
    #     self._for_write = True
    #     try:
    #         return self.get(**lookup), False
    #     except self.model.DoesNotExist:
    #         return self._create_object_from_params(lookup, params)
    # 

    def first(self):
        """
        Returns the first object of a query, returns None if no match is found.
        """
        objects = list(self)[:1]
        if objects:
            return objects[0]
        return None

    def exists(self):
        if self._result_cache is None:
            self._fetch_all()
        return bool(self._result_cache)

    def _fetch_all(self):
        if self._result_cache is None:
            from .models import BaseNode
            toutte = list(BaseNode._objects_impl.all())
            for item in toutte:
                item.comment = "Touched by CustomQuerySet yo"
            self._result_cache = toutte
        # if self._prefetch_related_lookups and not self._prefetch_done:
        #     self._prefetch_related_objects()

    def all(self):
        """
        Returns a new QuerySet that is a copy of the current one. This allows a
        QuerySet to proxy for a model manager in some cases.
        """
        if self._result_cache is None:
            self._fetch_all()
        return self._result_cache




    ### ADDITIONAL METHODS REQUIRED FOR ADMIN VIEWS ############################

    def filter(self, *args, **kwargs):
        """
        Returns a new QuerySet instance with the args ANDed to the existing
        set.
        """
        # HACK!!!
        print "In filter..."
        print args
        print kwargs
        if self._result_cache is None:
            self._fetch_all()
        return self

    def order_by(self, *field_names):
        return self

    def _clone(self):
        return self
