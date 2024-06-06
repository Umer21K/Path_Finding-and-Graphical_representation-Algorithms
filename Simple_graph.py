import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SimpleGraphGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Graph Visualization")

        self.simple_graph = nx.Graph()
        self.create_widgets()

    def create_widgets(self):
        self.draw_graph_button = ttk.Button(self.master, text="Draw Graph", command=self.draw_graph)
        self.draw_graph_button.pack(side=tk.TOP, pady=10)

        self.exit_button = ttk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.pack(side=tk.TOP, pady=10)

    def draw_graph(self):
        self.simple_graph.clear()
        self.simple_graph.add_nodes_from(range(10))
        self.simple_graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 0)])

        graph_window = tk.Toplevel(self.master)
        graph_window.title("Graph Visualization")

        plt.figure()
        pos = nx.spring_layout(self.simple_graph)
        nx.draw(self.simple_graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black')

        plt.title("Simple Graph Visualization")
        plt.axis('off')

        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = SimpleGraphGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
