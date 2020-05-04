import weakref

def singleton(cls):
    """ decorator for a class to make a singleton out of it """
    classInstances = {}

    def getInstance(*args, **kwargs):
        """ creating or just return the one and only class instance.
            The singleton depends on the parameters used in __init__ """
        key = (cls, args, str(kwargs))
        if key not in classInstances or classInstances[key]() == None:
            classInstance = cls(*args, **kwargs)
            classInstances[key] = weakref.ref(classInstance)
        return classInstances[key]() or classInstance

    return getInstance
