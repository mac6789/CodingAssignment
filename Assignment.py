# Import required packages

import pip
import subprocess
import sys
import json
import config as cfg

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

# Logic to install required packages if it is not installed

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()] 

if 'pandas' in installed_packages:
    pass
else:
    pipmain(['install', 'pandas'])
import pandas as pd


# Read input transaction file from path and load json data with exception handling
try:
    with open(cfg.input_files['input_transaction_path']) as json_data:
        transactions = json.load(json_data)
except FileNotFoundError:
    print("Wrong Input_Transactions file or file path")

# Create a pandas dataframe for read json data
transaction_df = pd.DataFrame([i.values() for i in transactions],columns=transactions[1].keys())

# Read Start of the day position into pandas dataframe
try:
    start_position_df = pd.read_csv(cfg.input_files['start_day_position_path'])
except FileNotFoundError:
    print("Wrong Input_StartOfDay_Positions file or file path")
except:
    print("Empty start position input data")
    
# Group transactions of the day based on instrument and TransactionType for summation of TransactionQuantity
total_transaction_df = transaction_df.groupby(['Instrument','TransactionType']).sum().reset_index()


# function definition to calculate positions

def position_calculator(transaction_type,account_type,transaction_quantity,quantity):
    if transaction_type == "B":
        if account_type == "E":
            quantity = quantity+transaction_quantity
        elif account_type == "I":
            quantity = quantity-transaction_quantity
                
    elif transaction_type == "S":
        if account_type == "E":
            quantity = quantity-transaction_quantity
        elif account_type == "I":
            quantity = quantity+transaction_quantity
         
    return quantity

## Logic for calculation of end of day position

# Define empty dataframe and its columns to store end of day position for each instrument

endofday_position_df = []
endofday_position_df_columns = ['Instrument','Account','AccountType','Quantity','Delta']
nrow = start_position_df.shape[0]              # calculate number of rows in start position dataframe

# Iterate over rows of start day position dataframe

for i in range(0,nrow):
    instrument = start_position_df['Instrument'].values[i]
    account_type = start_position_df['AccountType'].values[i]
    quantity = start_position_df['Quantity'].values[i]
    account = start_position_df['Account'].values[i]
    
    #Find out the rows in transaction file matching instruments from start day position file
    temp = total_transaction_df.loc[total_transaction_df['Instrument'] == instrument]
    initial_quantity = quantity
    
# End of day quantity calculation logic
    
    if not temp.empty:
        for j in temp.index:
            end_quantity = position_calculator(str(temp.TransactionType[j]),str(account_type),temp.TransactionQuantity[j],quantity)
            quantity=end_quantity
        delta = quantity - initial_quantity
        endofday_position_df.append([instrument,account,account_type,end_quantity,delta])
    elif temp.empty:
        delta = quantity - initial_quantity
        endofday_position_df.append([instrument,account,account_type,quantity,delta])
output_end_of_day_position_df = pd.DataFrame(endofday_position_df, columns=endofday_position_df_columns)

# Write enf of day position file to writepath
output_end_of_day_position_df.to_csv(cfg.output_file['writepath'],index = False)