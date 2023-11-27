class NumPyBackend:
    __ua_domain__: str
    @staticmethod
    def __ua_function__(method, args, kwargs): ...

class EchoBackend:
    __ua_domain__: str
    @staticmethod
    def __ua_function__(method, args, kwargs) -> None: ...
