import streamlit as st
import json
import uuid
from model import metamodel_dict
import graphviz
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
from graph_functions import output_nodes_and_edges, count_nodes, count_edges, check_path, is_empty, find_density, is_directed, specific_node

def upload_graph():
    uploaded_graph = st.file_uploader("Upload an existing graph", type="json")
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        uploaded_nodes = uploaded_graph_dict["nodes"]
        uploaded_edges = uploaded_graph_dict["edges"]
        st.write(uploaded_graph_dict)
    else:
        st.info("Please upload a graph if available")

    update_graph_button = st.button(
        "Update graph via the upload",
        use_container_width=True,
        type="primary"
    )
    if update_graph_button and uploaded_graph is not None:
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["edge_list"] = uploaded_edges
        graph_dict = {
            "nodes": st.session_state["node_list"],
            "edges": st.session_state["edge_list"],
        }
        st.session_state["graph_dict"] = graph_dict
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict

def create_nodes():
    def save_node(name, age, type_n):
        node_dict = {
            "name": name,
            "age": age,
            "id": str(uuid.uuid4()),
            "type": type_n
        }
        st.session_state["node_list"].append(node_dict)

    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    def print_hi(name, age,):
        st.info(f'Hi, My name is {name} and I am {age} years old')
    name_node = st.text_input("Type in the name of the node")
    type_node = st.selectbox("Specify the type of Node", ["Node", "Person"])
    age_node = int(st.number_input("Type in the age of the node", value=0))
    print_hi(name_node, age_node)
    save_node_button = st.button("Store node", use_container_width=True, type="primary")
    if save_node_button:
        save_node(name_node, age_node, type_node)
        st.write(st.session_state['node_list'])
def create_relation():
    def save_edge(node1, relation, node2):
        edge_dict = {
            "source": node1,
            "target": node2,
            "type": relation,
            "id": str(uuid.uuid4())
        }
        st.session_state["edge_list"].append(edge_dict)

    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    # ModelLogic
    node1_col, relation_col, node2_col = st.columns(3)
    node_list = st.session_state["node_list"]
    node_name_list = []
    for node in node_list:
        node_name_list.append(node["name"])
    with node1_col:
        node1_select = st.selectbox(
            "Select the first node",
            options=node_name_list,
            key="node1_select"
        )
    with relation_col:
        # Logic
        relation_list = metamodel_dict["edges"]
        # UI Rendering
        relation_name = st.selectbox(
            "Specify the relation",
            options=relation_list)
    with node2_col:
        node2_select = st.selectbox(
            "Select the second node",
            options=node_name_list,
            key="node2_select"
        )
    store_edge_button = st.button("Store Relation", use_container_width=True, type="primary")
    if store_edge_button:
        save_edge(node1_select, relation_name, node2_select)
    st.write(f"{node1_select} is {relation_name} {node2_select}")
    st.write(st.session_state["edge_list"])
def store_graph():
    with st.expander("Show individual lists"):
        st.json(st.session_state["node_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)

    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict
    with st.expander("Show Graph JSON", expanded=False):
        st.json(st.session_state["graph_dict"])

def visualize_graph():
    def set_color(node_type):
        color = "Grey"
        if node_type == "Person":
            color = "Blue"
        elif node_type == "Node":
            color = "Red"
        return color

    with st.expander("Graphviz Visualization"):
        graph = graphviz.Digraph()
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]

        for node in node_list:
            node_name = node["name"]
            graph.node(node_name, color=set_color(node_type="Person"))
        for edge in edge_list:
            source = edge["source"]
            target = edge["target"]
            label = edge["type"]
            graph.edge(source, target, label)
        st.graphviz_chart(graph)

    with st.expander("AGraph Visualization"):
        nodes = []
        edges = []
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]
        for node in node_list:
            node_name = node["name"]
            nodes.append(Node(id=node_name,
                              label=node_name,
                              size=25,
                              shape="circularImage",
                              image="default"))

        for edge in edge_list:
            source = edge["source"]
            target = edge["target"]
            relation = edge["type"]
            edges.append(Edge(source=source,
                              label=relation,
                              target=target))

        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        hierarchical=False)

        return_value = agraph(nodes=nodes,
                              edges=edges,
                              config=config)

    # Update session state with graph dictionary
    st.session_state["graph_dict"] = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"]
    }

def analyze_graph():
    G = nx.DiGraph()
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    node_tuple_list = []
    edge_tuple_list = []
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict
    for node in node_list:
        node_tuple = (node["name"], node)
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["source"], edge["target"], edge)
        edge_tuple_list.append(edge_tuple)

    G.add_nodes_from(node_tuple_list)
    G.add_edges_from(edge_tuple_list)

    select_function = st.selectbox(label="Select Function", options=["Output Nodes and Edges", "Count Nodes", "Count Edges", "Check Path", "Check if Graph is Empty", "Density of Graph", "Is Graph Directed", "Specific Node"])
    if select_function == "Output Nodes and Edges":
        output_nodes_and_edges(graph=G)
    elif select_function == "Count Nodes":
        count_nodes(graph=G)

    elif select_function == "Count Edges":
        count_edges(graph=G)
    elif select_function == "Check Path":
        node1_col, node2_col = st.columns(2)
        with node1_col:
            node1_select = st.selectbox("Select first node", options=G.nodes, key="node1_select")
        with node2_col:
            node2_select = st.selectbox("Select second node", options=G.nodes, key="node2_select")
        if node1_select and node2_select:
            check_path(node1_select, node2_select, graph=G)
    elif select_function == "Check if Graph is Empty":
        is_empty(graph=G)
    elif select_function == "Density of Graph":
        find_density(graph=G)
    elif select_function == "Is Graph Directed":
        is_directed(graph=G)
    elif select_function == "Specific Node":
        node_select = st.selectbox("Select node", options=G.nodes, key="node_select")
        specific_node(node_select, graph=G)


def export_graph():
    graph_string = json.dumps(st.session_state["graph_dict"])
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict

    st.download_button(
        "Export Graph to JSON",
        file_name="graph.json",
        mime="application/json",
        data=graph_string,
        use_container_width=True,
        type="primary"
    )

