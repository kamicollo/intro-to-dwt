import streamlit as st

from sklearn.metrics import pairwise_distances
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.sparse import csr_matrix
from scipy.spatial.distance import squareform
import numpy as np
import pywt
import altair as alt
import pandas as pd
import sections.dwt_shrinkage as dwt_shrinkage

@st.experimental_memo(max_entries=50)
def run_clustering(_sp_mat, threshold=0):
    pdists = pairwise_distances(_sp_mat, metric='cityblock')            
    dists = squareform(pdists)
    
    model = linkage(dists, method='complete')
    clusters = fcluster(model, threshold, criterion='distance')

    return model, clusters

@st.experimental_memo(max_entries=50)
def get_sparse_matrix(series):
    rows = np.array([], dtype=int)
    data = np.array([], dtype=float)
    cols = np.array([], dtype=int)
    for i, t in enumerate(series.values):   
        inds = np.where(t != 0)[0]            
        data = np.concatenate((data, t[inds]))
        cols = np.concatenate((cols, inds))
        rows = np.concatenate((rows, np.ones((len(inds)), dtype=int) * i))
    
    return csr_matrix((data, (rows, cols)))


@st.experimental_memo(max_entries=50)
def get_coeff_shapes(wavelet):               
    cfs = pywt.wavedec(list(range(8704)), wavelet, 'zero')
    c, slices, shapes = pywt.ravel_coeffs(cfs)
    return (len(c), slices, shapes)    


def sparse_arr_to_coeffs(arr, wavelet):
    l, slices, shapes = get_coeff_shapes(wavelet)
    coeffs = np.zeros((l,))
    coeffs[arr[0]] = arr[1]
    return pywt.unravel_coeffs(coeffs, slices, shapes, 'wavedec')

def build_scalogram(signals, sel_signals, decomp_func):
    scalogram = []
    for r in signals.iloc[sel_signals, :].itertuples():
        coeffs = decomp_func(r[2])
        coeffs = dwt_shrinkage.threshold_dwt(coeffs, saving = 0.95)[0]
        energy = {}
        for i,c in enumerate(coeffs):
            if i > 0:
                n = "D" + str(i)
                energy[n] = np.sum(np.abs(c))
        energy["key"] = "Signal" + str(r[0] + 1)
        energy['type'] = r[3]
        scalogram.append(energy)
    
    sc_df = pd.DataFrame(scalogram).melt(id_vars=['key', 'type'], var_name='Resolution', value_name='Energy')

    names = ["S"] + ["D" + str(i) for i in range(1,12)]
    c = alt.Chart(sc_df, height=400).mark_line().encode(
            x= alt.X('Resolution', sort=names),
            y='Energy',
            color= alt.Color('type', 
                legend = alt.Legend(orient="bottom", title=None),
                scale=alt.Scale(
                    domain=['Unimpaired signal', 'Wave impairment + upstream modulation', 'Tilt / wave impairment', 'Wave impairment'], 
                    range=['#f1a340', '#f7f7f7', '#998ec3', '#998ec3']
                )),
            strokeDash= alt.StrokeDash('key', legend = None)
        ).properties()
    return c


def show_sparse_code(df):
    with st.expander("See example code"):
        with st.echo():

            # Necessary imports
            
            from sklearn.metrics import pairwise_distances
            import scipy.cluster.hierarchy as sch
            import scipy.sparse as sps
            import scipy.spatial.distance as spd
            import numpy as np

            #Function that converts series to a sparse matrix
            def get_sparse_matrix(series):
                rows = np.array([], dtype=int)
                data = np.array([], dtype=float)
                cols = np.array([], dtype=int)
                for i, t in enumerate(series.values):   
                    inds = np.where(t != 0)[0]            
                    data = np.concatenate((data, t[inds]))
                    cols = np.concatenate((cols, inds))
                    rows = np.concatenate((rows, np.ones((len(inds)), dtype=int) * i))
                
                return sps.csr_matrix((data, (rows, cols)))

            #Obtain a sparse matrix representation
            sparse_mt = get_sparse_matrix(df['DWT coefficients'])

            #Obtain a dense (usual) matrix representation
            dense_mt = sparse_mt.todense()

            def cluster_the_sparse_way(sp_mat, metric, threshold):

                #obtain pairwise distances and convert to 
                # 1D condensed form required for scipy
                pdists = pairwise_distances(sp_mat, metric=metric)            
                dists = spd.squareform(pdists)

                #fit the model
                model = sch.linkage(dists, method='complete')

                #obtain clusters 
                clusters = sch.fcluster(model, threshold, criterion='distance')

                return clusters

            def cluster_the_dense_way(d_mat, metric, threshold):

                #fit the model
                model = sch.linkage(d_mat, method='complete', metric=metric)

                #obtain clusters 
                clusters = sch.fcluster(model, threshold, criterion='distance')

                return clusters

            # RUN clustering
            # cluster_the_sparse_way(sparse_mt, 'cityblock', SOME_THRESH)
            # cluster_the_dense_way(desne_mt, 'cityblock', SOME_THRESH)