import numpy as np
from scipy.linalg import expm
import warnings

import tables as tb

def mexp(A, v):
    max_r = 1.0
    epsilon = 1E-8
    fact_n = 1.0

    new_v_last = np.array(v)
    new_v = np.dot(A, new_v_last) + new_v_last

    new_v_last = new_v

    n = 2
    while (n < 100) and (epsilon < max_r):
        fact_n *= n
        new_v = (np.dot(A, new_v) / fact_n) + new_v

        max_r = (1.0 - new_v_last / new_v).max()

        new_v_last = new_v
        n += 1


    return new_v


def mexp2(A, v):
    fact_n = [1.0, 1.0]
    V = [np.array(v), np.dot(A, v)] 

    n = 2
    while (n < 100):
        fact_n.append(fact_n[-1] * n)
        V.append(np.dot(A, V[-1]))
        n += 1

    fact_n = np.array(fact_n)
    V = np.array(V)

    new_v = (V / fact_n[:, np.newaxis]).sum(axis=0)

    return new_v


def mexp3(A, v):
    fact_n = 1.0
    V = [np.array(v), np.dot(A, v)] 

    n = 2
    while (n < 1000):
        #fact_n *= n
        V.append(np.dot(A, V[-1]) / float(n))
        n += 1

    V = np.array(V)

    new_v = V.sum(axis=0)

    return new_v





def mexp4(A, v):
    fact_n = 1.0
    new_v = np.array(v)
    max_res = 1.0
    epsilon = 1E-16

    V = np.dot(A, v)
    new_v_last = new_v
    new_v = new_v + V

    n = 2
    while (n < 1000) and (epsilon < max_res):
#    while (n < 1000):
#    while (n < 400):
        V = np.dot(A, V / float(n))
        #print np.isnan(V).any(),
        #print np.isinf(V).any()
        V[np.isnan(V)] = 0.0
        V[np.isinf(V)] = 0.0
        V[1E+300 < abs(V)] = 0.0

        #print V[2816], new_v[2816]
        #print V[2812], new_v[2812]
        #print V[2484], new_v[2484]
        #print V[2770], new_v[2770]

        new_v = new_v + V
        max_res = abs(1.0 - new_v_last / new_v).max()
        new_v_last = new_v
        n += 1

    print n

    return new_v







def mexp5(A, v):
    ind = 2812
    #ind = 2816
    #ind = 2484
    #ind = 2770

    #q = A.max()
    #r = q / 1E+3
    #A = A / r
    #print q, r


    fact_n = 1.0
    new_v = np.array(v, dtype=np.float64)
    max_res = 1.0
    epsilon = 1E-16

#    print 0, 1.0, 1.0, new_v[ind]

    V_last = v
    V = np.dot(A, v)
    new_v_last = new_v
    new_v = new_v + V

#    print 1, 1.0, V[ind], new_v[ind]

    n = 2
#    while (n < 1000) and (epsilon < max_res):
#    while (n < 1000):
    while (n < 200):
#        V = np.dot(A, V)
        V = np.dot(A, V / float(n) )

        fact_n = fact_n * float(n)
#        new_v = new_v + (V / fact_n)
        new_v = new_v + V 

#        print n, fact_n, V[ind], new_v[ind], (V[ind] - V_last[ind]) == V[ind]

#        max_res = abs(1.0 - new_v_last / new_v).max()
        new_v_last = new_v
        V_last = V
        n += 1

    #new_v = mexp5(q * A, new_v)
    #new_v = q * new_v

    return new_v



def mexp6(A, v, t):
    I = np.identity(len(A))
    l = np.array(A.diagonal())
    A_lI_k = np.array([A - l[k]*I for k in range(len(A))])

    new_v = np.zeros(len(v))

    for j in range(len(l)):
        v_k = np.array(v)
        for k in range(len(l)):
            print (j, k)
            if k != j:
                v_k = np.dot(A_lI_k[k], v_k) / (l[j] - l[k])

        v_k = np.exp(l[k] * t) * v_k
        new_v = new_v + v_k

    return new_v



if __name__ == '__main__':
    me = mexp6

    """\
    A = np.zeros((5, 5), dtype=float)
    A[range(5), range(5)] = range(1, 6)
    v = np.ones(5, dtype=float)

    new_v = me(A, v)
    scp_v = np.dot(expm(A), v)
    print new_v
    print scp_v
    print 1.0 - scp_v / new_v
    print

    A = np.arange(25)
    A.shape = (5, 5)
    v = np.arange(1, 6)
    
    new_v = me(A, v)
    scp_v = np.dot(expm(A), v)
    print new_v
    print scp_v
    print 1.0 - scp_v / new_v
    print

    A = 100.0 * np.random.random((5, 5))
    A[range(5), range(5)] *= -1.0 
    v = 4000.0 *np.random.random(5)
    v[:3] = 1E-300
    v[-1] = 1E-300

    new_v = me(A, v)
    scp_v = np.dot(expm(A), v)
    print new_v
    print scp_v
    print 1.0 - scp_v / new_v
    print
    """


    f = tb.openFile('/home/scopatz/bright/data/nuc_data.h5')
    d = f.root.decay.read()
    f.close()

    a = d[['from_iso_zz', 'decay_const', 'to_iso_zz', 'branch_ratio']]
    K = set(d['from_iso_zz'])
    K.update(set(d['to_iso_zz']))
    K_num = len(K)
    K_ord = np.array(sorted(list(K)))
    K_ind = {iso: i for i, iso in enumerate(K_ord)}

    A = np.zeros((K_num, K_num), dtype=float)
    for from_iso_zz, decay_const, to_iso_zz, branch_ratio in a:
        if from_iso_zz != to_iso_zz:
            A[K_ind[from_iso_zz], K_ind[to_iso_zz]] = branch_ratio * decay_const
            A[K_ind[from_iso_zz], K_ind[from_iso_zz]] = -decay_const

    #A = A.T
    A = (A.T * 1E+17)
    #A = (A.T * 1E-2)
    #A = (A.T * 1E-2)

    v = np.zeros(K_num, dtype=np.float64)
    v[K_ind[922350]] = 0.05
    v[K_ind[922380]] = 0.95
    #v[K_ind[902310]] = 1.0

    #v = np.ones(K_num, dtype=float)

    print repr(A.sum(axis=0))
    print repr(A.sum(axis=1))
    print A.sum(axis=0)[K_ind[902310]]

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
#        new_v = me(A, v, 1E+17)
        d = abs(A.diagonal())
        m = (d == 0.0)
        B = A / d
        B[:, m] = 0.0
        #B[range(len(d)), range(len(d))] = 0.0
        print repr(B)

        C = 1.0 * A
        m = (1E3 < d)
        C[:, m] = A[:, m] / d[m]
        #C[m, m] = 0.0

        n_v = np.array(v)
        #new_v = mexp5(C, v)

        for n in range(10):
            new_v = mexp5(C, n_v)
            n_v[m] = new_v[m]
            print new_v
            


#    scp_v = np.dot(expm(A), v)

    #scp_v = np.dot(expm(C), v)
    mask = (new_v != 0.0)
    #print K_ord[mask]
    #print repr(new_v[mask])
    #print scp_v[mask]
    #print 1.0 - scp_v[mask] / new_v[mask]
    #print


    from bright import Storage, load_track_isos_text, bright_config
    from mass_stream import MassStream

    with open('tmpisos', 'w') as f:
        for k in K_ord[mask]:
            f.write('{nuc}\n'.format(nuc=k))

    load_track_isos_text('tmpisos')
    print bright_config.track_isos
    m = (v != 0.0)
    ms = MassStream(dict(zip(K_ord[m], v[m])))
    ms.print_ms()
    s = Storage(name='tmpstor')
    print "Starting storage calc..."
    s.calc(ms, 1E+17)
    print "Finished storage calc..."
    s.ms_prod.print_ms()

    cd = s.ms_prod.mult_by_mass()
    bv = np.zeros(K_num, dtype=float)
    for i, val in cd.items():
        bv[K_ind[i]] = val
    
    print
    print K_ord[mask]
    print repr(new_v[mask])
    print bv[mask]
    print 1.0 - bv[mask] / new_v[mask]
