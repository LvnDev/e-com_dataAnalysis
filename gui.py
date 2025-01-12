import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def launch_gui(revenue_data, loaded_data):
    if not revenue_data or not isinstance(revenue_data, dict):
        messagebox.showerror("Error", "Revenue data is not available or invalid.")
        return
    if not loaded_data or not isinstance(loaded_data, list):
        messagebox.showerror("Error", "Loaded data is not available or invalid.")
        return

    # Create the Tkinter window (root)
    root = tk.Tk()
    root.title("Revenue Visualization")
    root.geometry("900x700")  # You can adjust the window size here

    def show_pie_chart(frame):
        """Displays a pie chart of revenue contributions by store location."""
        # Clear existing content in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        total_revenue = sum(revenue_data.values())
        locations = list(revenue_data.keys())
        revenues = list(revenue_data.values())

        # Generate labels with just the location and revenue, no percentage
        labels = [f"{loc}\n£{rev:.2f}" for loc, rev in zip(locations, revenues)]

        # Create the figure for the pie chart (larger size)
        fig = Figure(figsize=(7, 6), dpi=100)
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(
            revenues,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Paired.colors
        )
        ax.set_title(f"Revenue Contribution by Store Locations\nTotal: £{total_revenue:.2f}", fontsize=12)

        # Embed the figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_histogram(frame):
        """Displays a histogram of total transaction values."""
        # Clear existing content in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Extract individual transaction values (TotalPrice)
        transaction_values = [
            float(row['TotalPrice']) for row in loaded_data if row['TotalPrice'].replace('.', '', 1).isdigit()
        ]

        # Set the number of bins and determine the bin range based on the transaction values
        num_bins = 10
        min_revenue = min(transaction_values)
        max_revenue = max(transaction_values)

        # Calculate bin size (range of each bin)
        bin_size = (max_revenue - min_revenue) / num_bins

        # Create empty bins
        bins = [0] * num_bins

        # Count how many transactions fall into each bin
        for value in transaction_values:
            bin_index = int((value - min_revenue) / bin_size)
            if bin_index == num_bins:  # Handle edge case where value is exactly max_revenue
                bin_index -= 1
            bins[bin_index] += 1

        # Calculate percentage for each bin
        total_transactions = len(transaction_values)
        percentages = [(bin_count / total_transactions) * 100 for bin_count in bins]

        # Create the figure for the histogram
        fig = Figure(figsize=(7, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Set the bin edges
        bin_edges = [min_revenue + i * bin_size for i in range(num_bins + 1)]

        # Plot the histogram with percentage on the y-axis
        ax.bar(bin_edges[:-1], percentages, width=bin_size, align='edge', color='skyblue', edgecolor='black')

        ax.set_title("Transaction Values (Histogram)", fontsize=12)
        ax.set_xlabel("Total Price (£)")
        ax.set_ylabel("Percentage of Total Transactions (%)")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Embed the figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    # Create a frame to hold the charts
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add buttons to switch between the charts
    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X)

    pie_button = tk.Button(button_frame, text="Pie Chart", command=lambda: show_pie_chart(frame))
    pie_button.pack(side=tk.LEFT, padx=5)

    hist_button = tk.Button(button_frame, text="Histogram", command=lambda: show_histogram(frame))
    hist_button.pack(side=tk.LEFT, padx=5)

    # Start the Tkinter main loop to display the window
    root.mainloop()
