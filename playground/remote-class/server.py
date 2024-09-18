class MockServer:
    def __init__(self):
        self.instances = {}

    def register_instance(self, instance_id, instance):
        self.instances[instance_id] = instance
        print(f"[Server] Registered instance {instance_id}")

    def get_instance(self, instance_id):
        return self.instances.get(instance_id)

    def get_attribute(self, instance_id, attr_name):
        print(f"[Server] Get attribute '{attr_name}' of instance {instance_id}")
        instance = self.get_instance(instance_id)
        if instance:
            attr = getattr(instance, attr_name, None)
            if attr is not None:
                if callable(attr):
                    return ("ERROR", "Attribute is callable")
                else:
                    return attr
            else:
                return ("ERROR", "Attribute not found")
        else:
            return ("ERROR", "Instance not found")

    def handle_method_call(self, instance_id, method_name, args, kwargs):
        print(f"[Server] Handle method '{method_name}' call on instance {instance_id} with args {args} and kwargs {kwargs}")
        instance = self.get_instance(instance_id)
        if instance:
            method = getattr(instance, method_name, None)
            if method:
                try:
                    result = method(*args, **kwargs)
                    return result
                except Exception as e:
                    return ("ERROR", str(e))
            else:
                return ("ERROR", "Method not found")
        else:
            return ("ERROR", "Instance not found")

# Create a singleton server instance
mock_server = MockServer()