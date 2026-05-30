import numpy as np

_DEG2RAD = np.pi / 180
_VIL_CONST = 3.44e-6
_RM = 8500
_VIL_EXP = 4.0 / 7.0


def _height_single(distance, elevation):
    return distance * np.sin(elevation * _DEG2RAD) + distance ** 2 / (2 * _RM)


def vert_integrated_liquid(ref, distance, elev, beam_width=0.99, threshold=18., density=False):
    v_beam_width = beam_width * _DEG2RAD
    zshape, xshape, yshape = ref.shape[0], ref.shape[1], ref.shape[2]
    VIL = np.zeros((xshape, yshape), dtype=np.float64)

    vert_z_all = np.power(10.0, ref / 10.0)

    dist_m = distance * 1000.0
    hi = dist_m * np.sin(v_beam_width / 2)

    elev_rad = elev * _DEG2RAD
    sin_diff = np.sin(elev_rad[1:]) - np.sin(elev_rad[:-1])

    above_threshold = ref > threshold
    z_avg = (vert_z_all[:-1] + vert_z_all[1:]) / 2.0
    factors = np.power(z_avg, _VIL_EXP)

    for i in range(xshape):
        for j in range(yshape):
            positions = np.where(above_threshold[:, i, j])[0]
            if positions.size == 0:
                continue

            pos_s = positions[0]
            pos_e = positions[-1]
            dist = dist_m[i, j]

            ht_values = dist * sin_diff[:pos_e]
            m1 = _VIL_CONST * np.sum(factors[:pos_e, i, j] * ht_values)

            if not density:
                mb = _VIL_CONST * np.power(vert_z_all[pos_s, i, j], _VIL_EXP) * hi[i, j]
                mt = _VIL_CONST * np.power(vert_z_all[pos_e, i, j], _VIL_EXP) * hi[i, j]
                VIL[i, j] = m1 + mb + mt
            else:
                if pos_s == pos_e:
                    VIL[i, j] = 0
                else:
                    h_lower = _height_single(distance[i, j], elev[pos_s])
                    h_higher = _height_single(distance[i, j], elev[pos_e])
                    VIL[i, j] = m1 / (h_higher - h_lower)

    return VIL


def echo_top(ref, distance, elev, radarheight, threshold=18.):
    zshape, xshape, yshape = ref.shape[0], ref.shape[1], ref.shape[2]
    et = np.zeros((xshape, yshape), dtype=np.float64)

    h_ = []
    for e in elev:
        h = distance * np.sin(e * _DEG2RAD) + distance ** 2 / (2 * _RM) + radarheight / 1000
        h_.append(h)
    hght = np.stack(h_, axis=0)

    above_threshold = ref >= threshold

    for i in range(xshape):
        for j in range(yshape):
            positions = np.where(above_threshold[:, i, j])[0]

            if positions.size == 0:
                continue

            max_pos = positions[-1]

            if ref[zshape - 1, i, j] >= threshold:
                et[i, j] = hght[zshape - 1, i, j]
                continue

            if max_pos == 0:
                et[i, j] = hght[0, i, j]
                continue

            z1 = ref[max_pos, i, j]
            z2 = ref[max_pos + 1, i, j]
            h1 = hght[max_pos, i, j]
            h2 = hght[max_pos + 1, i, j]
            w1 = (z1 - threshold) / (z1 - z2)
            et[i, j] = w1 * h2 + (1 - w1) * h1

    return et
