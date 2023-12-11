try:
    # AnsibleFilterTypeError was added in 2.10
    from ansible.errors import AnsibleFilterTypeError
except ImportError:
    from ansible.errors import AnsibleFilterError
    AnsibleFilterTypeError = AnsibleFilterError

from ansible.module_utils.common._collections_compat import Mapping
from ansible.plugins.filter.core import to_bool

TELEGRAF_PLUGIN_SECTIONS = (
    "input",
    "output",
    "aggregator",
    "processor",
)

def to_telegraf_plugin_filter_args(filter_map):
    if not isinstance(filter_map, Mapping):
        raise AnsibleFilterTypeError(
            "to_telegraf_plugin_filter_args requires a dict, got %s" % type(filter_map)
        )

    filter_args = []

    for section in TELEGRAF_PLUGIN_SECTIONS:
        values = ":".join(plugin for plugin, enabled in filter_map.get(section, {}).items() if to_bool(enabled))

        if values:
            filter_args.append(f"--{section}-filter {values}")

    return " ".join(filter_args)

class FilterModule(object):

    def filters(self):
        return {
            "to_telegraf_plugin_filter_args": to_telegraf_plugin_filter_args,
        }
