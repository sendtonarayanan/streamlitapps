import streamlit as st

option_map = {
    0: "Narayanan",
    1: "Raman"   
}
selection = st.pills(
    "Use this app as:",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "You are using this app as: "
    f"{None if selection is None else option_map[selection]}"
)

st.divider()