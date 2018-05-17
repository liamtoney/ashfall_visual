# Interactive visualization of ash deposition forecasts
![](demonstration.gif "Demonstration of interactive ash deposition map")

The spatial distribution, amount, and arrival time of deposited ash following a volcanic eruption are important parameters for hazard preparedness and mitigation. In New Zealand, [GNS Science](https://www.gns.cri.nz/) has collaborated with [MetService](http://www.metservice.com/national/home) to modify [HYSPLIT](https://ready.arl.noaa.gov/HYSPLIT.php) &mdash; an airborne ash dispersion modeling program &mdash; for ash deposition forecasting. This repository illustrates the variety of ashfall forecast products that can be produced from the model output.

## How to navigate this repository
Your first stop should be [`concept_portfolio.ipynb`](concept_portfolio.ipynb). This Jupyter notebook showcases and explains the three most fundamental interactive visualization products included in this repository:

* An ash deposition map
* An ash thickness time profile plotting tool
* A GIS / Google Earth data export utility

It also provides an overview of some key Python tools for geovisualization. To run (and edit!) cells within the notebook, you can launch an interactive version by following the badge link provided [below](#interactive-jupyter-notebooks).

The [`experiments/`](experiments) directory contains additional Jupyter notebooks which explore the "plotting tool space."

[`18042918_taupo_15.0_0.01.nc`](18042918_taupo_15.0_0.01.nc) is typical of the netCDF files output by the modified HYSPLIT program. This specific file describes the ashfall forecast for an eruption of the Taupō volcano on April 29th, 2018 at 18:00 NZST, with a plume height of 15 km and an erupted volume of 0.01 cubic km. The file is provided courtesy of MetService.

[`vis_tools.py`](vis_tools.py) contains several functions used within the Python code of the repository's notebooks.

## Interactive Jupyter notebooks
Click on the badge below to access a fully executable, editable version of this repository:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/liamtoney/ashfall_visual/master)

Note: If you see `Waiting for build to start...` at the top of the build logs, please be patient. Constructing the binder environment takes some time.

## Installation and dependencies
See [`environment.yml`](environment.yml) for a list of dependencies.

To create an environment with all of the dependencies installed (using [conda](https://conda.io/docs/)), run the following:
```
conda env create -f environment.yml
```
. . . then activate the environment:
```
source activate ashfall_visual
```
. . . and install a new IPython kernel to use with your Jupyter notebook:
```
pip install kernda --no-cache
python -m ipykernel install --name ashfall_visual
kernda -o -y /usr/local/share/jupyter/kernels/ashfall_visual/kernel.json
```
Note: The path to `kernel.json` may differ for your system.

## References
Chai, C., Ammon, C. J., Maceira, M., & Herrmann, R. B. (2018). Interactive visualization of complex seismic data and models using Bokeh. *Seismological Research Letters*, *89*(2A), 668–676. <https://doi.org/10.1785/0220170132>

Hurst, T., & Davis, C. (2017). Forecasting volcanic ash deposition using HYSPLIT. *Journal of Applied Volcanology*, *6*(1), 1-8. <https://doi.org/10.1186/s13617-017-0056-7>

Mastin, L. G., Randall, M. J., Schwaiger, H. F., & Denlinger, R. P. (2013). *User's guide and reference to Ash3d: A three-dimensional model for Eulerian atmospheric tephra transport and deposition* ([Open-File Report 2013-1122](https://pubs.usgs.gov/of/2013/1122/pdf/ofr20131122.pdf)). Reston, VA: U.S. Geological Survey.

</br>
<p align="center">
  <a href="https://www.gns.cri.nz">
    <img src="http://spacewardbound.astrobiology.kiwi/wp-content/uploads/2017/04/GNS_logo-1038x1709.png" height="70"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="http://www.metservice.com/national/home">
    <img src="http://m.metservice.com/sites/all/themes/mobile/images-new/hi/MetService-hammerhead-logo.svg" height="40"></a>
</p>