import time
from logging import exception

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

from PIL.ImageStat import Global
from PIL.SpiderImagePlugin import iforms
from fontTools.varLib.models import nonNone

#all global variables
loaded_data = None #global variable for the loaded data
total_transactions = None #global variable for the processed data of total transaction (will be used for visualisations)

unique_store_locations = [] #store any found unique store locations in an array... (will be used for visualisations)
unique_product_categories = [] #store any found unique product categories in an array... (will be used for visualisations)
transaction_details = None #a transaction of a single record that is used by a unique transactionID (will be used for visualisations)

transactions_by_location = None #all transactions by each location (will be used for visualisations)
transactions_by_category = None #all transactions by each category (will be used for visualisations)

revenue_by_location = None #total revenue made by location (will be used for visualisations)

export_store_data = [] #this will be used to store retail data into JSON file.

def start_interface():
    print(f"\nPlease select your option \n 1. Load Data \n 2. process data \n 3. visualise data \n 4. export data \n 5. exit program")
    while True: #will continue to repeat if user continuously fail choosing the correct option.
        try:
            usr_choice = int(input("Enter your choice: "))
            if 1 <= usr_choice <= 5:
                return usr_choice
            else:
                print("Invalid choice, please pick the number between 1 and 5...")
        except ValueError: #catch if any input was not integer.
            print("Invalid input, enter a number with the following options: 1-5...")

def load_data(): #load data
    filename = input("\n CASE SENSITIVE do not worry about adding .csv in the end \n Enter a .CSV file name: ")
    global loaded_data
    try: #if no issues will continue as normal
        loaded_data = pd.read_csv(f"{filename}.csv")
        print(f"{loaded_data.head()}")
        input("Press ENTER to continue...")
        return
    except FileNotFoundError: #if not found then user returns to the options screen again
        print("File not found")
        input("Press ENTER to continue...")
        return
    except Exception as e: #if some error happens the exception will pop up here and explain what the error may be.
        print(f"unexpected error: {e}")
        input("Press ENTER to continue...")
        return

def process_data():
    print("\nentering data processing menu...")
    global loaded_data
    time.sleep(0.5) #small wait time
    if loaded_data is None: #checking if data is not loaded
        print("No data loaded, please load data first...")
        input("Press ENTER to continue...")
        return
    else:
        while True:
            try: #small validation to prevent user stopping the program.
                print(f"\n select an option... \n 1. retrieve details of specific store using TransactionID \n 2. continue to process data \n 3. exit processing of data")
                usr_option = int(input("Enter your choice: "))
                if 1 <= usr_option <=3:
                    break;
                else:
                    print("Invalid choice, please pick the number between 1 and 3...")
            except ValueError:
                print("Invalid choice, please pick a number between 1 and 3...")

        if usr_option == 1: #add specific record using transaction ID
            while True:
                tid = input("Enter valid TransactionID: ")
                try:
                    if int(tid) not in loaded_data['TransactionID'].values:
                        print("TransactionID not found")
                    else:
                        global transaction_details
                        details = loaded_data[loaded_data['TransactionID'] == int(tid)] #match the transaction ID in the record
                        print(f"Saving Transaction details:\n")
                        print(details.to_string(index=False)) #prints into a full row of the matching transaction ID
                        transaction_details = details.to_string(index=False)
                        input("Press ENTER to continue...")
                        return process_data() #will return to processing selection option screen
                except ValueError:
                    print("invalid TransactionID, please enter a numeric value...")
        elif usr_option == 2: #continue to process without needing to input transaction ID for a specific record.
            global total_transactions
            global unique_store_locations
            global unique_product_categories

            global transactions_by_location
            global transactions_by_category
            usr_option = None #reset usr options
            total_transactions = loaded_data['TransactionID'].nunique() #number of unique. will count upto how many records
            unique_store_locations = loaded_data['StoreLocation'].unique() #will store all store locations into an array.
            unique_product_categories = loaded_data['ProductCategory'].unique() #will store all product category into an array
            print(f"Total transactions: {total_transactions}")
            print(f"Unique stores: {unique_store_locations}")

            for store in unique_store_locations:
                transactions_by_location = loaded_data[loaded_data['StoreLocation'] == store]
            #transactions in unique stores table
            usr_option = input("Do you want to show table for total transactions in unique stores? (y/n): ")
            if usr_option.lower() == "y":
                for store in unique_store_locations:
                    transactions_by_location = loaded_data[loaded_data['StoreLocation'] == store]
                    print(f"\nStore: {store}")
                    print(transactions_by_location.to_string(index=False))
                    print("-" * 150)
                    time.sleep(1.5)
            usr_option = None #reset usr option

            for category in unique_product_categories:
                transactions_by_category = loaded_data[loaded_data['ProductCategory'] == category]
            #transaction in unique categories table
            usr_option = input("Do you want to show table for total transactions in unique categories? (y/n): ")
            if usr_option.lower() == "y":
                for category in unique_product_categories:
                    transactions_by_category = loaded_data[loaded_data['ProductCategory'] == category]
                    print(f"\nCategory: {category}")
                    print(transactions_by_category.to_string(index=False))
                    print("-" * 150)
                    time.sleep(1.5)

            global revenue_by_location #group all store locations by total revenue.
            revenue_by_location = loaded_data.groupby('StoreLocation')['TotalPrice'].sum()
            print(f"Total revenue by store location: ")
            for store, revenue in revenue_by_location.items():
                print(f"store: {store} | total revenue: £{revenue:.2f}") #only need 2 decimal points

            summary_of_sales_for_store()
            input("Press ENTER to continue...")
            return
        else: #this is quit processing data
            return
def summary_of_sales_for_store(): #summary of a sale for specific store.
    global loaded_data, export_store_data
    print("\nsummary of sales for specific store location")

    for store in enumerate(unique_store_locations, 1):
        print(f"Store: {store}") #have user to pick the following store location.
    while True:
        try:
            store_input = int(input("Enter the number of a store location: "))
            if 1 <= store_input <= len(unique_store_locations):
                selected_store = unique_store_locations[store_input - 1]
                break
            else:
                print("Invalid store, please pick a number between 1 and 3...")
        except ValueError:
            print("Invalid store, please pick a number between 1 and 3...")

    print(f"Generating summary for {selected_store}...\n")

    store_data = loaded_data[loaded_data['StoreLocation'] == selected_store] #match users response with the following store locations array.

    store_total_transactions = store_data['TransactionID'].nunique() #find total number of transactions made
    store_total_revenue = store_data['TotalPrice'].sum() #add all the total prices in each transaction in store
    avg_transactions_store = store_total_revenue / total_transactions if total_transactions > 0 else 0 #calculate the average transactions
    store_total_quantity_sold = store_data['Quantity'].sum() #sum all the quantity sold...
    store_avg_customer_satisfaction =  store_data['CustomerSatisfaction'].mean() #find the average of customer satisfaction
    store_payment_method_distribution = store_data['PaymentMethod'].value_counts(normalize=True) * 100 #find the percentage of total payment methods used.

    summary_data_of_store = {
        "StoreLocation": str(selected_store),
        "TotalTransactions": int(store_total_transactions),
        "TotalRevenue": round(float(store_total_revenue), 2),
        "AverageTransactionsSold": round(float(avg_transactions_store), 2),
        "TotalQuantitySold": int(store_total_quantity_sold),
        "AverageCustomerSatisfaction": round(float(store_avg_customer_satisfaction), 2),
        "PaymentMethodDistribution": {str(k): round(float(v), 2) for k, v in store_payment_method_distribution.items()},
    }
    export_store_data.append(summary_data_of_store)
    print("Summary:")
    print(json.dumps(summary_data_of_store, indent=4))

def visualise_data():
    print("")
    #conducting some small experiments of making bar chart.
    '''category_sums = loaded_data.groupby("ProductCategory")['Quantity'].sum()
    plt.bar(category_sums.index, category_sums.values)
    plt.show()'''
def export_data():
    global export_store_data
    print("\nExport data...")

    if not export_store_data:
        print("No export data to export... please process the data before exporting.")
        input("Press ENTER to continue...")
        return
    generate_filename = input("Enter the filename for the export (e.g, 'summary_data') \n")
    try:
        with open(f"{generate_filename}.json", "w") as json_file:
            json.dump(export_store_data, json_file, indent=4)
        print(f"data successfully exported to '{generate_filename}.json'!")
    except exception as e:
        print(f"an error has occurred during export... {e}")

    input("Press ENTER to return to main menu...")

#user pick the following option
while True: #added a while so that it wouldn't exit the program if user wants to perform more actions in the other options...
    option = start_interface()

    if option == 1:
        load_data()
    if option == 2:
        process_data()
    if option == 3:
        visualise_data()
    if option == 4:
        export_data()
    if option == 5:
        print("Exiting program...")
        time.sleep(1)
        exit()



