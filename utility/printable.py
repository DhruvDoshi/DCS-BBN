'''
This is the file in which we are just returning the dictionary format of any thing which is 
coverd into this function or we can say this object
'''



class Printable:
    """A base class which implements printing functionality."""
    def __repr__(self):
        return str(self.__dict__)
