import tkinter as tk
from queue import PriorityQueue
import time


root = tk.Tk()
root.title("Shortest Path Finding")
root.geometry("600x650")
root.resizable(False, False)


canvas = tk.Canvas(root, bg="white", width=500, height=500)
canvas.pack(pady=20)


rows, cols = 40, 40
cell_size = 25
grid = []
start = None
end = None

for i in range(rows):
    row = []
    for j in range(cols):
        x1, y1 = j * cell_size, i * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        cell = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white")
        row.append(cell)
    grid.append(row)


def on_click(event):
    global start, end
    row, col = event.y // cell_size, event.x // cell_size
    if row >= rows or col >= cols:
        return
    cell = grid[row][col]
    color = canvas.itemcget(cell, "fill")

    if not start:
        start = (row, col)
        canvas.itemconfig(cell, fill="green")  
    elif not end:
        end = (row, col)
        canvas.itemconfig(cell, fill="red") 
    elif color == "white":
        canvas.itemconfig(cell, fill="black") 
    elif color == "black":
        canvas.itemconfig(cell, fill="white")  

canvas.bind("<Button-1>", on_click)


def dijkstra(start, end):
    dist = {start: 0}
    pq = PriorityQueue()
    pq.put((0, start))
    visited = set()
    parent = {}

    while not pq.empty():
        (cost, current) = pq.get()
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        row, col = current
        neighbors = [(row+1,col), (row-1,col), (row,col+1), (row,col-1)]
        for r, c in neighbors:
            if 0 <= r < rows and 0 <= c < cols:
                color = canvas.itemcget(grid[r][c], "fill")
                if color == "black":  # Wall
                    continue
                new_cost = cost + 1
                if (r, c) not in dist or new_cost < dist[(r, c)]:
                    dist[(r, c)] = new_cost
                    pq.put((new_cost, (r, c)))
                    parent[(r, c)] = current
                    if (r, c) != end and (r, c) != start:
                        canvas.itemconfig(grid[r][c], fill="yellow")  # Visited
                        root.update()
                        time.sleep(0.02)
    return parent


def draw_path(parent, start, end):
    if end not in parent:
        tk.messagebox.showinfo("No Path", "Path not found!")
        return
    current = end
    while current != start:
        current = parent[current]
        if current == start:
            break
        canvas.itemconfig(grid[current[0]][current[1]], fill="cyan")
        root.update()
        time.sleep(0.03)


def run():
    if not start or not end:
        tk.messagebox.showwarning("Warning", "Please set Start and End nodes first!")
        return
    parent = dijkstra(start, end)
    draw_path(parent, start, end)


def reset():
    global start, end
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            canvas.itemconfig(grid[i][j], fill="white")


frame = tk.Frame(root)
frame.pack()

btn_run = tk.Button(frame, text="Run Dijkstra", bg="#4CAF50", fg="white", width=15, command=run)
btn_run.grid(row=0, column=0, padx=10, pady=10)

btn_reset = tk.Button(frame, text="Reset Grid", bg="#f44336", fg="white", width=15, command=reset)
btn_reset.grid(row=0, column=1, padx=10, pady=10)


root.mainloop()

