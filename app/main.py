from config import *
from users import User

### Login Window Functions

def access_usersdata_sheet():
    # Define the Google Sheet and worksheet
    USERSDATA_SHEET_NAME = 'usersdata'  # The name of the Google Sheet
    USERSDATA_WORKSHEET_NAME = 'users'  # The name of the worksheet in the Google Sheet
    spreadsheet = gc.open(USERSDATA_SHEET_NAME)
    worksheet = spreadsheet.worksheet(USERSDATA_WORKSHEET_NAME)
    return worksheet

def users_load_google_sheet():
    # Open the Google Sheet and worksheet
    worksheet = access_usersdata_sheet()
    # Retrieve user data from the Google Sheet
    try:
        # Fetch all usernames from the first column
        usernames = worksheet.col_values(1)
        return usernames
    except Exception as e:
        print(f"An error occurred while retrieving data: {e}")
        return

def user_pick_google_sheet(picked_user_str):
    worksheet = access_usersdata_sheet()
    cell = worksheet.find(picked_user_str)
    row = cell.row
    values = worksheet.row_values(row)
    picked_user = User(values[0], values[1], float(values[2]), values[3])
    picked_user_dict["picked_user_obj"] = picked_user
    print(f"User details: {picked_user.username}, {picked_user.sex}, {picked_user.height}, {picked_user.birthdate}, {picked_user.age}")
    print(picked_user_dict)
    return picked_user

def create_and_or_load_google_sheet(sheet_name):
    try:
        worksheet = get_or_create_user_sheet(sheet_name)
        if not worksheet:
            return False  # Handle failure
        existing_headers = worksheet.row_values(1)
        calculations_headings = ["Date (DD/MM/YYYY)", "Weight (in kg)", "Skinfolds Sum (in mm)", "Body Fat (in %)", 
                    "Fat Free Body Mass (in %)", "Body Fat (in kg)", "Fat Free Body Mass (in kg)",
                    "Day Activity Intensity", "Day Activity Duration", "Day Calories Burned",
                    "Day Calories Consumed", "Day Fat Burned (in kg)"
                    ]
        headers_to_add = [header for header in calculations_headings if header not in existing_headers]
        if headers_to_add:
            worksheet.append_row(headers_to_add)
            print(f"Added calculations headings to {sheet_name} sheet.")
        return True
    except HttpError as e:
        print(f"API Error occurred: {e}")
        return False

def get_or_create_user_sheet(sheet_name):
    try:
        # Filter spreadsheets by folder_id
        spreadsheet_list = gc.list_spreadsheet_files()
        for spreadsheet in spreadsheet_list:
            if spreadsheet['name'] == sheet_name and folder_id in get_parents(spreadsheet['id']):
                print("User's data spreadsheet already exists. It has been loaded.")
                return gc.open_by_key(spreadsheet['id']).sheet1
        new_spreadsheet = create_google_sheet(sheet_name, folder_id)
        if new_spreadsheet:
            return new_spreadsheet.sheet1
        else:
            return None
    except HttpError as e:
        print(f"Error accessing Google Sheets API: {e}")
        return None

def get_parents(file_id):
    file = drive_service.files().get(fileId=file_id, fields='parents').execute()
    return file.get('parents', [])

def create_google_sheet(sheet_name, folder_id):
    # Returns the worksheet object of the new sheet, or None on error.
    try:
        # Create the spreadsheet directly in the desired folder
        file_metadata = {
            'name': sheet_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        print("User's data spreadsheet has been created.")
        # Return the Spreadsheet object itself, not sheet1 directly
        return gc.open_by_key(file['id'])
    except Exception as e:
        print(f"Error creating Google Sheet '{sheet_name}': {e}")
        return None

def username_check(worksheet, username, username_taken_text):
    # Check for existing usernames in Google Sheets
    existing_usernames = worksheet.col_values(1)
    if username in existing_usernames:
        username_taken_text.value = "This username is already in use. Try a different one."
        return False
    return existing_usernames

def user_record_create(new_user, worksheet, existing_usernames):
    # Store in the Google Sheet
    user_data_list = [new_user.username, new_user.sex, new_user.height, new_user.birthdate, str(new_user.age)]
    worksheet.append_row(user_data_list)

def read_data_from_google_sheet(display_database_listbox):
    display_database_listbox.clear()
    # Open the Google Sheet and worksheet
    worksheet = access_usersdata_sheet()
    # Retrieve all data from the Google Sheet
    data = worksheet.get_all_values()
    data_list = []
    for line in data[1:]:  # Skip header row
        # Convert list to string and remove punctuations
        string_stripped = ' '.join(line).translate(str.maketrans('', '', string.punctuation))
        # Add to array
        data_list.append(string_stripped)
    for row in data_list:
        display_database_listbox.append(row)

## MAIN WINDOW Functions
#A subroutine restarting all variables
def user_restart():
    #Restart variable status
    clear_dict_or_list(fat_data)
    print(fat_data)
    clear_dict_or_list(todays_data_list)
    print(todays_data_list)

# Function to clear the dictionary
def clear_dict_or_list(dictionary_or_list):
    dictionary_or_list.clear()
            
## Basic Data Box: Calculate quintessential data based on weight and skinfold_sum
def calculate_fat_data():
    weight = fat_data['weight']
    skinfolds_sum = fat_data['skinfolds_sum']
    picked_user = picked_user_dict["picked_user_obj"]
    fat_data['bmr'] = round(weight * 24.2, 2)
    fat_data['cal_main_lvl'] = round(float(fat_data['bmr'] * 1.2), 2)
    if picked_user.sex == "Male":
        body_density = 1.10938 - (0.0008267 * skinfolds_sum) + (0.0000016 * (skinfolds_sum ** 2)) - (0.0002574 * picked_user.age_in_years)
    else:
        body_density = 1.0994921 - (0.0009929 * skinfolds_sum) +  (0.0000023 * (skinfolds_sum ** 2)) - (0.0001392 * picked_user.age_in_years)
    fat_data['cur_fat_perc'] = round((495 / body_density) - 450, 2)
    fat_data['cur_fat_lvl'] = round(weight / 100 * fat_data['cur_fat_perc'], 2)
    fat_data['cur_non_fat_perc'] = round(100 - fat_data['cur_fat_perc'], 2)
    fat_data['cur_non_fat_lvl'] = round(weight - fat_data['cur_fat_lvl'], 2)
    fat_data['min_opt_fat_lvl'] = round(weight / 100 * picked_user.minimum_optimal_body_fat_perc, 2)
    fat_data['min_opt_non_fat_lvl'] = round(weight / 100 * (100 - picked_user.maximum_optimal_body_fat_perc), 2)
    fat_data['max_opt_fat_lvl'] = round(weight / 100 * picked_user.maximum_optimal_body_fat_perc, 2)
    fat_data['max_opt_non_fat_lvl'] = round(weight / 100 * (100 - picked_user.maximum_optimal_body_fat_perc), 2)
    fat_data['min_opt_weight'] = round(((picked_user.height / 100) ** 2) * 18.5, 2)
    fat_data['max_opt_weight'] = round(((picked_user.height / 100) ** 2) * 24.9, 2)
    fat_data['nd_weight_loss'] = round(float(weight - fat_data['max_opt_weight']), 2)
    fat_data['nd_weight_loss_cal'] = round(fat_data['nd_weight_loss'] * 1000 * 7.716179, 2)
    fat_data['nd_fat_loss'] = round(fat_data['cur_fat_lvl'] - fat_data['max_opt_fat_lvl'], 2)
    todays_data_list.clear()
    todays_data_list.append(str(todays_date_str))
    todays_data_list.append(str(weight))
    todays_data_list.append(str(skinfolds_sum))
    todays_data_list.append(str(fat_data['cur_fat_perc']))
    todays_data_list.append(str(fat_data['cur_non_fat_perc']))
    todays_data_list.append(str(fat_data['cur_fat_lvl']))
    todays_data_list.append(str(fat_data['cur_non_fat_lvl']))
    return picked_user

## Storing data in a list, append to Google Sheets
#DATA TO BE STORED
#1 Date (DD/MM/YYYY)
#2 Weight (in kg)
#3 Skinfolds Sum (in mm)
#4 Body Fat (in %)
#5 Fat Free Body Mass (in %)
#6 Body Fat (in kg)
#7 Fat Free Body Mass (in kg)
#8 Day Activity Intensity
#9 Day Activity Duration
#10 Day Calories Burned
#11 Day Calories Consumed
#12 Day Fat Burned

def access_picked_user_google_sheet():
    picked_user = picked_user_dict['picked_user_obj']
    spreadsheet = gc.open(picked_user.user_sheet_str)
    worksheet = spreadsheet.sheet1
    return worksheet
    
#Check if the necessary calculations have been made
def basic_calc_made_or_not():
    if 'weight' in fat_data:
        return True
    else:
        return False

def update_todays_data_google_sheet():
    worksheet = access_picked_user_google_sheet()
    # Get all values from the sheet
    data = worksheet.get_all_values()
    worksheet.delete_rows(len(data))
    # Append today's data to the sheet
    worksheet.append_row(todays_data_list)

### Login Window Variables
# None

### Main Window Variables
todays_date_str = dt.date.today().strftime("%d-%m-%Y") #this is a string
todays_date_obj = dt.date.today() #this is an object

### Main Window Lists / Dictionaries

#Activity factor list logic
#SEDENTARY <1.6
   #1.0 - sitting quietly, 1.5 - intense brain activity
#LIGHT 1.6-3
    #2.3, 2.5, 2.8, 2.9
#MODERATE 3-6 (up to 60 minutes)
    #3.0, 3.3, 3.5, 3.8, 4.0, 4.3, 4.4, 4.5, 4.8, 5.0, 5.3, 5.5, 5.8, 6.0
#VIGOROUS 6-9 (up to 30 minutes)
    #6.5, 7.0, 8.0, 8.5, 9.0
#HIGH >9 (up to 10 minutes)
    #10.0, 11.0, 12.0, 12.5, 14.0, 16.0, 16.5

# storing user object
picked_user_dict = {}
# picked_user's weight and fat data & ensuing calculations
fat_data = {}
# storing user day data to be appended to Google Sheets
todays_data_list = []

act_int_list = [
    ["0-59 minutes", "0-0.5 hours", "0-29 minutes", "0-14 minutes", "0-5 minutes"],
    ["1-2.5 hours", "1-2 hours", "30-59 minutes", "15-44 minutes", "6-29 minutes"],
    ["3-5.5 hours", "2.5 hours", "60-150 minutes", "45-89 minutes", "30-44 minutes"],
    ["6-12 hours", "2.5-8 hours", "3-4.5 hours", "1.5-2 hours", "45-89 minutes"],
    ["12.5-15 hours", "", "5-10 hours", "2.5-3 hours", "1.5-2.5 hours"],
    ["", "", "", "3.5-8 hours", "3-3.5 hours"],
    ["", "", "", "8.5-12 hours", "4-4.5 hours"],
    ["", "", "", "", "5-8 hours"],
    ["", "", "", "", "8.5-13 hours"]
]
act_typ_list = ["Light exercise", "Light-moderate exercise", "Moderate exercise",
                        "Moderate-intense exercise", "Intense exercise"]
act_fac_list = [1.2, 1.3, 1.4, 1.5, 1.6, 1.65, 1.725, 1.85, 1.95]
day_act_text = (f"{act_typ_list[0]}: light walking, light housework, playing frisbee, light gardening work…)\n\n{act_typ_list[1]}: playing frisbee, playing catch, walking moderately fast\n\n{act_typ_list[2]}: jogging slowly, biking slowly, dancing a basic dance, difficult household chores\n\n{act_typ_list[3]}: weight lifting, semi-intense cardio, swimming, jogging, tennis, aerobics, pilates, …\n\n{act_typ_list[4]}: heavy cardio, intense football, basketball, daily crossfit, non-stop running at 70-80% speed")

