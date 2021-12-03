# Connectivity

This repository contains code to analyze topographical maps of landscape for hydrological connectivity. 
* LEM_info: 
    * csv files with persistence homology diagrams for each timestep of [LEM data](https://databank.illinois.edu/datasets/IDB-1558455). Columns are timestep T-10. 
    * Also contains wasserstein distance data for each timeseries from timeseries S1 (wass_data_LEM_dist_to_S1.csv).
    * raw_data includes raw LEM data (elevation) for images used in figures


Additional data related to this publication can be found at:
* [Landscape evolution data](https://databank.illinois.edu/datasets/IDB-1558455), from Kwang et al., 2021
* [Scale model data](https://github.com/lapidesd/connectivity_topology/tree/main/scale_model_LEM), from [Li et al., 2020](https://www.sciencedirect.com/science/article/pii/S0167198719303435)

Supporting code for this project can be found at:
* [Colab notebook applying persistence homology to synthetic examples](https://colab.research.google.com/drive/1MCGMS5ecnnBBprYOyYtvnYafL9CgMKIW?authuser=1#scrollTo=LO_RmXiVjEZF)
* [Colab notebook applying persistence homology to rainfall simulator plot experiments](https://colab.research.google.com/drive/1KYyP1tGfe4L5_v9f1sxnFxeazSRqpia_?usp=sharing)
* [Colab notebook applying persistence homology to landscape evolution (LEM) data](https://colab.research.google.com/drive/1_0ny60WW4e_ZVxhM2tnav_LGiv65WBGI?usp=sharing)
