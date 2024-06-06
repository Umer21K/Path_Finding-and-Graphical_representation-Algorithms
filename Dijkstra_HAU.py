import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import random

class DijkstraVisualization:
    def __init__(self, master):
        self.master = master
        self.master.title("Dijkstra's Algorithm Visualization")
        self.master.geometry("800x600")

        self.canvas_frame = ttk.Frame(self.master)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.graph = nx.Graph()
        self.add_nodes_edges()

        self.result_text = tk.StringVar()
        self.result_label = ttk.Label(self.master, textvariable=self.result_text)
        self.result_label.pack(pady=10)

        self.run_button = ttk.Button(self.master, text="Run Dijkstra's Algorithm", command=self.run_dijkstra)
        self.run_button.pack(pady=10)

    def add_nodes_edges(self):
        # Clear existing graph
        self.graph.clear()

        # Add nodes
        nodes = ["A", "B", "C", "D", "E"]
        self.graph.add_nodes_from(nodes)

        # Connect nodes randomly to ensure traversal through other nodes
        self.graph.add_edge("A", "B", weight=random.randint(1, 10))
        self.graph.add_edge("A", "C", weight=random.randint(1, 10))
        self.graph.add_edge("B", "D", weight=random.randint(1, 10))
        self.graph.add_edge("C", "D", weight=random.randint(1, 10))
        self.graph.add_edge("D", "E", weight=random.randint(1, 10))
      

    def draw_graph(self, edge_colors=None):
        self.ax.clear()
        pos = nx.spring_layout(self.graph)  # Spring layout
        nx.draw(self.graph, pos, with_labels=True, node_size=700, font_size=10, font_color='white', font_weight='bold',
                node_color='skyblue', edge_color=edge_colors, font_family='arial', ax=self.ax)

        edge_labels = {(edge[0], edge[1]): edge[2]['weight'] for edge in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)

        self.canvas.draw()

    def run_dijkstra(self):
        start_node = "A"
        distances = {node: float('infinity') for node in self.graph.nodes}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        edge_colors = ['gray'] * len(self.graph.edges)

        def dijkstra_step():
            nonlocal distances, priority_queue, edge_colors
            if priority_queue:
                current_distance, current_node = heapq.heappop(priority_queue)

                for neighbor, edge_data in self.graph[current_node].items():
                    distance = current_distance + edge_data['weight']
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(priority_queue, (distance, neighbor))
                        edge_colors[list(self.graph.edges).index((current_node, neighbor))] = 'green'

                self.draw_graph(edge_colors)
                result_str = "Shortest distances from node {}:\n".format(start_node)
                for node, distance in distances.items():
                    result_str += "{}: {}\n".format(node, distance if distance != float('infinity') else "Not Reachable")

                self.result_text.set(result_str)
                self.master.after(1000, dijkstra_step)  # Delay for 1 second (1000 milliseconds)
            else:
                self.draw_graph(edge_colors)

        dijkstra_step()


def main():
    root = tk.Tk()
    app = DijkstraVisualization(root)
    root.mainloop()

if __name__ == "__main__":
    main()
