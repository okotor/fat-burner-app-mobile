from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataAdapter
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from main import *
from datetime import datetime

### Login Screen
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_name = 'first_screen'

    ## Login Screen Widgets
        self.add_widget(Label(text="Login", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 1.02}))

        # User selection elements
        self.add_widget(Label(text="Choose user:", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.95}))
        self.user_spinner = Spinner(text='Select user', values=['User1', 'User2'], size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.88})
        self.user_spinner.bind(text=self.user_pick)
        self.add_widget(self.user_spinner)

        # Load users into the spinner immediately after creation
        self.users_load(self.user_spinner)

        self.add_widget(Label(text="Register a new user", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.72}))
        self.add_widget(Label(text="Please enter your username:", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.65}))
        self.username_input = TextInput(multiline=False, size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.6})
        self.add_widget(self.username_input)

        self.add_widget(Label(text="Please choose your sex:", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.55}))
        self.sex_spinner = Spinner(text='Female', values=["Female", "Male"], size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.5})
        self.add_widget(self.sex_spinner)

        self.add_widget(Label(text="Please choose your height in cm:", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.45}))
        self.height_slider = Slider(min=90, max=250, value=165, size_hint=(0.6, 0.05), pos_hint={'center_x': 0.5, 'top': 0.4})
        self.height_slider.bind(value=self.update_height_label)
        self.add_widget(self.height_slider)

        self.height_label = Label(text="Height: 165 cm", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.35})
        self.add_widget(self.height_label)

        self.add_widget(Label(text="Select your date of birth:", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.3}))

        # Date of Birth Widgets
        dob_layout = FloatLayout(size_hint=(0.6, 0.1), pos_hint={'center_x': 0.43, 'top': 0.25})
        dob_layout.add_widget(Label(text="Day:", size_hint=(0.1, 0.5), pos_hint={'center_x': 0.2, 'center_y': 0.5}))
        self.day_spinner = Spinner(text='1', values=[str(i) for i in range(1, 32)], size_hint=(0.2, 0.5), pos_hint={'center_x': 0.35, 'center_y': 0.5})
        dob_layout.add_widget(self.day_spinner)

        dob_layout.add_widget(Label(text="Month:", size_hint=(0.1, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.month_spinner = Spinner(text='01', values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], size_hint=(0.2, 0.5), pos_hint={'center_x': 0.65, 'center_y': 0.5})
        dob_layout.add_widget(self.month_spinner)

        dob_layout.add_widget(Label(text="Year:", size_hint=(0.1, 0.5), pos_hint={'center_x': 0.8, 'center_y': 0.5}))
        self.year_spinner = Spinner(text='2009', values=[str(i) for i in range(1907, 2024)], size_hint=(0.2, 0.5), pos_hint={'center_x': 0.95, 'center_y': 0.5})
        dob_layout.add_widget(self.year_spinner)

        self.add_widget(dob_layout)

        # Back to self
        self.register_button = Button(text="Register", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.15}, on_press=self.user_register)
        self.add_widget(self.register_button)

        self.username_taken_label = Label(text="", size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'top': 0.1})
        self.add_widget(self.username_taken_label)

        self.database_listbox = RecycleView(size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5, 'top': 0.1})
        self.database_listbox.data = [{'text': str(x)} for x in range(100)]
        self.add_widget(self.database_listbox)

    ## Login Screen Functions
    def users_load(self, spinner):
        # Clear the current spinner values
        spinner.values = ()  
        usernames = users_load_google_sheet()
        # Add usernames to the spinner
        spinner.values = usernames[1:]  # Skip header row

    def user_pick(self, instance, picked_user_str):
        picked_user_str = self.user_spinner.text.strip()
        picked_user = user_pick_google_sheet(picked_user_str)
        create_and_or_load_google_sheet(sheet_name=picked_user.user_sheet_str)
        app = App.get_running_app()
        app.root.current = 'second_screen'
        
    def update_height_label(self, instance, value):
        self.height_label.text = f"Height: {int(value)} cm"

    # Function to be called when the "Register" button is pressed
    def user_register(self, instance):
        username = self.username_input.text.strip()
        # Check if the username contains only alphanumeric characters and no spaces
        if not username.isalnum() or ' ' in username:
            self.username_taken_label.text = "Username contains symbols other than numbers or letters (including spaces). Please change it."
            return
        # Open the Google Sheet and worksheet
        worksheet = access_usersdata_sheet()
        existing_usernames = username_check(worksheet, username, self.username_taken_label)
        if existing_usernames == False:
            return
        # Store user data
        day = self.day_spinner.text
        month = self.month_spinner.text
        year = self.year_spinner.text
        # Format the date column as date
        dob = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
        # Create an instance of the User class
        new_user = User(username, self.sex_spinner.text, int(self.height_slider.value), dob.strftime("%d/%m/%Y"))
        user_record_create(new_user, worksheet, existing_usernames)
        self.users_load(self.user_spinner)
        self.username_taken_label.text = "User successfully registered."

### Main Screen
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_name = 'second_screen'

    ## Main Screen Widgets
        welcome_label = Label(text=f"", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 1.02})
        self.add_widget(welcome_label)

        cur_fat_lvl_head = Label(text="Please enter the sum of your three skinfold areas in millimeters (mm):", size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 1.01})
        self.add_widget(cur_fat_lvl_head)
        
        self.cur_fat_lvl_inpu = TextInput(size_hint=(0.05, 0.05), pos_hint={'center_x': 0.5, 'top': 0.94})
        self.add_widget(self.cur_fat_lvl_inpu)
        
        opt_fat_lvl_head = Label(text="Please enter your weight in kilograms (kg):", size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 0.91})
        self.add_widget(opt_fat_lvl_head)
        
        self.opt_fat_lvl_inpu = TextInput(size_hint=(0.05, 0.05), pos_hint={'center_x': 0.5, 'top': 0.84})
        self.add_widget(self.opt_fat_lvl_inpu)
        
        calculate_button = Button(text="Calculate My Current & Optimal Fat Level", size_hint=(0.4, 0.05), pos_hint={'center_x': 0.5, 'top': 0.77})
        calculate_button.bind(on_press=self.calculate_basic_user_data)
        self.add_widget(calculate_button)
        
        self.cur_fat_lvl_disp = Label(text="", size_hint=(0.6, 0.05), pos_hint={'center_x': 0.5, 'top': 0.665})
        self.add_widget(self.cur_fat_lvl_disp)
        
        self.opt_fat_lvl_disp = Label(text="", size_hint=(0.6, 0.05), pos_hint={'center_x': 0.5, 'top': 0.54})
        self.add_widget(self.opt_fat_lvl_disp)
        
        self.bmr_head = Label(text="", size_hint=(0.6, 0.05), pos_hint={'center_x': 0.5, 'top': 0.37})
        self.add_widget(self.bmr_head)
        
        self.back_button = Button(text="Store Today's User Data in a Google Sheet", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.26}, on_press=lambda instance: self.store_todays_data(instance, todays_date_str, todays_data_list))
        self.add_widget(self.back_button)

        self.td_data_disp = Label(text="", size_hint=(0.6, 0.05), pos_hint={'center_x': 0.5, 'top': 0.15})
        self.add_widget(self.td_data_disp)

        self.back_button = Button(text="Change User", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'top': 0.099}, on_press=self.user_logout)
        self.add_widget(self.back_button)

    ## Main Screen Functions
    def calculate_basic_user_data(self, instance):
        fat_data['weight'] = round(float(self.opt_fat_lvl_inpu.text), 2)
        fat_data['skinfolds_sum'] = round(float(self.cur_fat_lvl_inpu.text), 2)
        picked_user = calculate_fat_data()
        self.cur_fat_lvl_disp.text = f"Your current fat balance is:\n    {fat_data['cur_fat_lvl']}kg fat ({fat_data['cur_fat_perc']}%)\n"
        self.opt_fat_lvl_disp.text = (f"Your recommended fat balance range right now is between\n" + " " * 37 + f"{fat_data['min_opt_fat_lvl']}kg ({picked_user.minimum_optimal_body_fat_perc}%) and\n" + " " * 37 + f"{fat_data['max_opt_fat_lvl']}kg ({picked_user.maximum_optimal_body_fat_perc}%)\n\n Your optimal weight range (BMI) is between {fat_data['min_opt_weight']} and {fat_data['max_opt_weight']}kg.") 
        self.bmr_head.text = (" " * 13 + f"Without any activity,\nyou should be able to consume up to:\n" + " " * 25 + f"{fat_data['cal_main_lvl']}kcal       \n     to preserve your current weight.")

    def store_todays_data(self, instance, todays_date_str, todays_data_list):
        have_some_data = basic_calc_made_or_not()
        if have_some_data:
            worksheet = access_picked_user_google_sheet()
            date_column = worksheet.col_values(1)  # Assuming date is in the first column
            if todays_date_str in date_column:
                self.show_info_popup()
            else:
                worksheet.append_row(todays_data_list)
                self.td_data_disp.text = "Today's data stored."
        else:
            self.td_data_disp.text = "You must first calculate your current & optimal fat level."

    def show_info_popup(self):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        info_label = Label(text="Do you want to update it?")
        popup_layout.add_widget(info_label)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)

        button1 = Button(text="Yes")
        button1.bind(on_press=self.update_todays_data)

        button2 = Button(text="No")
        button2.bind(on_press=self.update_not)

        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        popup_layout.add_widget(button_layout)

        self.info_popup = Popup(title="Today's data has already been stored.", content=popup_layout, size_hint=(None, None), size=(400, 200))
        self.info_popup.open()

    def update_todays_data(self, instance):
        self.info_popup.dismiss()
        update_todays_data_google_sheet()
        self.td_data_disp.text = "Today's data updated."

    def update_not(self, instance):
        self.info_popup.dismiss()

    def user_logout(self, instance):
        # Switch back to the first screen
        app = App.get_running_app()
        app.root.current = 'first_screen'
        # Reset GUI elements
        self.cur_fat_lvl_inpu.text = ""
        self.opt_fat_lvl_inpu.text = ""
        self.cur_fat_lvl_disp.text = ""
        self.opt_fat_lvl_disp.text = ""
        self.bmr_head.text = ""
        self.td_data_disp.text = ""
        # Restart main program's variables
        user_restart()

### App
class MobileApp(App):
    def build(self):
        sm = ScreenManager()

        screen1 = Screen(name='first_screen')
        screen1.add_widget(FirstScreen())
        sm.add_widget(screen1)
        
        screen2 = Screen(name='second_screen')
        screen2.add_widget(SecondScreen())
        sm.add_widget(screen2) 
        return sm
    
if __name__ == "__main__":
    MobileApp().run()
