import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt

class HavelHakimiGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Havel-Hakimi Algorithm")

        self.deg_seq_label = ttk.Label(master, text="Enter the degree sequence:")
        self.deg_seq_entry = ttk.Entry(master)
        self.submit_button = ttk.Button(master, text="Submit", command=self.run_algorithm)
        self.steps_text = scrolledtext.ScrolledText(master, wrap="word", width=40, height=10, state=tk.DISABLED)

        self.deg_seq_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")
        self.deg_seq_entry.grid(row=0, column=1, padx=10, pady=10)
        self.submit_button.grid(row=1, column=0, columnspan=2, pady=10)
        self.steps_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def havel_hakimi_algorithm(self, deg_seq):
        deg_seq.sort(reverse=True)
        steps = f"Initial sequence: {deg_seq}\n\n"

        while deg_seq and deg_seq[0] >= 0:
            steps += f"Current sequence: {deg_seq}\n"
            if deg_seq[0] >= len(deg_seq) - 1:
                for i in range(1, deg_seq[0] + 1):
                    deg_seq[i] -= 1
                deg_seq = deg_seq[1:]
            else:
                steps += "The graph is not graphical.\n"
                return False, steps

        if all(x == 0 for x in deg_seq):
            steps += "The graph is graphical.\n"
            return True, steps
        else:
            steps += "The graph is not graphical.\n"
            return False, steps

    def display_graph(self, deg_seq):
        G = nx.Graph()
        for i, degree in enumerate(deg_seq):
            G.add_node(i + 1)
            for j in range(degree):
                if i + j + 1 < len(deg_seq):
                    G.add_edge(i + 1, i + j + 2)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', font_size=8, edge_color='gray', width=1.5)
        plt.title("Graphical Representation")
        plt.show()

    def run_algorithm(self):
        deg_seq_str = self.deg_seq_entry.get()

        try:
            deg_seq = list(map(int, deg_seq_str.split()))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid sequence of integers.")
            return

        is_graphical, steps = self.havel_hakimi_algorithm(deg_seq)

        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, steps)
        self.steps_text.config(state=tk.DISABLED)

        if is_graphical:
            self.display_graph(deg_seq)
        else:
            messagebox.showinfo("Result", "The graph is not graphical.")

def main():
    root = tk.Tk()
    app = HavelHakimiGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
