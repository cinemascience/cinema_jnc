## CinemaViewer Jupyter notebook component

A Jupyter notebook with components to run a simple viewer for one or more Cinema databases.  Designed for the use case of populated, cinema databases of common format images. 

# Requirements

- python 3
- jupyter installed

# Usage

Run Jupyter and select the **cinema_module.ipynb** file

```
$ jupyter notebook
```

Load the `cinesci` module, then create a cinema viewer.

```
load cinesci

viewer = cinesci.pynb.CinemaViewer()
# optionally set layout to verical or horizontal
viewer.setLayoutToVertical()
# optionally set height
viewer.setHeight(250)
# load one or more databases in a single space-separated string
viewer.load("/path/to/cinema/database /path/to/another/cinema/database")
```

Contact `cinema-info@lanl.gov` for more information.
