import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.ndimage.morphology import distance_transform_edt
from scipy.stats import linregress


PIX_AREA = 0.0148   # the area of 1 pixel in microns


def get_myo_around(idx, tf, n=70):
    # get myosin concentration around a cell
    no_cell_mask = segmentation[tf] != idx
    dist_tr = distance_transform_edt(no_cell_mask)
    mask_around = (dist_tr <= n) * no_cell_mask
    myo_around = myosin[tf] * mask_around
    return np.sum(myo_around) / np.sum(mask_around) * PIX_AREA


def get_myo_in(idx, tf):
    # get myosin concentration inside a cell
    cell_mask = segmentation[tf] == idx
    myo_in = myosin[tf] * cell_mask
    return np.sum(myo_in) / np.sum(cell_mask) * PIX_AREA


def get_cell_size(idx, tf):
    # get cell size in pixels
    cell_mask = segmentation[tf] == idx
    return np.sum(cell_mask)


def smooth(values, sigma=3, tolerance=0.1):
    # smooth noisy data
    values = np.array(values)
    # check if any value is suspicious (differs from its neighbors too much)
    # it is most likely a merge
    for i in range(1, len(values) - 1):
        avg_neigh = (values[i - 1] + values[i + 1]) / 2
        if not (1 + tolerance) > (values[i] / avg_neigh) > (1 - tolerance):
            # replace this value with neighbors' average
            values[i] = avg_neigh
    # smooth with gaussian filter
    values = gaussian_filter1d(values, sigma=sigma)
    # crop the first and the last value
    # due to possible smoothing border artifacts
    return values[1:-1]


def remove_border_cells(segm, data_frame):
    # the area of cells on the border is unreliable
    # so we remove them
    segm_borders = segm.copy()
    segm_borders[:, 2:-2, 2:-2] = 0
    for tf in range(len(segm)):
        border_cells = np.unique(segm_borders[tf])
        border_cells = border_cells[border_cells != 0]
        for cell in border_cells:
            data_frame = data_frame[~((data_frame['frame_nb'] == tf) & (data_frame['new_id'] == cell))]
    return data_frame


def get_size_and_myo(table, myo_s=3, area_s=3):
    # for every cell in every time point get myo conc and size
    all_in_myo, all_out_myo, all_sizes = {}, {}, {}
    for idx in table['new_id'].unique():
        idx_data = table[table['new_id'] == idx]
        # don't take the first two frames, there are segmentation errors
        idx_data = idx_data[idx_data['frame_nb'] >= 2]
        tps = np.array(idx_data['frame_nb'])
        # if the cell is not present in enough frames, drop it
        # otherwise it's mostly smoothing artifacts
        if len(tps) < 5: continue
        # get cell myo, outside myo and area for every cell in every time frame
        myo = [get_myo_in(idx, tp) for tp in tps]
        o_myo = [get_myo_around(idx, tp) for tp in tps]
        area = [get_cell_size(idx, tp) for tp in tps]
        # smooth the values calculated per cell
        # the ones around are less noisy
        myo = smooth(myo, sigma=myo_s, tolerance=1)
        area = smooth(area, sigma=area_s, tolerance=0.1)
        # create dicts for every feature
        all_in_myo[idx] = {t: m for t, m in zip(tps[1:-1], myo)}
        all_out_myo[idx] = {t: o for t, o in zip(tps, o_myo)}
        all_sizes[idx] = {t: s for t, s in zip(tps[1:-1], area)}
    return all_in_myo, all_out_myo, all_sizes


def get_data_to_plot(myo_in_conc, myo_out_conc, sizes):
    data_points = []
    for idx in myo_in_conc.keys():
        tps = myo_in_conc[idx].keys()
        for tp in range(min(tps), max(tps) - 1):
            if tp not in tps or tp+1 not in tps: continue
            # calculate size change as next frame size divided by current ones'
            size_change = sizes[idx][tp + 1] / sizes[idx][tp]
            cell_myo = myo_in_conc[idx][tp]
            nbr_myo = myo_out_conc[idx][tp]
            data_points.append([size_change, cell_myo, nbr_myo])
    return np.array(data_points)


def show_myo_around_in(idx, tf, n=70):
    no_cell_mask = segmentation[tf] != idx
    dist_tr = distance_transform_edt(no_cell_mask)
    cell_countour = (dist_tr <= 2) * no_cell_mask
    myo_countour = (dist_tr < n+1) * (dist_tr > n-1)
    mask_in_around = (dist_tr <= n)
    myo_in_around = myosin[tf] * mask_in_around
    myo_in_around = myo_in_around / np.max(myo_in_around)
    plt.imshow(cell_countour + myo_countour + myo_in_around)
    plt.show()


data_h5 = '/home/zinchenk/work/drosophila_emryo_cells/data/img5.h5'
tracking_csv = '/home/zinchenk/work/drosophila_emryo_cells/data/img5.csv'

with h5py.File(data_h5, 'r') as f:
    membranes = f['membranes'][:]
    myosin = f['myosin'][:]
    segmentation = f['segmentation'][:]

data_table = pd.read_csv(tracking_csv)
data_table = remove_border_cells(segmentation, data_table)
myo_i, myo_o, c_area = get_size_and_myo(data_table, myo_s=3, area_s=3)
to_plot = get_data_to_plot(myo_i, myo_o, c_area)


# Figure 2K (main)
# Myosin concentration within a cell plotted versus surrounding myosin concentration in a ring
plt.scatter(to_plot[:, 1], to_plot[:, 2], c=to_plot[:, 0], cmap='RdYlBu', vmin=0.9, vmax=1.1, s=20)
plt.vlines([18, 22], 5, 48, linestyles='dotted')
plt.hlines([5, 48], 18, 22, linestyles='dotted')
plt.xlabel("Cell's myosin concentration (log)", size=25)
plt.ylabel("Myosin concentration in the neighborhood (log)", size=25)
plt.loglog()
plt.colorbar()
plt.show()


# Figure 2K (bottom right inset)
# Cells with inside concentration of 18-22, myo around against time change
plot_cutout = to_plot[(18 < to_plot[:, 1]) & (to_plot[:, 1] < 22)]
slope, intercept, rvalue, _, _ = linregress(plot_cutout[:, 0], np.log(plot_cutout[:, 2]))
y = intercept + slope * plot_cutout[:, 0]
fig, ax = plt.subplots()
ax.plot(plot_cutout[:, 0], y, 'red', label='linear fit')
ax.scatter(plot_cutout[:, 0], np.log(plot_cutout[:, 2]), s=100, c='tab:grey')
plt.xlabel("Relative size change", size=25)
plt.ylabel("Myosin concentration in the neighborhood (log)", size=25)
plt.text(1.06, 2.05, "Correlation={:.4f}".format(rvalue), size=20)
plt.legend(loc='upper left', fontsize=20)
plt.show()


# Figure 2K (upper left inset)
# Visualizing ring around the cell used to calculate outside myo concentration
show_myo_around_in(18, 11)


# Figure 2L (inset)
# Change in cell size compared to the ratio of cell-intrinsic over surrounding myosin concentration
exp = to_plot[np.where(to_plot[:, 0] > 1.01)]
constr = to_plot[np.where(to_plot[:, 0] < 0.99)]
middle = to_plot[np.where((to_plot[:, 0] >= 0.99) & (to_plot[:, 0] <= 1.01))]
fig, ax = plt.subplots()
ax.scatter(exp[:, 1] / exp[:, 2], exp[:, 0], c='tab:blue')
ax.scatter(constr[:, 1] / constr[:, 2], constr[:, 0], c='tab:red')
ax.scatter(middle[:, 1] / middle[:, 2], middle[:, 0], c='y')
ax.hlines(1, 0.4, 4.9)
ax.vlines(1, 0.83, 1.10)
plt.xlabel("Myosin concentration inside / outside", size=25)
plt.ylabel("Relative size change", size=25)
plt.show()


# Figure 2L (main)
# Density histogram of constricting and expanding cells
# binned by  the ratio of cell-intrinsic over surrounding myosin concentration
sm_range = np.arange(0.25, 5.25, 0.125)
plt.hist(exp[:, 1] / exp[:, 2], bins=sm_range, density=True, histtype='bar',
         label='Expanding', color='tab:blue', alpha=0.6)
plt.hist(constr[:, 1] / constr[:, 2], bins=sm_range, density=True, histtype='bar',
         label='Constricting', color='tab:red', alpha=0.6)
plt.ylabel('Cells density', size=25)
plt.xlabel('Ratio in/out myosin', size=25)
plt.legend(loc='upper left', fontsize=15)
plt.show()
