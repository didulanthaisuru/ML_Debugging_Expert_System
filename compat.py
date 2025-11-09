"""
Compatibility shims for older packages that reference collections.Mapping
which was moved to collections.abc in newer Python versions.

This module should be imported before packages that import `collections.Mapping`
to avoid AttributeError on Python 3.10+ / 3.11+ / 3.14.
"""
import collections
import collections.abc as collections_abc

# Provide backwards-compatible aliases if they're missing
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections_abc.Mapping
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections_abc.MutableMapping
if not hasattr(collections, "Iterable"):
    collections.Iterable = collections_abc.Iterable
if not hasattr(collections, "Sequence"):
    collections.Sequence = collections_abc.Sequence
