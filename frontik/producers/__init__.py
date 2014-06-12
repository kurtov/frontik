# coding=utf-8


class Producers(object):
    JSON, XML, GENERIC = ('JSON', 'XML', 'GENERIC')


def create_logging_proxy(logger, obj):
    class _LoggingProxy(object):
        def __getattribute__(self, item):
            if not item.startswith('__'):
                logger.info('proxying unaccessible attribute "%s" in legacy mode %s', item, logger.findCaller())
            return obj.__class__.__getattribute__(obj, item)

    return _LoggingProxy()
