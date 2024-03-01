import streamlit as st
from streamlit_option_menu import option_menu
from tabs import upload_graph, create_nodes, create_relation, store_graph, visualize_graph, analyze_graph, export_graph

st.set_page_config(layout="wide", initial_sidebar_state="auto")
if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []
    st.title("PyInPSE Tutorial 1")
    tab_list = [
        "Import Graph",
        "Create Nodes",
        "Create Relations Between Nodes",
        "Store the Graph",
        "Visualize the Graph",
        "Analyze the Graph",
        "Export the Graph"
        ]
    with st.sidebar:
        selected_tab = option_menu("Main Menu", tab_list,
                               icons=['list-task', 'list-task', 'list-task', 'list-task', 'list-task', 'list-task', 'list-task'], menu_icon="house", default_index=0, orientation="vertical")
        st.write(selected_tab)
    if selected_tab == "Import Graph":
       upload_graph()
    if selected_tab == "Create Nodes":
       create_nodes()
    if selected_tab == "Create Relations Between Nodes":
        create_relation()
    if selected_tab == "Store the Graph":
        store_graph()
    if selected_tab == "Visualize the Graph":
        visualize_graph()
    if selected_tab == "Analyze the Graph":
        analyze_graph()
    if selected_tab == "Export the Graph":
        export_graph()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
