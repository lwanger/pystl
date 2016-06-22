# pystl
Simple STL file class for Python

This is a very simple Python class to programmatically create STL files for 3D printing.

The easiest way to use this is with the context manager. Open the file, write triangles, and exit
the context block, the only parameter necessary is the file name.:

    with PySTL('stl_test.stl') as stl:
        stl.add_triangle( (0.0, 0.0, 0.5), (0.0, 1.0, 0.0), (1.0, 1.0, 0.5) )

For debugging you can use text-based STL files (by passing in False for the bin parameter).

To add geometry to the STL file, there are two methods:

def add_triangle(self, triangle, normal=None):
    """  Write a triamgle to the STL file
        :param triangle: a tuple of 3 vertices. Each being a tuple of 3 floats
        :param normal: a tuple of 3 floats for the normal
    """

The pystl class will automatically calculate the normal if none is given. Alternatively one can be passed in as a tuple of 3 floats.

def add_quad(self, v1, v2, v3, v4):
    """  Write a quadrilateral to the STL file
        :param triangle: a tuple of 4 vertices. Each being a tuple of 3 floats
    """

This is a convenience function that draws a quadrilateral as two triangles.


Len Wanger, 2016

        
