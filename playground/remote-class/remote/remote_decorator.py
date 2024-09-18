import uuid

from remote.common import Proxy
from server import mock_server

def remote_class(cls):
    original_new = cls.__new__

    def new_new(cls_, *args, **kwargs):
        instance = original_new(cls_)
        instance._remote_id = f"{cls_.__name__}_{str(uuid.uuid4())}"
        mock_server.register_instance(instance._remote_id, instance)
        cls_.__init__(instance, *args, **kwargs)
        proxy = Proxy(instance._remote_id, cls_.__name__)
        return proxy

    cls.__new__ = staticmethod(new_new)
    return cls