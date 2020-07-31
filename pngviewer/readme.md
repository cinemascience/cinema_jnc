## CinemaViewer Jupyter notebook component

A Jupyter notebook with components to run a simple viewer for one or more Cinema databases.  Designed for the use case of fully populated cinema databases of common format images. 

# Requirements

- python 3
- jupyter

# Usage

Run Jupyter and select the **cinema_module.ipynb** file

```
$ jupyter notebook
```

Looking at the python code, you load the `cinemasci` module, then create a cinema viewer.

```
import cinemasci

# create a viewer object
viewer = cinemasci.pynb.CinemaViewer()
# optionally set the layout of the viewer
viewer.setLayoutToHorizontal()
# optionally set the height of the viewer
viewer.setHeight(250)
# load one or more cinema databases
viewer.load("data/sphere.cdb data/sphere_01.cdb")
```

Contact `cinema-info@lanl.gov` for more information.
