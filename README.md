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
Copyright (c) 2016 Len Wanger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
        
