import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from networkx import bipartite_layout

class TripartiteGraphApp:
    def __init__(self, root, num_nodes_X, num_nodes_Y, num_nodes_Z):
        self.root = root
        self.root.title("Tripartite Graph")
        self.root.geometry("800x600")

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(expand=1, fill="both")

        self.draw_tripartite_graph(num_nodes_X, num_nodes_Y, num_nodes_Z)

    def draw_tripartite_graph(self, num_nodes_X, num_nodes_Y, num_nodes_Z):
        G = nx.DiGraph()

        # Generate node labels dynamically based on the number of nodes
        nodes_X = [f"X{i}" for i in range(1, num_nodes_X + 1)]
        nodes_Y = [f"Y{i}" for i in range(1, num_nodes_Y + 1)]
        nodes_Z = [f"Z{i}" for i in range(1, num_nodes_Z + 1)]

        # Generate additional edges dynamically to meet the requirements
        edges_XY = [(f"X{i}", f"Y{j}") for i in range(1, num_nodes_X + 1) for j in range(1, num_nodes_Y + 1)]
        edges_YZ = [(f"Y{i}", f"Z{j}") for i in range(1, num_nodes_Y + 1) for j in range(1, num_nodes_Z + 1)]

        # Setting the attributes
        G.add_nodes_from(nodes_X, bipartite=0)
        G.add_nodes_from(nodes_Y, bipartite=1)
        G.add_nodes_from(nodes_Z, bipartite=2)

        # Setting edges between the sets of nodes
        G.add_edges_from(edges_XY)
        G.add_edges_from(edges_YZ)

        # Makes sure the layout is in bipartite form
        pos = bipartite_layout(G, nodes_X)

        # This specifies positions for the sets of nodes so they are in separate columns
        pos.update((node, (0, index)) for index, node in enumerate(nodes_X))
        pos.update((node, (1, index)) for index, node in enumerate(nodes_Y))
        pos.update((node, (2, index)) for index, node in enumerate(nodes_Z))

        # Draw nodes from each set with different colors
        nx.draw(G, pos, nodelist=nodes_X, node_color="blue", with_labels=True, font_weight="bold", node_size=700)
        nx.draw(G, pos, nodelist=nodes_Y, node_color="red", with_labels=True, font_weight="bold", node_size=700)
        nx.draw(G, pos, nodelist=nodes_Z, node_color="green", with_labels=True, font_weight="bold", node_size=700)

        # Embed the graph in the Tkinter window
        figure_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def main():
    root = tk.Tk()
    app = TripartiteGraphApp(root, num_nodes_X=10, num_nodes_Y=10, num_nodes_Z=10)  # Adjust the number of nodes as needed
    root.mainloop()

if __name__ == "__main__":
    main()
