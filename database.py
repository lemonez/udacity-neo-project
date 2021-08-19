"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

"""
import extract, database, importlib
cas_collection = extract.load_approaches()
neo_collection = extract.load_neos()
ndb = database.NEODatabase(neo_collection, cas_collection)
ca1 = cas_collection[1]
ca2 = cas_collection[2]
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self._neo_designation_cache = {}

        self._link_neos_to_approaches()

    def __str__(self):
        return f'An instance of {self.__class__.__name__}'

    def __repr__(self):
        return f'{self.__class__.__name__}(neos, approaches)'

# TODO: What additional auxiliary data structures will be useful?
    def _cache_neo_by_designation(self, designation, neo):
        # perhaps implement a cache here for NEOs already seen in the query
        self._neo_designation_cache[designation] = neo
        #print(f'\rcached: {neo.fullname}', end='', sep=' ', flush=True)

    def _link_neos_to_approaches(self):
        print("Building database: linking NEOs to close approaches...")
        for approach in self._approaches:
            neo = self.get_neo_by_designation(approach._designation)
            # assign the NEO to this approach
            approach.neo = neo
            # add this approach to the NEO's approach list
            neo.approaches.append(approach)
        print('\n')

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        if designation in self._neo_designation_cache.keys():
            return self._neo_designation_cache[designation]
        for neo in self._neos:
            if neo.designation.lower() == designation.lower():
                self._cache_neo_by_designation(designation, neo)
                return neo
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # handle None or empty string
        if not name:
            return None
        for neo in self._neos:
            try:
                if neo.name.lower() == name.lower():
                    return neo
            except AttributeError:
                continue
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.
        for approach in self._approaches:
            # run each approach through all filters
            for filter in filters:
                if not filter(approach):
                    # break out of nested for loop b/c must pass all filters
                    break
                yield approach
