
try: import xmlrpclib as xmlrpc_client
except: import xmlrpc.client as xmlrpc_client

import pickle
import types

class MyProxy():

    class wrapper_():

        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            args = pickle.dumps(args)
            kwargs = pickle.dumps(kwargs)
            return pickle.loads(self.func(args, kwargs).data)

    def __init__(self, url='http://localhost:8000'):
        self.proxy = xmlrpc_client.ServerProxy(url)
        self.__override_methods__()

    def __override_methods__(self):

        for attr in self.proxy.system.listMethods():
            if attr.endswith('_'): continue
            if attr.startswith('system.'): continue
            m_attr = getattr(self.proxy, attr)
            setattr(self.proxy, attr+'_', m_attr)
            setattr(self, attr, MyProxy.wrapper_(m_attr))



if __name__ == '__main__':

    proxy = MyProxy()
    Address = proxy.SymLookupByName('nt!NtReadFile')
    print('nt!NtReadFile: %x' % (Address))
    Symbol = proxy.SymLookupByAddress(Address)
    print('%x: %s' % (Address, Symbol))