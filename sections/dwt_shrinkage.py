import streamlit as st
import numpy as np
import pywt
import itertools


@st.cache_data()
def threshold_coeffs(coeffs, levels):
    cs = coeffs.copy()
    for l in levels:
        cs[l][:] = 0
    return cs


def estimate_rreh_thresh(coeffs, saving=None):
    """
    Estimate RREh-based theershold for DWT coefficients
    If no saving is passed, optimal threshold is computed
    If a saving is passed (0-1), a threshold that ensures such data saving is computed
    """
    unrolled = np.array(list(itertools.chain(*coeffs)))
    if saving is None:
        threshold = np.sqrt(np.sum(unrolled**2)) / unrolled.size
    else:
        sorted_c = np.sort(np.abs(unrolled))
        threshold = sorted_c[int(unrolled.size * saving) + 1]
    return threshold


@st.cache_data()
def threshold_dwt(coeffs, threshold=None, saving=None):
    """
    Performs DWT coefficient thresholding
    If no saving or thresholding is passed, an optimal threshold is used
    Threshold - min absolute threshold to be retained
    Saving - data compression to be achieved (0-1)
    """
    if threshold is None:
        threshold = estimate_rreh_thresh(coeffs, saving)
    raveled, slices, shapes = pywt.ravel_coeffs(coeffs)
    cs = raveled.copy()
    saving = sum(np.abs(raveled) < threshold) / len(raveled)
    cs[np.abs(cs) < threshold] = 0
    return pywt.unravel_coeffs(cs, slices, shapes, "wavedec"), saving, threshold


def compare_signals(sig1, sig2):
    """
    Computes RMSE and MAX SE of two signals
    """
    diffs = (sig1 - sig2) ** 2
    rmse = np.sqrt(np.mean(diffs))
    rng = np.max(sig1) - np.min(sig1)
    return rmse / rng


def illustrate_levels(lvls):
    names = ["S"] + ["D" + str(d) for d in range(1, lvls + 1)]

    no_cols = 6
    col_tuples = [names[r::no_cols] for r in range(0, no_cols)]

    st.caption("Select resolution levels to threshold:")
    cols = st.columns(no_cols)
    check_states = {}

    cb = st.columns(2)

    th_all = cb[0].button("Threshold all")
    keep_all = cb[1].button("Keep all")
    if th_all or keep_all:
        for n in names:
            st.session_state["checkbox_" + n] = True if th_all else False

    for i, nms in enumerate(col_tuples):
        for n in nms:
            check_states[n] = cols[i].checkbox(n, key="checkbox_" + n)

    sel_states = [s for s in check_states if check_states[s]]
    sel_lvls = [names.index(o) for o in sel_states]

    return sel_lvls
