import pandas as pd
import matplotlib.pyplot as plt
import csv
import sqlite3
from prettytable import PrettyTable


import tkinter as tk
from tkinter import messagebox

#****************************************
print("WELCOME".center(90))
user_data = []  # List to store user details

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("social_db.sqlite")  # Corrected the database file name
cursor = conn.cursor()


############################################################################
# Function to enter user details
def userinsert():
    print("Enter User Details:")
    name = input("Enter your name: ")
    while True:
        age_input = input("Enter your age: ")
        if age_input.isdigit():  # Check if input is a valid integer
            age = int(age_input)
            break
        else:
            print("Invalid input. Please enter a valid age.")

    country = input("Enter your country: ")
    state = input("Enter your state: ")
    email = input("Enter your email_id: ")

    social_media_usage = {}
    social_media_platforms = ["Facebook", "WhatsApp", "Instagram", "Snapchat", "YouTube"]

    for platform in social_media_platforms:
        while True:
            try:
                usage = float(input(f"Enter how much time you spend on {platform} (in hours): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        social_media_usage[platform] = usage

    user_details = {
        "Name": name,
        "Age": age,
        "Country": country,
        "State": state,
        "Email": email,
        "Social Media Usage": social_media_usage
    }
    user_data.append(user_details)  # Add user details to the list

  
   # Insert user details into the 'users' table
    cursor.execute('''INSERT INTO users (name, age, country, state, email, facebook, whatsapp, instagram, snapchat, youtube)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, age, country, state, email, social_media_usage["Facebook"],
                   social_media_usage["WhatsApp"], social_media_usage["Instagram"],
                   social_media_usage["Snapchat"], social_media_usage["YouTube"]))

    # Commit changes to the database
    conn.commit()

    print("User details saved successfully.")
    return user_details

############################################################################################

# Function to view user details in a table format
def view_user():
    conn = sqlite3.connect("social_db.sqlite")  # Corrected the database file name
    cursor = conn.cursor()

    # Fetch user data from the 'users' table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Create a PrettyTable for displaying the data
    table = PrettyTable()
    table.field_names = ["User ID", "Name", "Age", "Country", "State", "Email", "Facebook (hours)", "WhatsApp (hours)", "Instagram (hours)", "Snapchat (hours)", "YouTube (hours)"]

    for user in users:
        table.add_row([user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10]])

    if len(users) > 0:
        print("User Details from Database:")
        print(table)
    else:
        print("No user data found in the database.")

###########################################################################################
# Function to update user details in the database
def userupdate():
    global conn  # Declare conn as a global variable to use the existing database connection

    # Display users for selection
    view_user()  # Reuse the view_user() function to display user details
    user_index = int(input("Enter the user ID to update: "))

    cursor = conn.cursor()

    # Fetch user data based on the entered user ID
    cursor.execute("SELECT * FROM users WHERE id=?", (user_index,))
    user = cursor.fetchone()

    if user:
        print(f"Editing details for User {user[0]}: {user[1]}")
        # Allow user to update specific fields
        new_name = input(f"Enter new name (or press Enter to keep existing '{user[1]}'): ") or user[1]
        new_age = int(input(f"Enter new age (or press Enter to keep existing '{user[2]}'): ") or user[2])
        new_country = input(f"Enter new country (or press Enter to keep existing '{user[3]}'): ") or user[3]
        new_state = input(f"Enter new state (or press Enter to keep existing '{user[4]}'): ") or user[4]
        new_email = input(f"Enter new email (or press Enter to keep existing '{user[5]}'): ") or user[5]

        # Update user details in the database
        cursor.execute('''UPDATE users
                          SET name=?, age=?, country=?, state=?, email=?
                          WHERE id=?''',
                       (new_name, new_age, new_country, new_state, new_email, user_index))

        conn.commit()
        print("User details updated successfully in the database.")
    else:
        print("Invalid user ID. No changes were made.")



###############################################################################################

# Function to delete user based on user ID
def userdelete():
    global conn  # Declare conn as a global variable to use the existing database connection

    # Display users for selection
    view_user()  # Reuse the view_user() function to display user details
    user_index = int(input("Enter the user ID to delete: "))

    cursor = conn.cursor()

    # Check if the user with the given ID exists in the database
    cursor.execute("SELECT * FROM users WHERE id=?", (user_index,))
    user = cursor.fetchone()

    if user:
        confirmation = input(f"Are you sure you want to delete User ID {user[0]}: {user[1]}? (yes/no): ").lower()
        if confirmation == "yes":
            # Delete the user from the database
            cursor.execute("DELETE FROM users WHERE id=?", (user_index,))
            conn.commit()
            print("User deleted successfully from the database.")
        else:
            print("User was not deleted.")
    else:
        print("Invalid user ID. No changes were made.")




##########################################################################################
# Function to review a specific user based on time spent on each social media platform
def performance_user_by_id():
    global conn  # Declare conn as a global variable to use the existing database connection

    # Display users for selection
    view_user()  # Reuse the view_user() function to display user details
    user_id = int(input("Enter the user ID to review: "))

    cursor = conn.cursor()

    # Fetch user data for the selected user
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user:
        print(f"Review for User ID {user_id}: {user[1]}")
        print("Time spent on each social media platform:")
        print(f"Facebook: {user[6]} hours")
        print(f"WhatsApp: {user[7]} hours")
        print(f"Instagram: {user[8]} hours")
        print(f"Snapchat: {user[9]} hours")
        print(f"YouTube: {user[10]} hours")
    else:
        print("Invalid user ID. No review available.")



######################################################################################################################

# Function to calculate average time spent on social media platforms and provide a review comment
def average_time_and_review():
    global conn  # Declare conn as a global variable to use the existing database connection

    cursor = conn.cursor()

    # Display users for selection
    view_user()  # Reuse the view_user() function to display user details
    user_id = int(input("Enter the user ID to calculate average time and provide review: "))

    # Fetch user data for the selected user
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user:
        total_time = sum(user[6:])  # Summing social media usage hours starting from the 7th column

        # Calculate average time
        average_time = total_time / len(user[6:])  # Divide total time by the number of social media platforms

        # Provide review comment based on average time
        print(f"Average time spent on social media platforms: {average_time:.2f} hours")
        if average_time <= 5:
            print("Excellent! You have a healthy social media usage.")
        elif average_time <= 7:
            print("Moderate usage. Consider balancing your time spent on social media.")
        else:
            print("High usage! It's important to limit your social media time for better productivity.")
    else:
        print("Invalid user ID. No review available.")

#######################################################################################################################

# Function to draw a pie chart for social media usage based on user ID
def draw_pie_chart():
    global conn  # Declare conn as a global variable to use the existing database connection

    cursor = conn.cursor()

    # Display users for selection
    view_user()  # Reuse the view_user() function to display user details
    user_id = int(input("Enter the user ID to draw a pie chart for social media usage: "))

    # Fetch social media usage data for the selected user ID
    cursor.execute("SELECT facebook, whatsapp, instagram, snapchat, youtube FROM users WHERE id=?", (user_id,))
    social_media_data = cursor.fetchone()

    if social_media_data:
        platforms = ["Facebook", "WhatsApp", "Instagram", "Snapchat", "YouTube"]
        usage_hours = list(social_media_data)

        # Draw a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(usage_hours, labels=platforms, autopct='%1.1f%%', startangle=140)
        plt.title(f"Social Media Usage for User ID {user_id}")
        plt.show()
    else:
        print("Invalid user ID. No social media usage data available.")


##########################################################################################################################

# Function to draw a line graph for average time spent on social media platforms and average age
def draw_line_graph():
    global conn  # Declare conn as a global variable to use the existing database connection

    cursor = conn.cursor()

    # Fetch social media usage data and age data
    cursor.execute("SELECT facebook, whatsapp, instagram, snapchat, youtube FROM users")
    social_media_data = cursor.fetchall()

    cursor.execute("SELECT age FROM users")
    age_data = cursor.fetchall()

    # Calculate average time spent on each social media platform and average age
    avg_social_media_time = [sum(hours) / len(hours) for hours in zip(*social_media_data)]
    

    # Social media platforms and corresponding labels for the line graph
    platforms = ["Facebook", "WhatsApp", "Instagram", "Snapchat", "YouTube"]
    values = avg_social_media_time 

    # Draw a line graph
    plt.figure(figsize=(10, 5))
    plt.plot(platforms, values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    plt.xlabel("Social Media Platforms")
    plt.ylabel("Average Time (hours)")
    plt.title("Average Time Spent on Social Media Platforms")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

#######################################################################################################
    
# Function to draw a horizontal bar graph for number of users per country
def draw_bar_graph():
    global conn  # Declare conn as a global variable to use the existing database connection

    cursor = conn.cursor()

    # Fetch country data
    cursor.execute("SELECT country, COUNT(*) FROM users GROUP BY country")
    country_data = cursor.fetchall()

    # Extract countries and corresponding user counts for the horizontal bar graph
    countries = [country[0] for country in country_data]
    user_counts = [count[1] for count in country_data]

    # Draw a horizontal bar graph
    plt.figure(figsize=(10, 6))
    plt.barh(countries, user_counts, color='skyblue')
    plt.xlabel("Number of Users")
    plt.ylabel("Country")
    plt.title("Number of Users per Country")
    plt.grid(axis='x')
    plt.show()

    
##########################################################################################################################


# Function to draw a vertical bar graph for number of users in different age groups
def draw_age_group_bar_graph():
    global conn  # Declare conn as a global variable to use the existing database connection

    cursor = conn.cursor()

    # Fetch age data
    cursor.execute("SELECT age FROM users")
    age_data = cursor.fetchall()

    # Define age groups (for example: 0-18, 19-35, 36-50, 51+)
    age_groups = ["0-18", "19-35", "36-50", "51+"]
    age_counts = [0, 0, 0, 0]

    # Count the number of users in each age group
    for age in age_data:
        if 0 <= age[0] <= 18:
            age_counts[0] += 1
        elif 19 <= age[0] <= 35:
            age_counts[1] += 1
        elif 36 <= age[0] <= 50:
            age_counts[2] += 1
        else:
            age_counts[3] += 1

    # Draw a vertical bar graph
    plt.figure(figsize=(8, 6))
    plt.bar(age_groups, age_counts, color='lightgreen')
    plt.xlabel("Age Groups")
    plt.ylabel("Number of Users")
    plt.title("Number of Users in Different Age Groups")
    plt.grid(axis='y')
    plt.show()
##########################################################################################################################
def MenuSet():
    while True:
        print("Press 1: To Enter User Details")
        print("Press 2: To Update User Records")
        print("Press 3: To View User Details")
        print("Press 4: To Delete User Details")
        print("Press 5: To View User Performance Report")
        print("Press 6: To Provide Review")
        print("Press 7: To See Pie Chart of User time spent in Social Media")
        print("Press 8: Line Graph to see Average Time Spent on Social Media Platforms")
        print("Press 9: Horizontal Graph to see Number of Users per Country")
        print("Press 10: Vertical Bar Graph to see Number of Users in Different Age Groups")
        print("Press 11: To Exit The Menu")
       
        userinput = int(input("Please Select an Above Option: "))
        if userinput == 1:
            user_details = userinsert()  # Call userinsert() and store the returned user details
            print("User details saved successfully:")
            print(user_details)  # Print the user details
        elif userinput == 2:
            updated_user = userupdate()  # Call userupdate() and store the returned user data
        elif userinput == 3:
             view_user()
        elif userinput == 4:
            userdelete()
        elif userinput == 5:
           performance_user_by_id()
        elif userinput == 6:
           average_time_and_review()   
        elif userinput == 7:
            draw_pie_chart()
        elif userinput == 8:
            draw_line_graph()
        elif userinput == 9:
            draw_bar_graph()
        elif userinput == 10:
            draw_age_group_bar_graph()
        elif userinput == 11:
            print("Thank You")
            break
        else:
            print("Invalid Option. Please try again.")

# Call the MenuSet function to start the program
MenuSet()

####################################################################################################################


conn.close()










                

        
        
        
    
