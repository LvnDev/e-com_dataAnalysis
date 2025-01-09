import time
from logging import exception

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from PIL.ImageStat import Global
from fontTools.varLib.models import nonNone

#all global variables
loaded_data = None #global variable for the loaded data
total_transactions = None #global variable for the processed data of total transaction

unique_store_locations = [] #store any found unique store locations in an array...
unique_product_categories = [] #store any found unique product categories in an array...



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
    print("\nProcessing data...")
    global loaded_data
    time.sleep(0.5) #small wait time
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

    if usr_option == 1: #add a specific detail using transaction ID
        print("add input code to retrieve details of specific store using TransactionID...")
    elif usr_option == 2: #continue to process without needing to input transaction ID for a specific record.
        global total_transactions
        global unique_store_locations
        total_transactions = loaded_data['TransactionID'].nunique() #number of unique. will count upto how many records
        unique_store_locations = loaded_data['StoreLocation'].unique() #will store all store locations into an array.
        print(unique_store_locations)
        input("Press ENTER to continue...")
    else: #this is quit processing data
        return
def visualise_data():
    print("")
    #conducting some small experiments of making bar chart.
    '''category_sums = loaded_data.groupby("ProductCategory")['Quantity'].sum()
    plt.bar(category_sums.index, category_sums.values)
    plt.show()'''
def export_data():
    print("")

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



