'''
this is the file which makes other file in the folder to be imported into any other
program works as a package or a module now we dont need to have anything into this file ,still 
this will work

now here we are having this code which will ensure that what and how much thing we let the 
other program to fetch from this folder
'''

from utility.hash_util import hash_string_256

__all__ = ['hash_string_256']