from functools import partial


class Arg(object):
    __slots__ = ('param_type', 'default', 'choice', 'default_on_exception')

    _PARAM_DEFAULT = []

    def __init__(self, param_type, default=_PARAM_DEFAULT, choice=None, default_on_exception=False):
        if default_on_exception and not self.has_default:
            raise ValueError('default_on_exception = True, but no default value')

        if isinstance(param_type, list) and not param_type:
            raise ValueError('list argument must specify the type of its items')

        self.param_type = param_type
        self.default = default
        self.choice = choice
        self.default_on_exception = default_on_exception

    @property
    def has_default(self):
        return self.default is not self._PARAM_DEFAULT


def get_parser(param_type):
    if isinstance(param_type, list):
        return partial(list_parser, get_parser(param_type[0]))
    return _ARG_PARSERS[param_type]


def list_parser(item_parser, values):
    return [item_parser(x) for x in values]


def str_parser(value):
    return value


def int_parser(value):
    return int(value)


def float_parser(value):
    return float(value)


def bool_parser(value):
    return value.lower() == 'true'


_ARG_PARSERS = {
    str: str_parser,
    int: int_parser,
    float: float_parser,
    bool: bool_parser
}
