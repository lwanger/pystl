# pystl
Simple STL file class for Python


The easiest way to use this is with the context manager. Open the file, write triangles, and exit
the context block:

    with PySTL('stl_test.stl') as stl:
        stl.add_triangle( (0.0, 0.0, 0.5), (0.0, 1.0, 0.0), (1.0, 1.0, 0.5) )

For debugging you can use text-based STL files (by passing in False for the bin parameter).
