import csv
import json

from gui import launch_gui #import the gui.py with the gui launcher into the main.py

# Global variables
loaded_data = None #load the data into the datasheet
total_transactions = None #find the total transaction made
unique_store_locations = [] #find unique stores
unique_product_categories = [] #find unique product categories
transaction_details = None #get whole details of a transaction detail from a user transactionID finder.
transactions_by_location = None #transactions made each location
transactions_by_category = None #transactions made in each category
revenue_by_location = None #revenue in each location
export_store_data = [] #JSON file template in the export()
total_units_sold = None #total units in all categories sold
payment_method_percentage = None #all percentage in each payment methods
avg_transaction_value = None #average transaction value
avg_customer_satisfaction_score = None #find the average satisfaction score

isProcessed = False #will turn true once all data has been processed.


# Text Interface
def start_interface(usr_choice=None):
    #user option selection
    print("\nPlease select your option:")
    print("1. Load Data")
    print("2. Process Data")
    print("3. Visualize Data (GUI)")
    print("4. Export Data")
    print("5. Exit Program")

    #will continuously prompt them this until they made their choice.
    while True:
        try:
            usr_choice = int(input("Enter your choice: "))
            if 1 <= usr_choice <= 5:
                return usr_choice
            else:
                print("Invalid choice, please pick a number between 1 and 5.")
        except ValueError:
            print("Invalid input, enter a number between 1 and 5.") #incase they did not put a interger value


def load_data(filename=None):
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
    global loaded_data, isProcessed, revenue_by_location, transaction_details, transactions_by_location, total_units_sold, payment_method_percentage, avg_transaction_value, avg_customer_satisfaction_score

    print("\nEntering data processing menu...")

    if loaded_data is None: #check if the user has loaded the data first before continuing and catching errors.
        print("No data loaded, please load data first...")
        input("Press ENTER to continue...")
        return
    else:
        print("Data loaded successfully. Processing started...")

        while True:
            try:
                print(f"\nSelect an option:\n1. Retrieve details of a specific transaction using TransactionID\n2. Continue to process data\n3. Exit processing of data")
                usr_option = int(input("Enter your choice: "))
                if 1 <= usr_option <= 3:
                    break
                else:
                    print("Invalid choice, please pick a number between 1 and 3...")
            except ValueError:
                print("Invalid choice, please pick a number between 1 and 3...")

        if usr_option == 1:  # Retrieve specific transaction details
             find_transaction_details()
        elif usr_option == 2:  # Continue to process data (revenue calculations)
            print("Processing data to calculate summary metrics...")

            total_transactions = len({row['TransactionID'] for row in loaded_data})  # Count unique transactions
            print(f"Total transactions: {total_transactions}")

            unique_store_locations = list({row['StoreLocation'] for row in loaded_data}) #Display unique store locations
            print(f"Unique store locations found: {unique_store_locations}")

            unique_product_categories = list({row['ProductCategory'] for row in loaded_data}) #Display unique Product categories
            print(f"Unique product categories found: {unique_product_categories}")

            # 1. Calculate total units sold
            total_units_sold = sum(int(row['Quantity']) for row in loaded_data if row['Quantity'].isdigit())
            print(f"Total units sold: {total_units_sold}")

            # 2. Calculate payment method percentages
            payment_methods = [row['PaymentMethod'] for row in loaded_data if 'PaymentMethod' in row]
            payment_method_counts = {method: payment_methods.count(method) for method in set(payment_methods)}
            payment_method_percentage = {
                method: (count / total_transactions) * 100 for method, count in payment_method_counts.items()}
            print("\nPayment method usage percentages:")
            for method, percentage in payment_method_percentage.items():
                print(f"{method}: {percentage:.2f}%")

            # 3. Calculate average transaction value
            total_revenue = sum(
                float(row['TotalPrice']) for row in loaded_data if row['TotalPrice'].replace('.', '', 1).isdigit())
            avg_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
            print(f"Average transaction value: £{avg_transaction_value:.2f}")

            # 4. Calculate average customer satisfaction score
            customer_satisfaction_scores = [
                int(row['CustomerSatisfaction']) for row in loaded_data if row['CustomerSatisfaction'].isdigit()]
            avg_customer_satisfaction_score = (
                sum(customer_satisfaction_scores) / len(customer_satisfaction_scores)
                if customer_satisfaction_scores else 0
            )
            print(f"Average customer satisfaction score: {avg_customer_satisfaction_score:.2f}")

            #5. Process transactions by location
            transactions_by_location = {}
            for store in unique_store_locations:
                transactions_by_location[store] = [row for row in loaded_data if row['StoreLocation'] == store]
                print(f"Processed transactions for store: {store} (Count: {len(transactions_by_location[store])})")

            # 6. Calculate revenue by location
            revenue_by_location = {}
            for row in loaded_data:
                location = row['StoreLocation']
                total_price = float(row['TotalPrice']) if row['TotalPrice'].replace('.', '', 1).isdigit() else 0
                if location not in revenue_by_location:
                    revenue_by_location[location] = 0
                revenue_by_location[location] += total_price

            print("\nRevenue by location:")
            for location, revenue in revenue_by_location.items():
                print(f"{location}: £{revenue:.2f}")

            print("\nData processing completed successfully.")
            input("Press ENTER to continue...")
            isProcessed = True
            return
        else:  # Quit processing data
            return

def find_transaction_details():
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

def load_gui():
    global isProcessed, revenue_by_location, loaded_data
    if not loaded_data:
        print("No data loaded. Please load data first.")
        input("Press ENTER to continue...")
        return

    print("Loading GUI...")

    # Ensure the data is processed before loading into gui
    if not isProcessed:
        print("data was not processed yet, cannot proceed to GUI.")
        input("Press ENTER to continue...")
        return

    launch_gui(revenue_by_location, loaded_data)  # Pass both revenue and loaded data


def export_data():
    global revenue_by_location, transactions_by_location, isProcessed, total_units_sold, payment_method_percentage, avg_transaction_value, avg_customer_satisfaction_score

    if not isProcessed or not revenue_by_location:
        print("No data processed. Please process data first.")
        input("Press ENTER to continue...")
        return

    # List the stores found
    print("\nStores found:")
    for index, store in enumerate(revenue_by_location.keys(), start=1):
        print(f"{index}. {store}")

    # Prompt the user to select a store by number
    try:
        store_choice = int(input("\nEnter the number of the store you want to export the sales summary for: "))

        # Check if the selected number is valid
        if store_choice < 1 or store_choice > len(revenue_by_location):
            print("Invalid selection, please select a valid store number.")
            input("Press ENTER to return to the main menu...")
            return

        # Get the store location based on the user's choice
        selected_store = list(revenue_by_location.keys())[store_choice - 1]

    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press ENTER to return to the main menu...")
        return

    # Ensure that the selected store exists in transactions_by_location
    if selected_store not in transactions_by_location:
        print(f"Error: No transactions found for store '{selected_store}'.")
        input("Press ENTER to return to the main menu...")
        return

    # Prepare export data for the selected store with properly formatted floats
    export_store_data = {
        "store_location": selected_store,
        "revenue": f"{revenue_by_location[selected_store]:.2f}",
        "transactions_count": len(transactions_by_location[selected_store]),
        "total_units_sold": total_units_sold,  # Total units sold is an integer, no formatting needed
        "average_transaction_value": f"{avg_transaction_value:.2f}",
        "average_customer_satisfaction_score": f"{avg_customer_satisfaction_score:.2f}",
        "payment_method_percentage": {
            method: f"{percentage:.2f}" for method, percentage in payment_method_percentage.items()
        },
    }

    print("\nExporting data...")
    generate_filename = input("Enter the filename for export (e.g., 'store_sales_summary'): ")
    try:
        with open(f"{generate_filename}.json", "w") as json_file:
            json.dump(export_store_data, json_file, indent=4)
        print(f"Sales summary for store '{selected_store}' successfully exported to '{generate_filename}.json'!")
    except Exception as e:
        print(f"An error occurred during export: {e}")

    input("Press ENTER to return to the main menu...")



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
        break
