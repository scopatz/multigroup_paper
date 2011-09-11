import numpy as np
import tables as tb


with tb.openFile('lwr/lwr.h5', 'a') as f:
    #grp = f.root.sigma_2n_x
    grp = f.root.sigma_gamma_x

    for a in grp:
        mask = np.isnan(a)
        a[mask] = 0.0
