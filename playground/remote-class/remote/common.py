from server import mock_server

class Proxy:
    def __init__(self, remote_id, class_name):
        self._remote_id = remote_id
        self._class_name = class_name

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"{self._class_name} object has no attribute {name}")
        # Handle attribute access via RPC
        attr = mock_server.get_attribute(self._remote_id, name)
        if isinstance(attr, tuple) and attr[0] == "ERROR":
            if attr[1] == "Attribute is callable":
                # Return a callable proxy method
                def method(*args, **kwargs):
                    print(f"[Proxy] RPC call: {self._class_name}.{name} on instance {self._remote_id}")
                    result = mock_server.handle_method_call(self._remote_id, name, args, kwargs)
                    if isinstance(result, tuple) and result[0] == "ERROR":
                        raise Exception(result[1])
                    return result
                return method
            else:
                raise Exception(attr[1])
        else:
            print(f"[Proxy] RPC get attribute: {self._class_name}.{name} on instance {self._remote_id}")
            return attr