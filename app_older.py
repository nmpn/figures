import streamlit as st
import pandas as pd

@st.cache_data
def init_state():
    print('initialising..')
    if 'my_index' not in st.session_state:
        st.session_state.my_index = 0
    if 'length' not in st.session_state:
        st.session_state.length = 0
    if 'my_data' not in st.session_state:
        st.session_state.my_data = None
    if 'loaded_keys' not in st.session_state:
        st.session_state.loaded_keys = []
    if 'checkbox_indices' not in st.session_state:
        st.session_state.checkbox_indices = {}

@st.cache_data
def load_data():
    print('Loading data..')
    df = pd.DataFrame({'A':['How to', 'Be a miserable', 'Hopeless little', 'Madam in a pony',
                            'Soft as a fluster', 'Manually tested', 'Hello World programmer',
                            'Eight by nine', 'A text is a must', 'That will be all',
                            'Sixtenn twenty one', 'All of things come to an end', 'Good bye all',
                            'I will rise again', 'Until now so long'],
                       'B':['a','a','a','b','b','b','c','c','c','d', 'e', 'e', 'e', 'e', 'e']})
    st.session_state.my_data = df.groupby('B').A.unique().apply(list).to_dict()
    st.session_state.length = len(st.session_state.my_data)

def expander_content(alist):
    print('creating expander..')
    for x in alist:
        st.checkbox(x)


def view_page():
    print('viewing data..')
    keys = list(st.session_state.my_data.keys())[st.session_state.my_index:st.session_state.my_index+2]
    for key in keys:
        if key not in st.session_state.loaded_keys:
            with st.expander(key):
                expander_content(st.session_state.my_data[key])
            st.session_state.loaded_keys.append(key)
    st.session_state.my_index += 2

def base_component():
    st.text(f'Index: {st.session_state.my_index}')
    st.text(f'Data size: {st.session_state.length}')
    
    for key in st.session_state.loaded_keys:
        with st.expander(key):
            expander_content(st.session_state.my_data[key])
    
    if st.session_state.my_index < st.session_state.length:
        if st.session_state.my_index==0:
            view_page()
            st.experimental_rerun()
        else:
            if st.button('Load more'):
                view_page()
                st.experimental_rerun()  # To refresh the page and ensure the button stays at the end

init_state()
load_data()
base_component()
