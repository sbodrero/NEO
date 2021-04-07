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
import copy


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
        neos = list(neos)  # to be sortable
        approaches = list(approaches)  # to be sortable

        # sort by designation desc to make query faster
        neos.sort(key=lambda x: x.designation)
        approaches.sort(key=lambda x: x.designation)

        self._neos = neos
        self._approaches = approaches

        i = 0
        j = 0

        while i < len(self.neos) and j < len(self.approaches):
            neo = self.neos[i]
            approach = self.approaches[j]
            if neo.designation == approach.designation:
                neo.approaches.append(approach)
                approach.neo = neo
                j += 1
            else:
                i += 1

        # pre compute get_neo_by_name
        neos_by_name = copy.deepcopy(self.neos)
        self._neos_by_name = sorted(neos_by_name, key=lambda x: x.name or '')

        # pre compute get_neo_by_designation
        neos_by_designation = copy.deepcopy(self.neos)
        neos_by_designation.sort(key=lambda x: x.designation)
        self._neos_by_designation = neos_by_designation

    @property
    def neos(self):
        return self._neos

    @property
    def approaches(self):
        return self._approaches

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation,
        or `None`.
        """
        filtered_neo = list(filter(
            lambda neo: neo.designation == designation
            or neo.designation == designation.lower()
            or neo.designation == designation.upper(),
            self._neos_by_designation
        ))
        return filtered_neo[0] if filtered_neo else None

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
        filtered_neo = list(filter(
            lambda neo: neo.name == name
            or neo.name == name.lower()
            or neo.name == name.upper(),
            self._neos_by_name
        ))
        return filtered_neo[0] if filtered_neo else None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection
        of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified
        criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self.approaches:
            if filters:
                for item in filters:
                    if item(approach):
                        if filters.index(item) + 1 == len(filters):
                            yield approach
                    else:
                        break
            else:
                yield approach
