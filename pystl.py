"""
PySTL - a simple package to write STL files


The easiest way to use this is with the context manager. Open the file, write triangles, and exit
the context block:

    with PySTL('stl_test.stl') as stl:
        stl.add_triangle( (0.0, 0.0, 0.5), (0.0, 1.0, 0.0), (1.0, 1.0, 0.5) )

For debugging you can use text-based STL files (by passing in False for the bin parameter).

Len Wanger
last updated: 02-15-2016
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

"""

import math
import struct

class PySTL(object):
    def __init__(self, file_name, bin=True, model_name=''):
        self.f = None
        self.model_name = model_name
        self.file_name = file_name
        self.is_bin = bin
        self.num_triangles = 0
        self.trailer_written = False


    def open(self):
        file_mode = 'wb' if self.is_bin else 'w'
        self.f = open(self.file_name, file_mode)


    def close(self):
        self.f.close()
        self.f = None


    def __enter__(self):
        self.open()
        self.write_stl_header()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.trailer_written:
            self.write_stl_trailer()
        self.close()


    def write_stl_header(self):
        if self.is_bin:
            header_str = ''
            self.f.write(struct.pack("80s", header_str.encode()))
            self.write_num_triangles_bin()
        else:
            self.f.write('solid ' + self.model_name + '\n' )


    def write_num_triangles_bin(self, write_num_triangles=False):
        if self.is_bin:
            if write_num_triangles:
                self.f.seek(80)
                self.f.write(struct.pack("I", self.num_triangles))
            else:
                self.f.write(struct.pack("I", 0))
        else:
            raise RuntimeError('Cannot call write_num_triangles_bin on a text STL file.')


    def write_stl_trailer(self):
        if self.is_bin:
            self.write_num_triangles_bin(True)
        else:
            # No trailer on binary STL files
            self.f.write('endsolid \n' )


    def add_triangle(self, triangle, normal=None):
        """  Write a triamgle to the STL file
        :param triangle: a tuple of 3 vertices. Each being a tuple of 3 floats
        :param normal: a tuple of 3 floats for the normal
        """
        if not normal:
            normal = self.calc_normal(triangle)

        if self.is_bin:
            """ Each triangle is 4 sets of 3 floats - normal, three vertices, then a byte count
	    (which can be used for color)"""


            data = [ normal[0], normal[1], normal[2],
                     triangle[0][0], triangle[0][1], triangle[0][2],
                     triangle[1][0], triangle[1][1], triangle[1][2],
                     triangle[2][0], triangle[2][1], triangle[2][2],
                     0 ]
            self.f.write(struct.pack("12fH", *data))
            self.num_triangles += 1
        else:
            self.f.write('  facet normal {:.3f} {:.3f} {:.3f}\n'.format(normal[0], normal[1], normal[2]) )
            self.f.write('    outer loop\n' )
            self.f.write('      vertex {:.3f} {:.3f} {:.3f}\n'.format(triangle[0][0], triangle[0][1], triangle[0][2]))
            self.f.write('      vertex {:.3f} {:.3f} {:.3f}\n'.format(triangle[1][0], triangle[1][1], triangle[1][2]))
            self.f.write('      vertex {:.3f} {:.3f} {:.3f}\n'.format(triangle[2][0], triangle[2][1], triangle[2][2]))
            self.f.write('    endloop\n' )
            self.f.write('  endfacet \n')


    def add_quad(self, v1, v2, v3, v4):
        """  Write a quadrilateral to the STL file
        :param triangle: a tuple of 4 vertices. Each being a tuple of 3 floats
        """
        self.add_triangle((v1, v2, v4))
        self.add_triangle((v2, v3, v4))
        self.add_triangle((v1, v3, v4))

    def add_cuboid(stl, x, y, z, w, l, h):
        """  Write a cuboid at the point (x, y, z) extending in the positive
             direction with the given width, length and height (w, l, h).
        :param x: the x coordinate
        :param y: the y coordinate
        :param z: the z coordinate
        :param w: the width in the x-axis
        :param l: the length in the y-axis
        :param h: the height in the z-axis
        """
        for dz in (z, z+h):
            # top and bottom faces
            stl.add_quad((x, y, dz), (x+w, y, dz), (x, y+l, dz), (x+w, y+l, dz))
        for dx in (x, x+w):
            # left and right faces
            stl.add_quad((dx, y, z), (dx, y, z+h), (dx, y+l, z), (dx, y+l, z+h))
        for dy in (y, y+l):
            # front and back faces
            stl.add_quad((x, dy, z), (x, dy, z+h), (x+w, dy, z), (x+w, dy, z+h))

    def length_vector(self, v):
        """ Return the length of a vector """
        return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)


    def unit_vector(self, v):
        """ return the unit vector for a vector """
        l = self.length_vector(v)
        #return (v[0] / l, v[1] / l, v[2] / l)
        try:
            return (v[0] / l, v[1] / l, v[2] / l)
        except RuntimeWarning as e:
            pass

    def calc_normal(self, t):
        """ Return the normal for a triangle. Make sure it's a unit vector """
        # U = pt2 - pt1
        # V = pt3 - pt1
        # nx = UyVz - UzVy
        # ny = UzVx - UxVz
        # nz = UxVy - UyVx
        u = (t[1][0] - t[0][0], t[1][1] - t[0][1], t[1][2] - t[0][2])
        v = (t[2][0] - t[0][0], t[2][1] - t[0][1], t[2][2] - t[0][2])

        nx = u[1]*v[2] - u[2]*v[1]
        ny = u[2]*v[0] - u[0]*v[2]
        nz = u[0]*v[1] - u[1]*v[0]
        return self.unit_vector((nx, ny, nz))


if __name__ == '__main__':
    stl_name = 'bin_stl_test.stl'
    v1 = (0.0, 0.0, 0.5)
    v2 = (0.0, 1.0, 0.0)
    v3 = (1.0, 1.0, 0.5)
    v4 = (1.0, 0.0, 0.0)
    t1 = (v1,v2,v4)
    t2 = (v2,v3,v4)

    with PySTL('stl_test_bin.stl',  bin=True) as stl:
        stl.add_triangle(t1)
        stl.add_triangle(t2)

    with PySTL('stl_test_txt.stl',  bin=False) as stl:
        stl.add_triangle(t1)
        stl.add_triangle(t2)
