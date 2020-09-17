"""Classes to perform introspection on objects.
Created by: Tony Held tony.held@gmail.com
Created on: 8/13/20 """

from tony_util.misc import my_calling_statement, function_arguments
from tony_util.classes_examples import *
import pprint


class Inspector:
    """Routines to explore magic variables, dir, and other namespace details."""

    def __init__(self):
        """Initialize inspector to allow recursive searches to save results in common variables to avoid repeat calls"""
        self.climb_history = {}    # Store inspections with object id as key
        self.children = {}         # Store parent child relationships among objects
        self.entry_id = 0          # Counter to retain order of dictionary insertions

    def clear_history(self):
        """Reset data saved from last inspection."""
        self.climb_history = {}
        self.children = {}
        self.entry_id = 0

    def __call__(self, *args, **kwargs):
        """call climb_dir if no function is specified"""
        self.climb_dir(*args, *kwargs)

    def climb_dir(self, obj, drilldown='__class__'):
        """Print the dir results for obj, recursively explore attributes of the attribute specified as drilldown.
        Parameters
        ----------
        obj :
            obj to explore recursively with dir
        drilldown : str
            name of dir attribute you wish to recursively explore.
        Notes
        -------"""

        # Call dir & store the object name and class name
        obj_dir = dir(obj)
        obj_class_name = getattr(obj, '__class__').__name__
        obj_name = getattr(obj, '__name__', f'*Unnamed instance of {obj_class_name}*')

        # If the object has already been inspected then end recursion
        # Otherwise store the object id in the inspected object list
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

        # Display dir attribute names and the attributes values where possible.
        for item in obj_dir:
            if item != "__abstractmethods__":
                print(f"{item:20s} = {getattr(obj, item)}")
            else:
                print(f"{item:20s} = ** Not evaluated, calls to __abstractmethods__ can result in exceptions **")
        print(f"{'-' * 80}")

        # Evaluate the object specified by the drilldown string through recursion
        # getattr(obj, drilldown) results vary based on attribute of interest
        # This inspector is designed to handle getattr results that are None, single item, a list, or tuple


        if drilldown is None: return    # End recursion if there is no drilldown

        # If it is None, then return, otherwise pack results into a 1-d list
        matches = getattr(obj, drilldown, None)
        # print(f"matches = {matches}")
        if matches is None: return    # End recursion

        if type(matches) is tuple:
            matches = [*matches]
        if type(matches) is not list:
            matches = [matches]
        # print(f"Now inspecting: {matches}")

        # Evaluate the objects matches list recursively
        for match in matches:
            self.climb_dir(match, drilldown)

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
        # self.climb_dir(Super, '__class__')
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
        a = inspector.climb_history
        b = inspector.children
        pp = pprint.PrettyPrinter(indent=3)
        # pp.pprint(a)
        pp.pprint(b)
        pp.pprint(J.__mro__)

