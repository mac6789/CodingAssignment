# CodingAssignment

### Config.py file is developed to specify each file paths ####
A. Please specify file paths in config.py file in following sequence

      1) In front of variable name "input_transaction_path" please specify input_transaction.txt file path
      2) In front of variable name "start_day_position_path" please specify Input_StartOfDay_Positions.txt file path
      3) In front of variable name "writepath" please specify file name and path where you want to write your output file

B. For Windows systems Paths should be separated with "\\\\"

C. For linux systems Paths must be separated with "/"

### Assignment.py file contains main logic to calculate end of the day positions ###

D. The code will first install required packages ("Pandas" package will be installed in first run if it is not installed on your system)

E. Please note that the code is developed on python version 3.0 and above

F. "Output_EndOfDay_Positions" file is the file generated with the code . This file matches with        "Expected_EndOfDay_Positions" file
