import streamlit as st
import pandas as pd

# Initialize state
def init_state():
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


def sort_by_size(scope, desc = True):
    # Group by 'B', get unique values from 'A' and convert to list
    result = st.session_state.all_data[st.session_state.all_data.C == scope].groupby('B')['A'].unique().apply(list).to_dict()
    st.session_state.my_data = dict(sorted(result.items(), key=lambda item: len(item[1]), reverse=desc))
    st.session_state.length = len(st.session_state.my_data)

# Load data
def load_data():
    df = pd.DataFrame({
        'A': ['How to', 'Be a miserable', 'Hopeless little', 'Madam in a pony', 'Soft as a fluster',
              'Manually tested', 'Hello World programmer', 'Eight by nine', 'A text is a must', 'That will be all',
              'Sixteen twenty one', 'All of things come to an end', 'Good bye all',
              'I will rise again', 'Until now so long'],
        'B': ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c', 'd', 'e', 'e', 'e', 'e', 'e'],
        'C': ['In', 'In', 'Out', 'In','In','In', 'Out', 'Out', 'Out', 'Out', 'In', 'In', 'Out', 'Out', 'Out']
    })
    st.session_state.all_data = df


def expander_content(key, alist):
    if key not in st.session_state.checkbox_indices:
        st.session_state.checkbox_indices[key] = 0

    index = st.session_state.checkbox_indices[key]
    sublist = alist[:index + max_checkbox]

    for item in sublist:
        st.checkbox(item, key=f'{key}_{item}')

    if index + max_checkbox < len(alist):
        if st.button('Load more checkboxes', key=f'{key}_load_more_checkboxes'):
            st.session_state.checkbox_indices[key] += max_checkbox
            st.experimental_rerun()


def view_page():
    keys = list(st.session_state.my_data.keys())[st.session_state.my_index:st.session_state.my_index + max_expander]
    for key in keys:
        if key not in st.session_state.loaded_keys:
            st.session_state.loaded_keys.append(key)
    st.session_state.my_index += max_expander


def update_index():
    st.session_state.my_index = 0
    st.session_state.loaded_keys = []
    st.session_state.checkbox_indices = {}


def update_sort():
    st.session_state.my_data = dict(sorted(st.session_state.my_data.items(), 
                                           key=lambda item: len(item[1]), 
                                           reverse=st.session_state['sort_button']=='Desc'))
    update_index()


def base_component():
    st.text(f'Index: {st.session_state.my_index}')
    st.text(f'Data size: {st.session_state.length}')

    op1 = st.selectbox('Please select In or Out of scope', options=['In', 'Out'], on_change=update_index)
    op2 = st.selectbox('Please select sorting order', options=['Asc', 'Desc'], on_change=update_sort, key = 'sort_button')

    sort_by_size(op1,desc= op2=='Desc')


    for key in st.session_state.loaded_keys:
        with st.expander(key):
            expander_content(key, st.session_state.my_data[key])

    if st.session_state.my_index < st.session_state.length:
        if st.session_state.my_index == 0:
            view_page()
            st.experimental_rerun()
        else:
            if st.button('Load more expanders'):
                view_page()
                st.experimental_rerun()

max_expander = 2
max_checkbox = 2
init_state()
load_data()
base_component()
