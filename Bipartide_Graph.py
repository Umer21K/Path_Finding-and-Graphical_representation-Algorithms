import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from networkx import bipartite_layout

class BipartiteGraphApp:
    def __init__(self, root, num_nodes_X, num_nodes_Y):
        self.root = root
        self.root.title("Bipartite Graph")
        self.root.geometry("800x600")

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(expand=1, fill="both")

        self.draw_bipartite_graph(num_nodes_X, num_nodes_Y)

    def draw_bipartite_graph(self, num_nodes_X, num_nodes_Y):
        G = nx.DiGraph()

        # Generate node labels dynamically based on the number of nodes
        nodes_X = [f"X{i}" for i in range(1, num_nodes_X + 1)]
        nodes_Y = [f"Y{i}" for i in range(1, num_nodes_Y + 1)]

        # Generate additional edges dynamically to meet the requirements
        ex = [(f"X{i}", f"Y{j}") for i in range(1, num_nodes_X + 1) for j in range(1, num_nodes_Y + 1)]

        edge = pd.DataFrame([{"s": s, "t": t} for s, t in ex])

        # setting the attributes
        G.add_nodes_from(nodes_X, bipartite=0)
        G.add_nodes_from(nodes_Y, bipartite=1)
        # setting edges between the 2 sets of notes
        G.add_edges_from(tuple(x) for x in edge.values)

        # makes sure the layout is in bipartite form
        pos = bipartite_layout(G, nodes_X)

        # this specifies positions for the sets of nodes so they are in separate columns
        pos.update((node, (0, index)) for index, node in enumerate(nodes_X))
        pos.update((node, (1, index)) for index, node in enumerate(nodes_Y))

        # Draw nodes from each set with different colors
        nx.draw(G, pos, nodelist=nodes_X, node_color="blue", with_labels=True, font_weight="bold", node_size=700)
        nx.draw(G, pos, nodelist=nodes_Y, node_color="red", with_labels=True, font_weight="bold", node_size=700)

        # Embed the graph in the Tkinter window
        figure_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def main():
    root = tk.Tk()
    app = BipartiteGraphApp(root, num_nodes_X=10, num_nodes_Y=10)  # Adjust the number of nodes as needed
    root.mainloop()

if __name__ == "__main__":
    main()
