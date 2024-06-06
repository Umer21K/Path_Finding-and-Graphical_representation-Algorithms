import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CompleteGraphGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Complete Graph Visualization")

        self.num_nodes_var = tk.StringVar(value="5")  # Default value for the number of nodes

        self.complete_graph = nx.Graph()
        self.create_widgets()

    def create_widgets(self):
        self.num_nodes_label = ttk.Label(self.master, text="Number of Nodes:")
        self.num_nodes_label.pack(side=tk.TOP, pady=5)

        self.num_nodes_entry = ttk.Entry(self.master, textvariable=self.num_nodes_var)
        self.num_nodes_entry.pack(side=tk.TOP, pady=5)

        self.draw_graph_button = ttk.Button(self.master, text="Draw Complete Graph", command=self.draw_complete_graph)
        self.draw_graph_button.pack(side=tk.TOP, pady=10)

        self.exit_button = ttk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.pack(side=tk.TOP, pady=10)

    def draw_complete_graph(self):
        num_nodes = int(self.num_nodes_var.get())

        # Create a complete graph with the specified number of nodes
        self.complete_graph.clear()
        self.complete_graph.add_nodes_from(range(num_nodes))
        self.complete_graph.add_edges_from([(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)])

        graph_window = tk.Toplevel(self.master)
        graph_window.title("Graph Visualization")

        plt.figure()
        pos = nx.spring_layout(self.complete_graph)
        nx.draw(self.complete_graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black')

        plt.title("Complete Graph Visualization")
        plt.axis('off')

        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = CompleteGraphGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
