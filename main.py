import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import getpass
import time
import sys

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
        process_users()
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


#def search_badge(badge_num):
#    print(f"Searching For Badge Number  {badge_num}.")
#    existing_user_search = driver.find_element(By.ID, "searchUsersText")
#    #existing_user_search.clear()
#    existing_user_search.send_keys(badge_num)
#    existing_user_search.send_keys(Keys.RETURN)
#    #check for element on the page
#    time.sleep(2)
#    user_element = driver.find_elements(By.XPATH, "//*[@id='tr0']")
#    existing_user_search.clear()
#    time.sleep(1)
#    #check if the element exists
#    if len(user_element) == 1:
#        print(f"{badge_num} already exists. Proceeding to change existing info.")
#        return True
#    else: 
#        print("User doesn't exist!")
#        return False


def process_users():
    global first_name, last_name, employ_id, badge_num, department
    # Loop through each row in Excel and add users
    for index, row in apex_users.iterrows():
        first_name = row["First Name"]
        last_name = row["Last Name"]
        employ_id = row["Badge Number"]
        
        # Check if 'Badge Number' is NaN and handle accordingly
        if pd.isna(row["Badge Number"]):
            # Option 1: Skip this user
            continue
            # Option 2: Use a default value, e.g., 0 or some placeholder
            # badge_num = 0
            # Option 3: Handle NaN differently as per your requirements
        else:
            badge_num = int(row["Badge Number"])
        
        department = row["Department"]
        
        add_user(first_name, last_name, employ_id, badge_num, department)


def add_user(first_name, last_name, employee_id, badge_num, department):
    time.sleep(2)
    print(f"Searching For Badge Number  {badge_num}.")
    existing_user_search = driver.find_element(By.ID, "searchUsersText")
    existing_user_search.click()
    existing_user_search.clear()
    existing_user_search.send_keys(badge_num)
    print("Searching..")
    existing_user_search.send_keys(Keys.RETURN)
    #check for element on the page
    time.sleep(2)
    user_element = driver.find_elements(By.XPATH, "//*[@id='tr0']")
    #existing_user_search.clear()
    time.sleep(1)
    #check if the element exists
    if len(user_element) == 1:
        print(f"{badge_num} already exists. Proceeding to change existing info.")
        last_name_element = driver.find_element(By.CSS_SELECTOR, '#tr0 > td:nth-child(1) > a:nth-child(1)')
        last_name_element.click()
        sys.exit()
    else: 
        print(f"{badge_num} doesn't exist. Adding now..")
        add_user_link = driver.find_element(By.ID, "addUserLink")
        add_user_link.click()
        f_name = driver.find_element(By.ID, "user.first_name")
        f_name.send_keys(first_name)
        l_name = driver.find_element(By.ID, "user.last_name")
        l_name.send_keys(last_name)
        emp_id = driver.find_element(By.ID, "addPassport.employee_id")
        emp_id.send_keys(employee_id)
        badge_number = driver.find_element(By.ID, "addPassport.user_card_key")
        badge_number.send_keys("0", badge_num)
        dept = driver.find_element(By.LINK_TEXT, "User Group Membership:")
        dept.click()
        time.sleep(1)
        uncheck_all_checkboxes()
        time.sleep(1)
        group_assignment(department)
        #xpath = f"//input[@id='membershipCheck{group_assignment}']"
        #checkbox = driver.find_element(By.XPATH, xpath)
        #checkbox.click()
        add_button = driver.find_element(By.XPATH, "//button[normalize-space()='Add']")
        ActionChains(driver).move_to_element(add_button).click().perform()
        time.sleep(2)
        submit = driver.find_element(By.XPATH, "//button[normalize-space()='Submit']")
        submit.click()
        popup = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/button")
        popup.click()
        print(f"User {first_name} {last_name} has been added!")
        process_users()


def uncheck_all_checkboxes():
    checkboxes = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'membershipCheck')]")
    for checkbox in checkboxes:
        if checkbox.is_selected():
            checkbox.click()


def group_assignment(group):
    if department == "Cycle Count":
        return group_selection(2)
    elif department == "General":
        return group_selection(3)
    elif department == "Material Handler":
        return group_selection(4)
    elif department == "Sort":
        return group_selection(5)
    elif department == "Voice Pick":
        return group_selection(6)
    
def group_selection(group):
    emp_group = driver.find_element(By.LINK_TEXT, "User Group Membership:")
    emp_group.click()
    
    time.sleep(1)
    
    xpath = f"//input[@id='membershipCheck{group}']"
    checkbox = driver.find_element(By.XPATH, xpath)
    checkbox.click()






login_to_apex()

