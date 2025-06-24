import streamlit as st
import pages
import hashlib
import altair as alt

alt.data_transformers.disable_max_rows()


st.markdown(
    """
<style>
button {
    width: 250px !important
}
</style>""",
    unsafe_allow_html=True,
)


mapping = {
    "Home": pages.show_homepage,
    "DWT basics": pages.show_dwt_basics,
    "DWT Shrinkage": pages.show_dwt_shrinkage,
    "DWT and Scalograms": pages.show_scalograms,
    "DWT Clustering": pages.show_clustering,
    "Summary": pages.show_summary,
}


def show_page(page):
    st.session_state.page = page


def show_nav_buttons(page):
    keys = list(mapping.keys())
    no_cols = 3

    cols = st.columns(no_cols)
    ind = keys.index(page)
    if ind > 0:
        title = keys[ind - 1]
        cols[0].button(
            " ← \u00a0\u00a0\u00a0" + title, on_click=show_page, args=(title,)
        )
    if ind + 1 < len(mapping):
        title = keys[ind + 1]
        cols[no_cols - 1].button(
            title + "\u00a0\u00a0\u00a0 → ", on_click=show_page, args=(title,)
        )


def introduction():
    st.header("Introduction")


def show_password():
    st.header("This site is password protected")
    text = st.text_input("Enter password")
    st.session_state.password = text


def get_markdown_text(filename):
    with open("md/" + filename + ".md") as f:
        lines = f.readlines()
    return "".join(lines)


def show_app():
    st.sidebar.subheader("Menu")
    for t in mapping.keys():
        st.sidebar.button(t, on_click=show_page, key="menu" + t, args=(t,))

    st.sidebar.markdown(get_markdown_text("about-me"))

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    page = st.session_state.page
    func = mapping[page]
    func()
    st.write("")
    show_nav_buttons(page)


def check_password():
    PASS = "c750a40e2e5c5c1029326927401d4a21"

    if "password" not in st.session_state:
        show_password()
        hash = hashlib.md5(st.session_state.password.encode()).hexdigest()

    else:
        hash = hashlib.md5(st.session_state.password.encode()).hexdigest()
        if hash != PASS:
            show_password()
            hash = hashlib.md5(st.session_state.password.encode()).hexdigest()
            if hash != PASS:
                st.warning("Wrong password")

    if hash == PASS:
        show_app()


show_app()
