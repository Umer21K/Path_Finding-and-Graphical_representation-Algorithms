import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, Tk, Y
import networkx as nx
import random
import time

class GraphVisualization:
    def __init__(self):
        self.window = Tk()
        self.window.title("Prim's Algorithm Visualization")
        self.canvas_frame = Frame(self.window)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_canvas()

        self.scrollbar = Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.button_frame = Frame(self.window)
        self.button_frame.pack(side=tk.RIGHT)

        self.generate_button = tk.Button(self.button_frame, text="Generate Graph", command=self.generate_graph)
        self.generate_button.pack(pady=10)
        self.prim_button = tk.Button(self.button_frame, text="Run Prim's Algorithm", command=self.run_prim_algorithm)
        self.prim_button.pack(pady=10)

        self.graph = None
        self.pos = None
        self.mst = None
        self.delay = 1000  # Delay in milliseconds

    def create_canvas(self):
        self.canvas = Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 800, 800))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def visualize_graph(self, graph, pos):
        self.canvas.delete("all")
        for edge in graph.edges():
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

            # Calculate midpoint to place the weight
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            # Display weight on the canvas
            weight = graph[edge[0]][edge[1]]['weight']
            self.canvas.create_text(mid_x, mid_y, text=str(weight))

        for node in graph.nodes():
            x, y = pos[node]
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="skyblue", outline="black")
            self.canvas.create_text(x, y, text=str(node))

    def highlight_edge(self, edge):
        if self.canvas:  # Check if the canvas is still available
            x1, y1 = self.pos[edge[0]]
            x2, y2 = self.pos[edge[1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    def run_prim_algorithm(self):
        if self.graph is not None:
            self.mst = prim_algorithm(self.graph)
            edges_to_highlight = list(self.mst.edges())
            self.visualize_prim_algorithm(edges_to_highlight)

    def visualize_prim_algorithm(self, edges):
        self.visualize_graph(self.graph, self.pos)
        for edge in edges:
            self.window.after(self.delay, self.highlight_edge, edge)
            self.window.update()
            time.sleep(self.delay / 1000)

    def generate_graph(self):
        num_vertices = 10  # Change the number of vertices as needed
        self.graph = generate_random_graph(num_vertices)
        self.pos = nx.get_node_attributes(self.graph, 'pos')
        self.visualize_graph(self.graph, self.pos)

    def start(self):
        self.window.mainloop()

def generate_random_graph(num_vertices):
    G = nx.Graph()
    pos = {}

    for i in range(num_vertices):
        x, y = random.uniform(0, 800), random.uniform(0, 800)
        G.add_node(i, pos=(x, y))
        pos[i] = (x, y)

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            weight = random.randint(1, 10)
            G.add_edge(i, j, weight=weight)

    nx.set_node_attributes(G, pos, 'pos')  # Ensure that position is set for every node

    return G

def prim_algorithm(graph):
    MST = nx.Graph()
    start_node = random.choice(list(graph.nodes))
    visited_nodes = set([start_node])

    pos = nx.get_node_attributes(graph, 'pos')  # Get node positions

    while len(visited_nodes) < len(graph.nodes):
        edge_candidates = []

        for node in visited_nodes:
            edges = [(node, neighbor) for neighbor in graph.neighbors(node) if neighbor not in visited_nodes]
            edge_candidates.extend(edges)

        if not edge_candidates:
            # If there are no more edges to consider, break the loop
            break

        edge_candidates.sort(key=lambda edge: graph[edge[0]][edge[1]]['weight'])
        chosen_edge = edge_candidates[0]

        MST.add_edge(chosen_edge[0], chosen_edge[1], weight=graph[chosen_edge[0]][chosen_edge[1]]['weight'])
        visited_nodes.add(chosen_edge[1])

    return MST


def main():
    app = GraphVisualization()
    app.start()

if __name__ == "__main__":
    main()
