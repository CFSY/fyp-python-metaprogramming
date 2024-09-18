# Remote class

A simple framework that simulates a distributed environment where objects can interact with each other via remote procedure calls (RPC). Metaprogramming abstracts away the complexities of distributed computing, allowing users to write code as if all objects are local.

## File Structure

1. **`server.py`**: Implements the `MockServer` class, which registers instances and handles method calls and attribute accesses
2. **`remote`**: Contains the implementation of three different approaches:
   - **Approach 1**: Base Class Inheritance (`RemoteObject`)
   - **Approach 2**: Decorator (`@remote_class`)
   - **Approach 3**: Metaclass (`RemoteMetaclass`)
3. **`main.py`**: Demo

## Overview

This demo is designed to simulate a distributed system where objects can be instantiated on different nodes. Interactions between these objects are handled via RPC through a centralized server (`MockServer`). There are three provided ways to mark objects as remote, the results are equivalent:

1. **Base Class Inheritance**: Users inherit from a `RemoteObject` class.
2. **Decorator**: Users decorate their classes with `@remote_class`.
3. **Metaclass**: Users set a custom metaclass (`RemoteMetaclass`) for their classes.

## Core Components

### 1. MockServer

The `MockServer` class acts as a centralized registry and handler for all remote objects. It includes:

- **Instance Registration**: When a remote object is created, it's registered with the server.
- **Method Call Handling**: When an RPC call is made, the server executes the method on the appropriate instance.
- **Attribute Access**: Retrieves attributes of remote objects.

### 2. RemoteObject / Decorator / Metaclass

- **RemoteObject (Base Class)**: Users inherit from this class to make their objects remote.
- **Decorator (`@remote_class`)**: Users decorate their classes to make them remote.
- **RemoteMetaclass**: Users set this as the metaclass for their classes to make them remote.
- Each approach registers the instance with the `MockServer` and returns a `Proxy` object instead of the actual instance.

### 3. Proxy

The `Proxy` class stands in for the actual remote instance. It intercepts attribute access and method calls, forwarding them to the `MockServer` to simulate RPCs.

## How It Works

### 1. Instance Creation

- When a remote class (using any of the three approaches) is instantiated:
  - A unique identifier is assigned to the instance.
  - The instance is registered with the `MockServer`.
  - Instead of returning the actual instance, a `Proxy` object is returned.

### 2. Attribute Access and Method Calls

- When the user accesses an attribute or calls a method on the proxy:
  - The proxy intercepts it via the `__getattr__` method.
  - If the attribute is a method, the proxy sends an RPC call to the server to execute the method on the actual instance.
  - The server handles the call and returns the result to the proxy, which then returns it to the user.

### 3. Interactions Between Remote Classes

- Remote objects can interact with each other via their proxies.
- For example, a `Restaurant` can call methods on a `Supplier` proxy.
- These interactions are routed through the server, simulating remote communication.

## How to Test the Different Implementations

The **`main.py`** file contains a demo. To test the different approaches, simply uncomment the method you want to try.

## Comparison of Approaches

| Aspect              | Base Class Inheritance                   | Decorator                           | Metaclass                         |
|---------------------|-------------------------------------------|-------------------------------------|-----------------------------------|
| **Ease of Use**     | Users inherit from `RemoteObject`.       | Users use `@remote_class` decorator.| Users set `metaclass=RemoteMetaclass`. |
| **Flexibility**     | Straightforward and explicit.            | Non-intrusive to class definitions. | Powerful but can conflict with other metaclasses. |
| **Remarks**         | - Requires inheritance, limiting flexibility if another base class is already in use. | - Clean syntax. Does not affect inheritance. <br> - Users need to remember to apply the decorator. | - Advanced and potentially confusing for some developers. <br> - Python classes can only have one metaclass. |
