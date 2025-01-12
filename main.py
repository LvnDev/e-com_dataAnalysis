#main.py
import csv
import time
import json
import tkinter as tk
import os

from gui import launch_gui

# Global variables
loaded_data = None
total_transactions = None
unique_store_locations = []
unique_product_categories = []
transaction_details = None
transactions_by_location = None
transactions_by_category = None
revenue_by_location = None
export_store_data = []
isProcessed = False


# Text Interface
def start_interface():
    print("\nPlease select your option:")
    print("1. Load Data")
    print("2. Process Data")
    print("3. Visualize Data (GUI)")
    print("4. Export Data")
    print("5. Exit Program")

    while True:
        try:
            usr_choice = int(input("Enter your choice: "))
            if 1 <= usr_choice <= 5:
                return usr_choice
            else:
                print("Invalid choice, please pick a number between 1 and 5.")
        except ValueError:
            print("Invalid input, enter a number between 1 and 5.")


def load_data():
    global loaded_data
    filename = input("\nEnter the filename of the CSV (case sensitive, without .csv extension): ")
    try:
        with open(f"{filename}.csv", "r") as file:
            csv_reader = csv.DictReader(file)
            loaded_data = list(csv_reader)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    input("Press ENTER to continue...")


def process_data():
    global loaded_data, isProcessed, revenue_by_location, transaction_details

    print("\nEntering data processing menu...")
    time.sleep(0.5)

    if loaded_data is None:
        print("No data loaded, please load data first...")
        input("Press ENTER to continue...")
        return
    else:
        print("Data loaded successfully. Processing started...")

        while True:
            try:
                print(
                    f"\nSelect an option:\n1. Retrieve details of a specific store using TransactionID\n2. Continue to process data\n3. Exit processing of data")
                usr_option = int(input("Enter your choice: "))
                if 1 <= usr_option <= 3:
                    break
                else:
                    print("Invalid choice, please pick a number between 1 and 3...")
            except ValueError:
                print("Invalid choice, please pick a number between 1 and 3...")

        if usr_option == 1:  # Retrieve specific transaction details
            while True:
                tid = input("Enter valid TransactionID: ")
                try:
                    print(f"Searching for TransactionID {tid}...")
                    transaction = next((row for row in loaded_data if row['TransactionID'] == tid), None)
                    if not transaction:
                        print("TransactionID not found.")
                    else:
                        transaction_details = transaction
                        print(f"Transaction found! Details for Transaction ID {tid}:")
                        for key, value in transaction_details.items():
                            print(f"{key}: {value}")
                        input("Press ENTER to continue...")
                        return process_data()  # Return to processing menu
                except ValueError:
                    print("Invalid TransactionID, please enter a numeric value.")

        elif usr_option == 2:  # Continue to process data (revenue calculations)
            print("Processing data to calculate summary metrics...")

            global total_transactions
            global unique_store_locations
            global unique_product_categories

            total_transactions = len({row['TransactionID'] for row in loaded_data})  # Count unique transactions
            print(f"Total transactions: {total_transactions}")

            unique_store_locations = list({row['StoreLocation'] for row in loaded_data})
            print(f"Unique store locations found: {unique_store_locations}")

            unique_product_categories = list({row['ProductCategory'] for row in loaded_data})
            print(f"Unique product categories found: {unique_product_categories}")

            print("\nProcessing transactions by location...")
            transactions_by_location = {}
            for store in unique_store_locations:
                transactions_by_location[store] = [row for row in loaded_data if row['StoreLocation'] == store]
                print(f"Processed transactions for store: {store} (Count: {len(transactions_by_location[store])})")

            print("\nProcessing transactions by category...")
            transactions_by_category = {}
            for category in unique_product_categories:
                transactions_by_category[category] = [row for row in loaded_data if row['ProductCategory'] == category]
                print(
                    f"Processed transactions for category: {category} (Count: {len(transactions_by_category[category])})")

            print("\nCalculating revenue by location...")
            revenue_by_location = {}
            for store in unique_store_locations:
                total_revenue = sum(float(row['TotalPrice']) for row in transactions_by_location[store] if
                                    row['TotalPrice'].replace('.', '', 1).isdigit())
                revenue_by_location[store] = total_revenue
                print(f"Revenue calculated for store {store}: £{total_revenue:.2f}")

            print("\nData processing completed successfully.")
            input("Press ENTER to continue...")
            isProcessed = True
            return
        else:  # Quit processing data
            return


def load_gui():
    global isProcessed, revenue_by_location, loaded_data
    if not isProcessed:
        print("No data processed. Please process data first.")
        input("Press ENTER to continue...")
        return

    print("Loading GUI...")
    time.sleep(1)

    # Ensure the data is valid before passing it to the GUI
    if not revenue_by_location:
        print("Revenue data is missing, cannot proceed to GUI.")
        input("Press ENTER to continue...")
        return

    launch_gui(revenue_by_location, loaded_data)  # Pass both revenue and loaded data

def export_data():
    global export_store_data, isProcessed

    if not isProcessed:
        print("No data processed. Please process data first.")
        input("Press ENTER to continue...")
        return

    print("\nExporting data...")
    generate_filename = input("Enter the filename for export (e.g., 'summary_data'): ")
    try:
        with open(f"{generate_filename}.json", "w") as json_file:
            json.dump(export_store_data, json_file, indent=4)
        print(f"Data successfully exported to '{generate_filename}.json'!")
    except Exception as e:
        print(f"An error occurred during export: {e}")

    input("Press ENTER to return to the main menu...")


def gui_main():
    print("GUI not implemented in CSV-only mode.")
    input("Press ENTER to continue...")


# Main program loop
while True:
    option = start_interface()

    if option == 1:
        load_data()
    elif option == 2:
        process_data()
    elif option == 3:
        load_gui()
    elif option == 4:
        export_data()
    elif option == 5:
        print("Exiting program...")
        time.sleep(1)
        break
