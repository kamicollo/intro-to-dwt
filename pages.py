import streamlit as st
import numpy as np
import pywt
import json
import pandas as pd
import altair as alt
import itertools
import polars as pl

from sections import dwt_basics, dwt_shrinkage, dwt_clustering

WAV_FAMILY = "db2"


def get_markdown_text(filename):
    with open("md/" + filename + ".md") as f:
        lines = f.readlines()
    return "".join(lines)


def show_homepage():
    st.title("A practical intro to Discrete Wavelet Transformation")
    body_text = get_markdown_text("intro")
    st.markdown(body_text)


def show_dwt_basics():
    # Intro text
    body_text = get_markdown_text("dwt-basics")
    st.markdown(body_text)

    # render the dropdown for wavelet families
    option = st.selectbox(
        "Select a wavelet family",
        ("Daubechies", "Coiflets", "Mexican hat", "Gaussian", "Symlets"),
        index=0,
    )

    wav_fam = {
        "Daubechies": ("db", True),
        "Coiflets": ("coif", True),
        "Mexican hat": ("mexh", False),
        "Gaussian": ("gaus", False),
        "Symlets": ("sym", True),
    }

    w_str, discrete = wav_fam[option]

    wav_list = pywt.wavelist(w_str, kind="all")[:8]
    st.code("hello")
    st.altair_chart(
        dwt_basics.get_wav_image(wav_list, discrete), use_container_width=True
    )

    # More text
    body_text = get_markdown_text("dwt-basics2")
    st.markdown(body_text)

    # Visualize sample signal
    signal = get_sample_signal()
    st.altair_chart(signal_chart(signal), use_container_width=True)

    # More text
    st.markdown(get_markdown_text("dwt-basics3"))

    # Coeff plots
    coeffs = decomp_signal(signal["log(dB)"].values)
    c1, c2 = st.columns(2)

    chart1, chart2 = dwt_basics.get_coeff_plot(coeffs)
    c1.altair_chart(chart1, use_container_width=False)
    c2.altair_chart(chart2, use_container_width=False)


def show_dwt_shrinkage():
    # Intro text
    st.markdown(get_markdown_text("dwt-shrinkage-1"))

    # Illustration of what happens when a level is thresholded
    signal = get_sample_signal()
    coeffs = decomp_signal(signal["log(dB)"].values)

    # Build checkboxes and return result
    lvls = pywt.dwt_max_level(len(signal), WAV_FAMILY)
    sel_levels = dwt_shrinkage.illustrate_levels(lvls)
    th_coeffs = dwt_shrinkage.threshold_coeffs(coeffs, sel_levels)
    rec_raw = reconstruct_signal(th_coeffs)
    rec_signal = wrap_signal(rec_raw)
    rec_signal["Signal"] = "Reconstructed"
    signal["Signal"] = "Original"
    st.altair_chart(overlay_chart(signal, rec_signal), use_container_width=True)

    # Illustration of RREH thresholding
    st.markdown(get_markdown_text("dwt-shrinkage-2"))

    saving = st.slider("Select data compression level", 70.0, 99.9, 70.0, 0.1, "%f%%")
    coeffs = decomp_signal(signal["log(dB)"].values)
    th_coeffs_rreh = dwt_shrinkage.threshold_dwt(coeffs, saving=saving / 100)[0]
    rec_raw_rreh = reconstruct_signal(th_coeffs_rreh)
    rec_signal_rreh = wrap_signal(rec_raw_rreh)
    rec_signal_rreh["Signal"] = "Reconstructed"

    rmse = dwt_shrinkage.compare_signals(rec_raw_rreh, signal["log(dB)"].values) * 100

    c1 = overlay_chart(signal, rec_signal_rreh).properties(
        title=f"Average reconstruction error {rmse:.2f}%"
    )

    st.altair_chart(c1, use_container_width=True)
    st.markdown(get_markdown_text("dwt-shrinkage-3"))


def show_scalograms():
    st.markdown(get_markdown_text("scalogram-1"))

    # Visualize sample signal
    signals = get_sample_signals()

    for r in signals.itertuples():
        col = "#f1a340" if r[3] == "Unimpaired signal" else "#998ec3"
        c = (
            alt.Chart(wrap_signal(r[2]), height=200)
            .mark_line(color=col)
            .encode(x="Frequency (MHz)", y="log(dB)")
            .properties(title=r[3])
        )
        st.altair_chart(c, use_container_width=True)

    # Scalograms
    st.markdown(get_markdown_text("scalogram-2"))

    # placeholder for scalogram chart
    plc = st.empty()
    sel_signals = []

    # Build checkboxes
    cols = st.columns(len(signals))
    for i in range(0, len(signals)):
        sel = cols[i].checkbox("Signal #" + str(i + 1), value=True)
        if sel:
            sel_signals.append(i)

    # Show scalogram (this is ugly, but..)
    if len(sel_signals) > 0:
        c = dwt_clustering.build_scalogram(signals, sel_signals, decomp_signal)
        plc.altair_chart(c, use_container_width=True)

    st.markdown(get_markdown_text("scalogram-3"))


def show_clustering():
    st.markdown(get_markdown_text("clustering-1"))

    node_data = get_node()

    sp_mat = dwt_clustering.get_sparse_matrix()
    threshold = 5500
    model, clusters = dwt_clustering.run_clustering(sp_mat, threshold)

    from plotly_d import create_dendrogram

    c = create_dendrogram(
        model,
        orientation="left",
        height=800,
        color_threshold=threshold,
        hovertext=list(range(100)),
    )
    st.plotly_chart(c, use_container_width=True)

    st.markdown(
        """
        You can explore how the signals look in some selected clusters. 
        Admittedly, this is not a perfect clustering solution but perfect clustering was not the goal either! 
        Instead, I hope this illustrates that using thresholded DWT coefficients can lead to useful results.

        ### Cluster explorations  
        """
    )

    no_clusters = clusters.max() - clusters.min() + 1

    c1, c2 = st.columns([1, 5])

    opts = [3, 5, 9, 13, 16, 21]

    selected_cl = c1.radio(
        label="Example cluster",
        options=opts,
        # list(range(1, no_clusters + 1)),
        index=0,
        format_func=lambda x: "Cluster " + str(x),
    )

    st.caption("Randomly selected 3 signals in cluster")
    cluster_members = np.where(clusters == selected_cl)[0]
    s_ids = np.random.default_rng().choice(cluster_members, 3, replace=False)

    c2.markdown("**What's special about this cluster? **")
    descs = {
        21: "Observe the irregularity at low frequency range (0-50) and its channel borders seem to be less pronounced that usually.",
        16: 'This cluster exhibits what is called "standing waves" pattern.',
        13: "This cluster has a tilt impairment - notice how the signal is not in a straight line.",
        9: "This signal has unusual energy levels - notice that it is in the range log(0-40) dB only.",
        5: "This cluster has a bit of tilt impairment and some waves too (you may need to zoom in).",
        3: "This is an cluster of unimpaired signals.",
    }

    c2.write(descs[selected_cl])

    for id in s_ids:
        id_df = node_data.slice(id, 1).select(pl.col("amplitudes")).collect()
        s = wrap_signal(json.loads(id_df[0, 0]))
        st.altair_chart(signal_chart(s), use_container_width=True)

    st.markdown(get_markdown_text("clustering-2"))

    ex_df = node_data.slice(0, 5).collect().to_pandas()
    ex_df["DWT coefficients"] = ex_df["DWT coefficients"].apply(
        lambda x: np.array(json.loads(x))
    )

    dwt_clustering.show_sparse_code(ex_df)


def show_summary():
    st.markdown(get_markdown_text("summary"))


@st.cache_data()
def decomp_signal(signal):
    return pywt.wavedec(signal, wavelet=WAV_FAMILY, mode="zero")


@st.cache_data()
def reconstruct_signal(coeffs):
    return pywt.waverec(coeffs, wavelet=WAV_FAMILY, mode="zero")


@st.cache_data()
def get_sample_signal():
    with open("data/sample.signal", "r") as f:
        d = json.loads(f.readlines()[0])
    return wrap_signal(np.array(d) / 100)


def get_sample_signals():
    df = pd.read_csv("data/example_signals.csv")
    df["amplitudes"] = df.amplitudes.apply(lambda x: np.array(json.loads(x)) / 100)
    return df


def wrap_signal(signal):
    x = np.linspace(6, 996 + 30, 8704)
    return pd.DataFrame(zip(x, signal), columns=["Frequency (MHz)", "log(dB)"])


def get_node():
    df = pl.scan_csv("data/proc-node.csv")
    return df


@st.cache_data()
def calc_node():
    df = pd.read_csv("data/node.csv")
    df.amplitudes = df.amplitudes.apply(lambda x: np.array(json.loads(x)) / 100)

    def _helper(s):
        cfs = decomp_signal(s)
        th_cfs = dwt_shrinkage.threshold_dwt(cfs, saving=0.95)[0]
        flat_th_cfs = np.fromiter(itertools.chain(*th_cfs), float)
        return flat_th_cfs

    df["DWT coefficients"] = df.amplitudes.apply(_helper)
    return df


def signal_chart(df, height=300, domain=[-80, 10]):
    c = (
        alt.Chart(df, height=height)
        .mark_line()
        .encode(
            x="Frequency (MHz)",
            y=alt.Y("log(dB)", scale=alt.Scale(domain=domain)),
        )
    )
    return c


def overlay_chart(signal, rec_signal):
    c1 = (
        alt.Chart(pd.concat([rec_signal, signal]))
        .mark_line()
        .encode(
            x="Frequency (MHz)",
            y=alt.Y("log(dB)", scale=alt.Scale(domain=[-100, 50])),
            color=alt.Color(
                "Signal",
                scale=alt.Scale(
                    domain=["Original", "Reconstructed"], range=["lightgrey", "Orange"]
                ),
            ),
            opacity=alt.Opacity(
                "Signal",
                scale=alt.Scale(domain=["Original", "Reconstructed"], range=[0.4, 1]),
            ),
        )
    )
    return c1
