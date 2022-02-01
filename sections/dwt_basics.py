
from turtle import width
import streamlit as st
import pywt
import altair as alt
from altair import datum
import numpy as np
import pandas as pd
from collections import defaultdict
import altair as alt



@st.experimental_memo(max_entries=50)
def get_wav_image(wav_list, discrete):
    no_cols = 4
    no_rows = max(int(len(wav_list) / no_cols),1)

    rows = defaultdict(list)
    
    def base_chart(df, title):
        return alt.Chart(df).mark_line().encode(
            x= alt.X('x', axis=alt.Axis(title = title, labels=False)),
            y= alt.Y('y', axis=alt.Axis(title = "", labels=False))           
        ).properties(
            height=150,
            width=150
        )    

    for i, w_str in enumerate(wav_list):        
        if discrete:
            w = pywt.Wavelet(w_str)
            _, psi_d, x = w.wavefun(level=10)            
        else:
            w = pywt.ContinuousWavelet(w_str)
            psi_d, x = w.wavefun(level=10)
                
        row = int(i / no_cols)    

        c = base_chart(pd.DataFrame(zip(x,psi_d), columns=['x', 'y']), w_str)
        rows[row].append(c)

    res = alt.vconcat(*[alt.hconcat(*r) for r in rows.values()])    
    
    return res

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