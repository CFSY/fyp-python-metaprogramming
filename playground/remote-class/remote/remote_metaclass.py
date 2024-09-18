import uuid

from remote.common import Proxy
from server import mock_server

class RemoteMetaclass(type):
    def __call__(cls, *args, **kwargs):
        instance = super(RemoteMetaclass, cls).__call__(*args, **kwargs)
        instance._remote_id = f"{cls.__name__}_{str(uuid.uuid4())}"
        mock_server.register_instance(instance._remote_id, instance)
        proxy = Proxy(instance._remote_id, cls.__name__)
        return proxy
