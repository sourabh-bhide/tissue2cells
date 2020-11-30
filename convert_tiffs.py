import argparse
import os
import h5py
import numpy as np
import pandas as pd
from tifffile import imread


def get_segm(tif_folder):
    # iterate through the folder with segmented timeframes
    # and merge everything in one np.array
    num_frames = len(os.listdir(tif_folder))
    segm_timepoints = []
    for i in range(num_frames):
        tif_file = os.path.join(tif_folder, 'cell_identity_T{}.tif'.format(i))
        segm_t = imread(tif_file)[:, :, 2]
        segm_timepoints.append(segm_t)
    segm_timepoints = np.array(segm_timepoints)
    return segm_timepoints


def remap_segm(segm_timepoints, data_frame):
    # remap segmentation to keep consistent ids over time
    remapped_segm = np.zeros_like(segm_timepoints)
    track_id_map = {tr_id: new_id + 1 for new_id, tr_id
                    in enumerate(data_frame['track_id_cells'].unique())}
    for row in data_frame.iterrows():
        tf, track_id, loc_id = row[1][['frame_nb', 'track_id_cells', 'local_id_cells']]
        new_id = track_id_map[track_id]
        remapped_segm[tf][segm_timepoints[tf] == loc_id] = new_id
    return remapped_segm, track_id_map


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert tiff data to h5')
    parser.add_argument('data_path', type=str,
                        help='folder with the data')
    parser.add_argument('sample_num', type=int, choices=[5, 6, 24],
                        help='the sample number')
    args = parser.parse_args()

    # get all the files names depending on the sample number
    raw_tif_file = os.path.join(args.data_path, 'Img{}_SUM.tif'.format(args.sample_num))
    segm_folder = os.path.join(args.data_path, 'Img{}_segmentation/'.format(args.sample_num))
    tracking_csv = os.path.join(args.data_path, 'img{}_full.csv'.format(args.sample_num))
    out_h5 = os.path.join(args.data_path, 'img{}.h5'.format(args.sample_num))

    # read the data
    raw_data = imread(raw_tif_file)
    segmentation = get_segm(segm_folder)
    data_table = pd.read_csv(tracking_csv)

    # remap segmentation to have consistent cell ids over time
    # and save the new ids as a separate columns in the tracking csv file
    remapped_segmentation, id_map = remap_segm(segmentation, data_table)
    data_table['new_id'] = [id_map[key] for key in data_table['track_id_cells']]
    data_table.to_csv(tracking_csv, index=False)

    # not all the timeframes in the raw data were segmented
    # so depending on the sample number, segmentation starts and ends differently
    if args.sample_num == 5:
        raw_data = raw_data[2:33]
    elif args.sample_num == 6:
        raw_data = raw_data[:23]
    elif args.sample_num == 24:
        raw_data = raw_data[:31]

    # write down all the volumes as one h5 file
    with h5py.File(out_h5, 'w') as f:
        _ = f.create_dataset('membranes', data=raw_data[:, 0], compression='gzip')
        _ = f.create_dataset('myosin', data=raw_data[:, 1], compression='gzip')
        _ = f.create_dataset('segmentation_unmapped', data=segm_timepoints, compression='gzip')
        _ = f.create_dataset('segmentation', data=remapped_segmentation, compression='gzip')
