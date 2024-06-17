import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import getpass
import time

# Define the excel sheet for new users

apex_users = pd.read_excel("New_Apex_Users.xlsx")

# Define the global webdriver
driver = webdriver.Firefox()
# Set the window size to 1920x1080
driver.set_window_size(1920, 1080)

def login_to_apex():
    """
    Opens the webdriver, prompts for login info,
    and navigates to the User Management page.
    """
    #define the URL to connect load
    driver.get("https://apexconnectandgo.com/")
    #find the username field
    userID_element = driver.find_element(By.ID, "user.login_id")
    #clear the field in case it contains something
    userID_element.clear
    #pass the user ID
    userID_element.send_keys(input("Enter your username: "))
    #locate the password field element
    pw_element = driver.find_element(By.ID, "user.password")
    #clear the field
    pw_element.clear
        #call for the password input
    pw_element.send_keys(getpass.getpass("Enter your password: "))
    pw_element.send_keys(Keys.RETURN)
    #Give the page time to load
    time.sleep(4)
    print("Navigating to the 'Manage Users' screen.")
    #Navigate to the 'Manage Users' screen
    driver.get("https://apexconnectandgo.com/APEX-Login/accountAction_initManageuser.action?isShow=users")
    # Find a specific element on the page, if element exists, call 
    # another function.

    # Check if a specific element exists
    #ready_element = driver.find_element(By.ID, 'tab2')
    try:
        ready_element = driver.find_element(By.ID, 'tab2')
        print("Ready to continue.")
        read_user_dump()
    except NoSuchElementException:
        print("Can't find element. Are we on the right page?")
        driver.quit()
    
def read_user_dump():
    """
    Opens and reads the .xlsx file of the users to be added.
    Prints the DF and then iterates over the rows and sends to another function.
    """
    for index, row in apex_users.iterrows():
        badge_num = row["Badge Number"]
        print(badge_num)


def change_user_info():
    """
    This function is only called if a badge number is 
    already in use. If a badge number is already in use, this function will
    edit the existing information and change it to the newly
    requested information.
    
    """




login_to_apex()

