"""Classes to perform introspection on objects.
Created by: Tony Held tony.held@gmail.com
Created on: 8/13/20 """

from tony_util.misc import my_calling_statement, function_arguments, get_max_char
from tony_util.classes_examples import *
import pprint


class Inspector:
    """Routines to explore dir output to better understand magic variables and other namespace details."""

    def __init__(self):
        """Initialize inspector by resetting structures used
            to save previous search results."""
        self.clear_history()

    def clear_history(self):
        """Reset data saved from last inspection."""
        self.climb_history = {}    # Store inspections with object id as key
        self.children = {}         # Store parent child relationships among objects
        self.entry_id = 0          # Counter to retain order of dictionary insertions

    def __call__(self, *args, **kwargs):
        """Call climb_dir if Inspector is directly called."""
        self.climb_dir(*args, *kwargs)

    def climb_dir(self, obj, drilldown='__class__', max_output=-1, ignore_start=None):
        """Print the dir results for obj, recursively explore attributes
            of the attribute specified as drilldown.

        Parameters
        ----------
        obj : object
            obj to explore with dir
        drilldown : str
            name of dir attribute you wish to recursively explore.
        max_output : int
            Max number of characters of an attribute to print.
            -1 indicates that all characters will be used.
        ignore_start: str
            Filter to ignore attributes that start with a character string.
            Typical values include "_" or "__" to suppress magic methods.
        Notes
        -------
        """
        # Call dir & store the object name and class name
        obj_dir = dir(obj)
        obj_class_name = getattr(obj, '__class__').__name__
        obj_name = getattr(obj, '__name__', f'*Unnamed instance of {obj_class_name}*')

        # If the object has already been inspected then end recursion.
        # Otherwise, store the object id in the inspected object list
        if id(obj) in self.climb_history:
            return
        else:
            self.climb_history[id(obj)] = {'object name': obj_name, 'class name': obj_class_name}

        # Display the stack statement that resulted in this function call,
        # the object's name (if present), and the name of its class
        my_call = my_calling_statement()
        my_args = function_arguments(my_call)
        print(f"\n{'*'*80}")
        print(f'Directory climb called by: {my_call}')
        print(f"The class name of this object is: {obj_class_name}")
        print(f"The name of this object is: {obj_name}")
        print(f"The object id is: {id(obj)}")
        print(f"{'-'*80}")

        # Filter out unwanted variables that start with an unwanted string pattern
        if ignore_start:
            obj_dir = [i for i in obj_dir if not i.startswith(ignore_start)]

        # Display dir attribute names and the attributes values where possible.
        for item in obj_dir:
            if item == "__abstractmethods__":
                print(f"{item:20s} = ** Not evaluated, calls to __abstractmethods__ can result in exceptions **")
            else:
                attr = str(getattr(obj, item))
                if 0 < max_output < len(attr):
                    attr = get_max_char(attr, max_output)
                print(f"{item:20s} = {attr}")
        print(f"{'-' * 80}")

        # Evaluate the object attribute specified by the drilldown parameter.
        # getattr(obj, drilldown) results vary based on attribute of interest.
        # This inspector is designed to handle getattr results that are None, single item, a list, or tuple.

        # End recursion if there is no drilldown parameter
        if drilldown is None:
            return

        # Find the drilldown attribute
        matches = getattr(obj, drilldown, None)

        # If the attribute does not exist, then return and end recursion.
        if matches is None:
            return

        # Pack results attribute results into a 1-d list
        if type(matches) is tuple:
            matches = [*matches]
        if type(matches) is not list:
            matches = [matches]
        # print(f"Now inspecting: {matches}")

        # Evaluate each attribute in the 1-d list
        for match in matches:
            self.climb_dir(match, drilldown, max_output=max_output, ignore_start=ignore_start)

    def climb_bases(self, obj):
        """Climb the __bases__ special function to inspect inheritance structure.

        Parameters
        ----------
        obj :
            obj to explore recursively to inspect its __bases__ variable
        Notes
        -------
        """
        mcs = my_calling_statement()  # Inspect Stack to find the calling statement and its arguments
        my_obj_name = function_arguments(mcs)
        # print(mcs, my_obj_name)

        obj_class_name = getattr(obj, '__class__').__name__
        obj_name = getattr(obj, '__name__', f'*Unnamed instance of {obj_class_name}*')

        # print(f"class name: {obj_class_name}")
        # print(f"object name: {obj_name}")

        # print(dir(obj))
        # print(obj.__dict__)
        my_bases = getattr(obj, '__bases__', None)
        if my_bases is None:
            # You have an instance of an object, search its class type next
            my_bases = (obj.__class__,)
            obj_name = f"Instance {my_obj_name}"

        # print(f"my bases = {my_bases}")
        # Save the parent, child relationship in a dictionary, save entry order
        my_dict = {}
        my_dict[obj_name] = [i.__name__ for i in my_bases]
        self.children[self.entry_id] = my_dict
        self.entry_id += 1

        # Save the current object into a dictionary or exit if it has been examined before
        if id(obj) in self.climb_history:
            return
        else:
            self.climb_history[id(obj)] = \
                {'object name': obj_name, 'class name': obj_class_name, '__dict__': obj.__dict__}

        for i in my_bases:
            self.climb_bases(i)

    def test_climbs(self):
        """Test the climbDir function"""
        # not sure this block is going to be helpful in the future, but i learned a bit getting it this far
        # x = C()
        self.climb_dir(Super, '__class__', max_output=100)
        self.climb_dir(Sub, drilldown=None, max_output=100)

        # self.climb_dir(Super(), '__class__')
        # self.climb_dir(Sub, '__bases__')
        # self.climb_dir(Sub(), '__bases__')
        # self.climb_dir(x, '__class__')
        # self.climb_dir(x, '__subclasses__')
        # self.climb_dir(J, '__bases__')
        # x = Sub()
        # x.hola()
        # x.hello()
        # self.climb_bases(x)
        self.climb_bases(J())


if __name__ == "__main__":

    inspector = Inspector()
    inspector.test_climbs()

    if True:
        pass

    if False:

        a = inspector.climb_history
        b = inspector.children
        pp = pprint.PrettyPrinter(indent=3)
        # pp.pprint(a)
        pp.pprint(b)
        pp.pprint(J.__mro__)

