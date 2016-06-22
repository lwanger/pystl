# pystl
Simple STL file class for Python

This is a very simple Python class to programmatically create STL files for 3D printing.

The easiest way to use this is with the context manager. Open the file, write triangles, and exit
the context block:

    with PySTL('stl_test.stl') as stl:
        stl.add_triangle( (0.0, 0.0, 0.5), (0.0, 1.0, 0.0), (1.0, 1.0, 0.5) )

def add_triangle(self, triangle, normal=None):
        """  Write a triamgle to the STL file
        :param triangle: a tuple of 3 vertices. Each being a tuple of 3 floats
        :param normal: a tuple of 3 floats for the normal
        """

def add_quad(self, v1, v2, v3, v4):

For debugging you can use text-based STL files (by passing in False for the bin parameter).
