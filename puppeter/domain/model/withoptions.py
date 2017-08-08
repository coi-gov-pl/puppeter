import collections
from abc import ABCMeta, abstractmethod

from six import with_metaclass, iteritems
from typing import Dict, Any


class WithOptions(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def raw_options(self):
        # type: () -> Dict[str, Any]
        pass

    @abstractmethod
    def read_raw_options(self, options):
        # type: (Dict[str, Any]) -> None
        pass

    @staticmethod
    def _update(orig_dict, new_dict):
        for key, val in iteritems(new_dict):
            if isinstance(val, collections.Mapping):
                tmp = WithOptions._update(orig_dict=orig_dict.get(key, {}), new_dict=val)
                orig_dict[key] = tmp
            elif isinstance(val, list):
                orig_dict[key] = (orig_dict.get(key, []) + val)
            else:
                orig_dict[key] = new_dict[key]
        return orig_dict
