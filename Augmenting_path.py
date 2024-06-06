import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import cycle
import time


class FordFulkersonGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ford-Fulkerson Algorithm Visualization")

        self.graph = nx.DiGraph()
        # Create 10 vertices
        self.graph.add_nodes_from(range(10))
        # Add edges with random capacities
        self.graph.add_edges_from([(0, 1, {'capacity': 8, 'flow': 0}),
                                   (0, 2, {'capacity': 12, 'flow': 0}),
                                   (1, 3, {'capacity': 5, 'flow': 0}),
                                   (1, 4, {'capacity': 10, 'flow': 0}),
                                   (2, 5, {'capacity': 6, 'flow': 0}),
                                   (2, 6, {'capacity': 14, 'flow': 0}),
                                   (3, 7, {'capacity': 8, 'flow': 0}),
                                   (3, 8, {'capacity': 6, 'flow': 0}),
                                   (4, 9, {'capacity': 7, 'flow': 0}),
                                   (5, 9, {'capacity': 10, 'flow': 0}),
                                   (6, 7, {'capacity': 15, 'flow': 0}),
                                   (7, 8, {'capacity': 12, 'flow': 0}),
                                   (8, 9, {'capacity': 9, 'flow': 0})])

        self.flow_value = tk.StringVar()

        self.create_widgets()
        self.draw_graph()

    def create_widgets(self):

        self.flow_entry_label = ttk.Label(self.master, text="Initial Flow Values and Capacity:")
        self.flow_entry_label.pack(side=tk.TOP, pady=5)

        self.flow_entries = {}
        self.capacity_entries = {}  # Add a dictionary to store capacity entry fields
        for u, v, data in self.graph.edges(data=True):
            capacity = data.get('capacity', 0)
            flow_entry = ttk.Entry(self.master, width=5)
            flow_entry.insert(0, str(0))  # Initial flow is set to 0
            flow_entry.pack(side=tk.TOP, pady=2)
            self.flow_entries[(u, v)] = flow_entry

            capacity_entry = ttk.Entry(self.master, width=5)
            capacity_entry.insert(0, str(capacity))  # Set the initial capacity
            capacity_entry.pack(side=tk.TOP, pady=2)
            self.capacity_entries[(u, v)] = capacity_entry

        self.run_button = ttk.Button(self.master, text="Run Ford-Fulkerson", command=self.run_ford_fulkerson)
        self.run_button.pack(side=tk.TOP, pady=10)

        self.exit_button = ttk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.pack(side=tk.TOP, pady=10)

    def run_ford_fulkerson(self):
        source = 0
        sink = 9

        # Update flow and capacity values based on user input
        for u, v, data in self.graph.edges(data=True):
            flow_value = int(self.flow_entries[(u, v)].get())
            capacity_value = int(self.capacity_entries[(u, v)].get())
            self.graph[u][v]['flow'] = flow_value
            self.graph[u][v]['capacity'] = capacity_value

        max_flow, augmenting_paths = self.ford_fulkerson(self.graph, source, sink)

        # Display the max flow value in a new window
        result_window = tk.Toplevel(self.master)
        result_window.title("Ford-Fulkerson Results")
        max_flow_label = ttk.Label(result_window, text=f"Max Flow: {max_flow}")
        max_flow_label.pack(side=tk.TOP, pady=5)

        augmenting_paths_label = ttk.Label(result_window, text="Augmenting Paths:")
        augmenting_paths_label.pack(side=tk.TOP, pady=5)

        for i, path in enumerate(augmenting_paths, start=1):
            path_label = ttk.Label(result_window, text=f"Path {i}: {path}")
            path_label.pack(side=tk.TOP)

        # Draw the simulation with augmenting paths
        self.draw_simulation(augmenting_paths)

    def create_residual_graph(self):
        residual_graph = nx.DiGraph()

        residual_graph.add_nodes_from(self.graph.nodes)

        for u, v, data in self.graph.edges(data=True):
            capacity = data.get('capacity', 0)
            flow = data.get('flow', 0)
            residual_capacity = capacity - flow
            residual_graph.add_edge(u, v, capacity=residual_capacity)
            residual_graph.add_edge(v, u, capacity=flow)

        return residual_graph

    def ford_fulkerson(self, graph, source, sink):
        self.residual_graph = self.create_residual_graph()

        def find_augmented_path():
            visited = set()
            stack = [(source, [source])]

            while stack:
                current, path = stack.pop()
                visited.add(current)

                for neighbor in self.residual_graph.neighbors(current):
                    if neighbor not in visited and self.residual_graph[current][neighbor]['capacity'] > 0:
                        if neighbor == sink:
                            return path + [neighbor]
                        stack.append((neighbor, path + [neighbor]))

            return None

        augmenting_paths = []
        augmented_path = find_augmented_path()

        while augmented_path:
            augmenting_paths.append(augmented_path)

            min_capacity = min(self.residual_graph[augmented_path[i]][augmented_path[i + 1]]['capacity'] for i in
                               range(len(augmented_path) - 1))

            for i in range(len(augmented_path) - 1):
                u, v = augmented_path[i], augmented_path[i + 1]
                self.residual_graph[u][v]['capacity'] -= min_capacity
                self.residual_graph[v][u]['capacity'] += min_capacity

            augmented_path = find_augmented_path()

        max_flow = sum(self.graph[source][neighbor]['capacity'] - self.residual_graph[source][neighbor]['capacity']
                       for neighbor in self.residual_graph.neighbors(source))

        return max_flow, augmenting_paths

    def draw_simulation(self, augmenting_paths):
        # Create a new window for visualization
        simulation_window = tk.Toplevel(self.master)
        simulation_window.title("Ford-Fulkerson Simulation")

        plt.figure()
        pos = nx.spring_layout(self.graph)
        labels = {(u, v): f"{self.graph[u][v]['flow']} / {self.graph[u][v]['capacity']}" for u, v in self.graph.edges}
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10,
                font_color='black')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        plt.title("Max Flow Calculation")
        plt.axis('off')

        canvas = FigureCanvasTkAgg(plt.gcf(), master=simulation_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        colors = cycle(
            ['red', 'green', 'blue', 'purple', 'orange'])  # Cycle through colors for different augmenting paths

        for path in augmenting_paths:
            nx.draw_networkx_edges(self.graph, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
                                   edge_color=next(colors), width=2)

            canvas.draw()
            simulation_window.update()
            time.sleep(1)

    def draw_graph(self):
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Graph Visualization")

        plt.figure()
        pos = nx.spring_layout(self.graph)
        labels = {(u, v): f"{self.graph[u][v]['flow']} / {self.graph[u][v]['capacity']}" for u, v in self.graph.edges}
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10,
                font_color='black')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        plt.title("Graph Visualization")
        plt.axis('off')

        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = FordFulkersonGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()