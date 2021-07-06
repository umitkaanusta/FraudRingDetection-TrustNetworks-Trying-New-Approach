"""
Parses the CSV file into a SNAP network

Col1: Source node's id (int)
Col2: Dest node's id (int)
Col3: Rating given to dest by source (int, -10 to 10)
Col4: Timestamp of the rating
"""
from typing import List
import pandas as pd
import snap

RATING_ATTR = "rating"
TIMESTAMP_ATTR = "timestamp"


def get_dataframe():
    df = pd.read_csv("../../raw_data/soc-sign-bitcoinotc.csv")
    df.columns = ["src_id", "dest_id", "rating", "timestamp"]
    return df


def get_nodes(df: pd.DataFrame) -> List[int]:
    return list(set(list(df["src_id"]) + list(df["dest_id"])))


def add_nodes(net: snap.TNEANet, nodes: List[int]):
    for node_id in nodes:
        net.AddNode(node_id)


def add_edges(net: snap.TNEANet, df: pd.DataFrame):
    for i in range(len(df)):
        row = df.iloc[i]
        net.AddEdge(int(row["src_id"]), int(row["dest_id"]))  # Edge id starts from 0
        net.AddIntAttrDatE(i, row["rating"], RATING_ATTR)
        net.AddFltAttrDatE(i, row["timestamp"], TIMESTAMP_ATTR)


def make_network():
    df = get_dataframe()
    nodes = get_nodes(df)
    net = snap.TNEANet()
    net.AddIntAttrE(RATING_ATTR, 0)
    net.AddFltAttrE(TIMESTAMP_ATTR, 0.0)
    add_nodes(net, nodes)
    add_edges(net, df)
