"""
Parses the CSV file into Neo4j
Imports Neo4j query results into NetworkX

Col1: Source node's id (int)
Col2: Dest node's id (int)
Col3: Rating given to dest by source (int, -10 to 10)
Col4: Timestamp of the rating
"""
from typing import List
from neo4j import GraphDatabase
import pandas as pd
import networkx as nx

USER_LABEL = "BTCUser"
RELATIONSHIP_LABEL = "RATED"


def get_driver(url="bolt://localhost:7687", user="neo4j", password="dtdtdt"):
    return GraphDatabase.driver(url, auth=(user, password))


def get_dataframe():
    df = pd.read_csv("../../raw_data/soc-sign-bitcoinotc.csv")
    df.columns = ["src_id", "dest_id", "rating", "timestamp"]
    return df


def get_nodes(df: pd.DataFrame) -> List[int]:
    return list(set(list(df["src_id"]) + list(df["dest_id"])))


def add_nodes(driver, nodes: List[int]):
    s = driver.session()
    for node_id in nodes:
        s.run("MERGE (:%s {node_id: %d});" % (USER_LABEL, node_id))
    s.close()


def add_edges(driver, df: pd.DataFrame):
    s = driver.session()

    def add_edge(src_id, dest_id, rating, timestamp):
        s.run(
                """MATCH (n1 {node_id: %d})
MATCH (n2 {node_id: %d})
WITH n1, n2
MERGE ((n1)-[:%s {rating: %d, timestamp: %f}]->(n2));"""
                % (src_id, dest_id, RELATIONSHIP_LABEL, rating, timestamp)
        )
    df.apply(
        lambda row: add_edge(row["src_id"], row["dest_id"], row["rating"], row["timestamp"]), axis=1
    )
    s.close()


def make_network():
    df_ = get_dataframe()
    driver_ = get_driver()
    nodes_ = get_nodes(df_)
    add_nodes(driver_, nodes_)
    add_edges(driver_, df_)


def neo4j_to_nx(driver, query="MATCH (n)-[r]->(c) RETURN *"):
    # Create a NetworkX MultiDiGraph using data from Neo4j
    s = driver.session()
    results = s.run(query)
    G = nx.MultiDiGraph()
    nodes = list(results.graph()._nodes.values())
    edges = list(results.graph()._relationships.values())
    for node in nodes:
        G.add_node(node.id, labels=node._labels, properties=node._properties)
    for edge in edges:
        G.add_edge(edge.start_node.id, edge.end_node.id, key=edge.id, type=edge.type, properties=edge._properties)
    return G
