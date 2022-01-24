
import streamlit as st
import pywt
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import numpy as np
import pandas as pd



@st.experimental_memo
def get_wav_image(wav_list, discrete):
    no_cols = 4
    no_rows = max(int(len(wav_list) / no_cols),1)
    

    f, axarr = plt.subplots(no_rows, no_cols)
    f.set_size_inches(6, no_rows * 1.5)

    for i, w_str in enumerate(wav_list):        
        if discrete:
            w = pywt.Wavelet(w_str)
            _, psi_d, x = w.wavefun(level=10)            
        else:
            w = pywt.ContinuousWavelet(w_str)
            psi_d, x = w.wavefun(level=10)
        
        col = i % no_cols
        row = int(i / no_cols)    
        if no_rows > 1:
            ax = axarr[row, col]
        else:
            ax = axarr[col]
            
        sns.lineplot(x=x, y=psi_d, ax=ax)
        ax.set_title(w_str, size=8)
        ax.axes.yaxis.set_visible(False)
        plt.tight_layout()
    return f

def get_coeff_plot(coeffs):
    
    c, _, _ = pywt.ravel_coeffs(coeffs)

    dt = []
    names = []
    i = 0
    for c in coeffs:
        name = 'S' if i == 0 else 'D' + str(i)
        names.append(name)
        x = np.linspace(0, 4352, len(c))
        df = pd.DataFrame({
            'x': x,
            "y": c,
            "name": name
        })
        dt.append(df)
        i += 1
    df_coeffs = pd.concat(dt)
    
    base = alt.Chart(df_coeffs).mark_bar().encode(
        x='x:Q',
        y= alt.Y('y:Q', scale=alt.Scale(domain=[-2000, 650]))        
    ).properties(        
        height=80,
        width=300
    ).interactive()

    chart1 = alt.hconcat()
    chart2 = alt.hconcat()
    for n1, n2 in zip(names[:-1:2], names[1::2]):
        chart1 &= base.transform_filter(datum.name == n1).properties(title=n1)
        chart2 &= base.transform_filter(datum.name == n2).properties(title=n2)
    
    chart1 = chart1.configure_axis(
        #labels=False,
        title=None
    ).configure_axisX(labels=False)
    chart2 = chart2.configure_axis(
        labels=False,
        title=None
    )

    return chart1, chart2