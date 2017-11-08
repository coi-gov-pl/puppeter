import collections

from six import iteritems
from typing import Sequence, Tuple

from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer, ScriptFormat
from puppeter.domain.model.installer import PuppetConf
from puppeter.domain.model.ordered import Order


@Named('puppet.conf')
@Order(900)
class PuppetConfConfigurer(Configurer):

    def __init__(self, installer):
        self.__puppetconf = installer.puppetconf()  # type: PuppetConf

    def produce_commands(self):
        # type: () -> Sequence[str]
        collector = self._collector()
        augeas = self.__puppetconf_as_augeas()
        augeas_pp = ',\n    '.join(list(map(lambda cmd: '"{cmd}"'.format(cmd=cmd), augeas)))
        collector.collect_from_template(
            description="Configuring Puppet configuration file (puppet.conf)",
            format=ScriptFormat.PUPPET,
            template='puppetconf.pp',
            mapping={
                'settings': augeas_pp
            }
        )
        return collector.lines()

    def __puppetconf_as_augeas(self):
        # type: () -> Sequence[str]
        flat = self.__flatten(self.__puppetconf)
        return list(map(PuppetConfConfigurer.__augeaize, iteritems(flat)))

    @staticmethod
    def __augeaize(tup):
        # type: (Tuple[str, str]) -> str
        key, value = tup
        try:
            safe = {
                str: lambda x: "'{str}'".format(str=x),
                bool: lambda x: 'true' if x else 'false',
            }[value.__class__](value)
        except KeyError:
            safe = value
        return "set {key} {value}".format(key=key, value=safe)

    @staticmethod
    def __flatten(d, parent_key='', sep='/'):
        items = []
        for k, v in iteritems(d):
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(PuppetConfConfigurer.__flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
