import numpy as np


def unwrap_2d(image, mask, unwrapped_image, wrap_around):
    """2D phase unwrapping using sequential 1D unwrapping along each axis.

    Parameters
    ----------
    image : numpy.ndarray
        2D wrapped phase image in radians
    mask : numpy.ndarray
        Binary mask where 0 = valid pixel, 1 = invalid/masked pixel
    unwrapped_image : numpy.ndarray
        Output array for unwrapped phase (modified in-place)
    wrap_around : list or tuple
        [wrap_y, wrap_x] - whether each axis wraps around
        wrap_around[0] -> y axis (rows), wrap_around[1] -> x axis (columns)
    """
    image = np.asarray(image, dtype=np.float64)
    mask = np.asarray(mask, dtype=np.uint8)

    result = image.copy()

    valid_mask = mask == 0

    for i in range(result.shape[0]):
        valid_indices = np.where(valid_mask[i])[0]
        if len(valid_indices) < 2:
            continue
        result[i, valid_indices] = np.unwrap(result[i, valid_indices], discont=np.pi)

    for j in range(result.shape[1]):
        valid_indices = np.where(valid_mask[:, j])[0]
        if len(valid_indices) < 2:
            continue
        result[valid_indices, j] = np.unwrap(result[valid_indices, j], discont=np.pi)

    np.copyto(unwrapped_image, result)
