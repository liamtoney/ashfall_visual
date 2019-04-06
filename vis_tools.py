# Module containing various ashfall visualization utility functions.

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import xesmf as xe
import cartopy.crs as ccrs
import cartopy.feature as cf
import colorcet as cc

def read_hysplit_netcdf(filename, lower_limit=0.0):
    """Reads a HYSPLIT netCDF file.

    Reads the netCDF file, crops the model, adds an "empty grid" time step at t=0,
    and adds in volcano location info.

    Args:
        filename: A string specifying the path/filename for the netCDF file.
        lower_limit: (Optional) A float specifying the value to use for cropping.
                     Model cells with a value at or below this value will be
                     made NaN. Default is 0.0 (include everything).

    Returns:
        model: An xarray.Dataset containing all of the processed netCDF info.
    """

    model = xr.open_dataset(filename)

    model = model.isel(lon=slice(-1))  # remove all model grid points with longitude = 180.0 degrees

    final_deposition = model.isel(time=-1)['total_deposition'].values  # the "final" ash distribution
    coords = np.argwhere(final_deposition > lower_limit)
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    model = model.isel(lon=slice(x_min, x_max+1), lat=slice(y_min, y_max+1))  # crop model

    np.place(model['total_deposition'].values, model['total_deposition'].values <= lower_limit, np.nan)

    # add in an extra, empty time step at t=0
    model = xr.concat((model.isel(time=0), model), dim='time')
    model.isel(time=0)['total_deposition'].values.fill(np.nan)
    model['time'].values[0] = np.datetime64(model.attrs['eruption_time'])

    # taken from ASHFALL model output files (converted from NZMG to WGS84)
    src_locs = {'auckland':[-36.8882, 174.7352],\
                'mayor':[-37.2852, 176.2562],\
                'white':[-37.5192, 177.1832],\
                'haroharo':[-38.1452, 176.4662],\
                'tarawera':[-38.2252, 176.5062],\
                'taupo':[-38.8072, 175.9782],\
                'tongariro':[-39.1062, 175.6732],\
                'ngauruhoe':[-39.1552, 175.6322],\
                'ruapehu':[-39.2816, 175.5639],\
                'taranaki':[-39.2952, 174.0642]}
    volc_name = filename.split('/')[-1].split('_')[1]
    model.attrs['volcano_location'] = src_locs[volc_name]

    model.attrs['ash_thickness_units'] = 'mm'

    return model

def grab_gshhg_features(scale, levels, extent):
    """Grabs lat/lon coordinates for GSHHG features.

    Grab geographical feature data from the GSHHG database for a specified extent,
    level of detail, and resolution. Outputs simple lat/lon coordinates -- useful
    for plotting backends (like Bokeh) that don't have fancy geo feature integration.

    Args:
        scale: A string, can be either f(ull), h(igh), i(ntermediate), l(ow), or c(rap)
               depending upon the desired resolution.
        levels: Specify which level(s) of feature to plot; [1] is only coastlines
                and [1, 2, 3, 4] is everything.
        extent: Specify [lonmin, lonmax, latmin, latmax] in decimal degrees.

    Returns:
        features: A dictionary containing coordinates of geo features
                  (WGS84 lat/lon, decimal degrees).
    """

    unformatted_features = list(cf.GSHHSFeature(scale=scale, levels=levels).intersecting_geometries(extent))

    features = {'latitude':[], 'longitude':[]}
    for feature in unformatted_features:
        lons = list(list(feature)[0].exterior.coords.xy[0])
        lats = list(list(feature)[0].exterior.coords.xy[1])
        features['longitude'].append(lons)
        features['latitude'].append(lats)

    return features

def grab_contour_info(X, Y, Z, V):
    """Extracts vertices of contour lines created by matplotlib's contour function.

    Modified from:
    <https://stackoverflow.com/questions/33533047/how-to-make-a-contour-plot-in-python-using-bokeh-or-other-libs>

    Args:
        Identical to those specified here:
        <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contour.html>

    Returns:
        x_all, y_all: Lists of lists of vertices for the x and y coordinates. Sublists
                      correspond to individual paths.
    """

    contour_info = plt.contour(X, Y, Z, V)
    plt.close()

    x_all = []
    y_all = []
    for iso_level in contour_info.collections:
        for path in iso_level.get_paths():
            vertices = path.vertices
            x = vertices[:, 0]
            y = vertices[:, 1]
            x_all.append(x.tolist())
            y_all.append(y.tolist())

    return x_all, y_all

def show_regridding_effects(fname, csz, alg='bilinear'):
    """Displays the effects of regridding a model.

    Plots a side-by-side comparison of the original model and the regridded model,
    using a high-contrast colormap for easy identification of discrepancies.

    Args:
        fname: Filename string, including path.
        csz: Desired output cell size in degrees (cell square side length).
        alg: Regridding algorithim. This function has only been tested with 'bilinear'
             (see <http://xesmf.readthedocs.io/en/latest/Compare_algorithms.html>
             for more info).
    """

    model = read_hysplit_netcdf(fname)
    new_grid = xr.Dataset({'lat': (['lat'], np.arange(np.min(model['lat']), np.max(model['lat']), csz)),
                           'lon': (['lon'], np.arange(np.min(model['lon']), np.max(model['lon']), csz))
                          })
    regridder = xe.Regridder(model, new_grid, alg)
    td_regrid = regridder(model['total_deposition'].transpose('time', 'lat', 'lon'))
    regridder.clean_weight_file()

    proj = ccrs.epsg(2193)
    params = dict(vmin=-5, vmax=0, cmap=cc.m_rainbow, transform=ccrs.PlateCarree(), add_colorbar=False)
    coast_res = '10m'
    ts = -1

    plt.figure(figsize=(16, 6))

    ax1 = plt.subplot(121, projection=proj)
    model['total_deposition'] = np.log10(model['total_deposition'])
    model['total_deposition'].isel(time=ts).plot.pcolormesh(ax=ax1, **params)
    ax1.coastlines(resolution=coast_res)
    plt.title('original')

    ax2 = plt.subplot(122, projection=proj)
    td_regrid = np.log10(td_regrid)
    td_regrid.isel(time=ts).plot.pcolormesh(ax=ax2, **params)
    ax2.coastlines(resolution=coast_res)
    plt.title('regridded')

    plt.show()
