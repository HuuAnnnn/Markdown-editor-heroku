import streamlit as st
from streamlit_autorefresh import st_autorefresh
from localStorage import localStoragePy
import sys
sys.path.append('./localStorage')
from localStorage import localStoragePy


st.set_page_config(
    page_title="Markdown Editor",
     layout="wide",
)

col1, col2 = st.columns([5, 5])
layout_sidebar = st.sidebar
layout_sidebar.write('''### Mark downfiles''')
localStorage = localStoragePy('Markdown Editor', 'text')

md_files = localStorage.getItem('files')
if md_files:
    md_tuple = tuple([md_file.strip() for md_file in md_files.split(',') if md_file.strip() != ''])
else:
    md_tuple = ()
file = layout_sidebar.radio(
    "",
    md_tuple
)

save_btn = layout_sidebar.button("Save")
layout_sidebar.write('''### New file''')
file_name = layout_sidebar.text_input("Your file name:", value="")
create_btn = layout_sidebar.button("Create new file")
delete_btn = layout_sidebar.button("Delete file")

if create_btn:
    create_file_name = file_name
    if '.md' not in create_file_name:
        create_file_name += '.md'
    
    if create_file_name not in md_tuple and create_file_name != ' ' and create_file_name != '' and len(create_file_name) > 1:
        current_data = localStorage.getItem('files')
        if not current_data:
            current_data = ""
        localStorage.setItem('files', current_data +', '+create_file_name)
        localStorage.setItem(create_file_name, "")
        st_autorefresh()

st.markdown(
    """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 250px;
            background-color: #151b25;
        }

        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 250px;
            margin-left: -250px;
            background-color: #151b25;
        }
        [class="row-widget stButton"] > button,
        [class="row-widget stDownloadButton"] > button {
            width: 100%;
        }

        [data-baseweb="base-input"] > textarea:first-child {
            background-color: #0e1117;
        }

        [data-baseweb="base-input"] > input:first-child {
            width: 100%;
            background-color: #364156;
        }
        </style>
    """,
    unsafe_allow_html=True,
)

markdown_content = ""

with col1:    
    st.write('''##### Editor area''')
    editor = st.empty()
with col2:
    if file:
        st.write('''##### {}'''.format(file))
        content = ""
        lines = 0
        content=localStorage.getItem(file)
        if content:
            lines = len(content.split("\n"))
        
        markdown_content = editor.text_area('', value=localStorage.getItem(file), height= 1024 if lines*28 <= 1024 else lines*28)
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.write('''##### Untitled''')

if save_btn:
    localStorage.setItem(file, markdown_content)

if markdown_content:
    layout_sidebar.download_button('Download {}'.format(file), markdown_content, mime='text/plain;charset=UTF-8',file_name=file)

if delete_btn:
    localStorage.removeItem(file)
    localStorage.setItem('files', 
        localStorage.getItem('files').replace('{}'.format(file), '').replace(',,', '')
    )
    st_autorefresh()

current_storage = localStorage.getItem('files')
if current_storage:
    localStorage.setItem('files',localStorage.getItem('files').replace(', ,', ''))