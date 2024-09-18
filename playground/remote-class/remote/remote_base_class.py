import uuid

from remote.common import Proxy
from server import mock_server

class RemoteObject:
    def __new__(cls, *args, **kwargs):
        # Create the actual instance
        instance = super().__new__(cls)
        # Assign a unique ID
        instance._remote_id = f"{cls.__name__}_{str(uuid.uuid4())}"
        # Register with the server
        mock_server.register_instance(instance._remote_id, instance)
        # Initialize the instance
        instance.__init__(*args, **kwargs)
        # Return a Proxy instead
        proxy = Proxy(instance._remote_id, cls.__name__)
        return proxy