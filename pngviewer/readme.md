## Cinema:JNC repository

A prototype jupyter notebook with components to run a simple viewer for a single Cinema database.  Currently only takes PNG image files as the data artifacts.

# Requirements

- python 3, jupyter installed
- assumes user is familiar with jupyter notebooks

# Usage

Load the local module, then create a cinema viewer.

```
load cinema

cinema.pynb.loadCinemaViewer('paths to cdb folders')
```

## Getting Started

- Clone the repository
- Open jupyter

```
$ jupyter notebook
```

- Select the **cinema_module.ipynb** file
- Input full path to Cinema database when requested

## Multiple Databases (Cinema Compare)

- This framework can load multiple databases for side by side comparison
- In the **path** bar, enter the path to as many databases as desired, each path seperated by a space 

Contact `cinema-info@lanl.gov` for more information.
