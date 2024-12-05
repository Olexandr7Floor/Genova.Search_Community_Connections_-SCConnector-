import csv
import graphviz
import matplotlib.pyplot as plt
import numpy as np
import sys

FILTER_VALUE_NETWORK = 0  # Фільтрація для мережі 

def read_graph_data(file_path):
    data = set()
    unique_nodes = set()
    node_mentions = {}
    repeated_edges = {}
    
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if len(row) != 2:
                continue
            from_node, to_node = [node.strip().lower() for node in row]

            if from_node not in unique_nodes:
                unique_nodes.add(from_node)
                node_mentions[from_node] = 1
            else:
                node_mentions[from_node] += 1

            if to_node not in unique_nodes:
                unique_nodes.add(to_node)
                node_mentions[to_node] = 1
            else:
                node_mentions[to_node] += 1

            edge = (from_node, to_node)
            if edge in repeated_edges:
                repeated_edges[edge] += 1
            else:
                repeated_edges[edge] = 1

            data.add(edge)

    return data, node_mentions, repeated_edges

def filter_graph_data(data, node_mentions, filter_value):
    filtered_nodes = {node for node, count in node_mentions.items() if count >= filter_value}
    filtered_data = {(from_node, to_node) for from_node, to_node in data if from_node in filtered_nodes and to_node in filtered_nodes}

    if len(filtered_data) < 1:
        print('Unable to filter, graph disappears. Adjust the filter value.')
        sys.exit()

    return filtered_nodes, filtered_data

def visualize_graph(filtered_data, node_mentions, repeated_edges, output_path):
    dot = graphviz.Digraph(format='png', engine='sfdp')
    dot.attr('graph', nodesep='0.1', ranksep='0.1', overlap='false', splines='true')

    node_counts = {}
    for from_node, to_node in filtered_data:
        node_counts[from_node] = node_mentions[from_node]
        node_counts[to_node] = node_mentions[to_node]

    max_count = max(node_counts.values())

    for node, count in node_counts.items():
        normalized_count = count / max_count
        color = plt.cm.Paired(normalized_count)
        hex_color = "#{:02x}{:02x}{:02x}".format(int(255 * color[0]), int(255 * color[1]), int(255 * color[2]))
        dot.node(node, style='filled', fillcolor=hex_color)

    added_edges = set()
    for from_node, to_node in filtered_data:
        edge = (from_node, to_node)
        if edge not in added_edges and (to_node, from_node) not in added_edges:
            edge_penwidth = repeated_edges[(from_node, to_node)]
            dot.edge(from_node, to_node, penwidth=str(edge_penwidth), arrowhead='none')
            added_edges.add(edge)

    dot.render(output_path)


def main():
    file_path = 'related_persons_pairs.txt'
    filtered = FILTER_VALUE_NETWORK

    data, node_mentions, repeated_edges = read_graph_data(file_path)
    filtered_nodes, filtered_data = filter_graph_data(data, node_mentions, filtered)
    visualize_graph(filtered_data, node_mentions, repeated_edges, 'Connections')

if __name__ == "__main__":
    main()
