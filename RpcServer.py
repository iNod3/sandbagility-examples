
import types
import pickle
import inspect

from Sandbagility import Helper
from Sandbagility.Core import FDP

from xmlrpc.server import SimpleXMLRPCServer

class XmlRpcHelper(Helper):

    class wrapper_():

        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):

            caller = inspect.stack()[1][3]
            if caller == '_dispatch':

                pickled_args = args
                args = pickle.loads(bytes(pickled_args[0], encoding='latin1'))
                kwargs = pickle.loads(bytes(pickled_args[1], encoding='latin1'))
                return pickle.dumps(self.func(*args, **kwargs), protocol=2)
            else:
                return self.func(*args, **kwargs)

    def __init__(self):
        super().__init__("Windows 10 x64 - 14393", FDP)
        self.__override_methods__()

    def __override_methods__(self):

        for attr in dir(self):
            m_attr = getattr(self, attr)
            if type(m_attr) == types.MethodType:
                setattr(self, attr+'_', m_attr)
                setattr(self, attr, XmlRpcHelper.wrapper_(m_attr))

if __name__ == '__main__':

    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    print("Listening on port 8000...")
    server.register_introspection_functions()

    server.register_instance(XmlRpcHelper())
    server.serve_forever()