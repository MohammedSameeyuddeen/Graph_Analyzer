import streamlit as st
import networkx as nx
def output_nodes_and_edges(graph:nx.Graph):
    st.write(graph.nodes)
    st.write(graph.edges)
def count_nodes(graph:nx.Graph):
    num_nodes = len(graph.nodes)
    num_nodes = graph.number_of_nodes()
    st.info(f"the graph has {num_nodes} nodes")
def count_edges(graph:nx.Graph):
    num_edges = len(graph.edges)
    num_edges = graph.number_of_edges()
    st.info(f"the graph has {num_edges} edges")

def check_path(node1, node2, graph: nx.Graph):
    if nx.has_path(graph, node1, node2):
        st.success(f"There is a path between node {node1} and node {node2}.")
    else:
        st.error(f"There is no path between node {node1} and node {node2}.")
def is_empty(graph: nx.Graph):
    is_empty = nx.is_empty(graph)

    if is_empty:
        st.info("The graph is empty.")
    else:
        st.info("The graph is not empty.")
def find_density(graph: nx.Graph):
    density = nx.density(graph)
    st.info(f"The density of graph is {density}")
def is_directed(graph: nx.Graph):
    is_directed = nx.is_directed(graph)
    if is_directed:
        st.info("The graph is directed.")
    else:
        st.info("The graph is not directed.")
def specific_node(inputNode, graph: nx.Graph):
    node = graph.nodes[inputNode]
    st.info(node)

