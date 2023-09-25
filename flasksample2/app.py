import os
import csv
from flask import Flask, render_template, request, redirect, url_for

# Create a Flask app instance
app = Flask(__name__)

# Get the directory of the current script
script_dir = os.path.dirname(__file__)
# Construct the full file path
file_path = os.path.join(script_dir, 'users.csv')
# Function to register a new user
def register_user(email, username, password):
    # Check if the user already exists in the CSV file
    if not user_exists(email, username):
        # If not, add the user to the CSV file
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, username, password])
            print("User registered successfully.")
    else:
        print("User with the same email or username already exists.")

# Function to check if a user already exists in the CSV file
def user_exists(email, username):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if email == row[0] or username == row[1]:
                return True
    return False

def login_user(email_or_username, password):
    # Check if the user exists in the CSV file and the password matches
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (email_or_username == row[0] or email_or_username == row[1]) and password == row[2]:
                return True
    return False

import csv

# Function to implement tourist actions
def handle_tourist_actions():
    print("Tourist Menu:")
    print("1. Get Travel Plan")
    print("2. Purchase Resource")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        # Option: Get Travel Plan
        direction = input("Enter the direction of the state in India: ")
        place_type = input("Enter the type of place (hill, coastal, cultural, historic, hotel, resort): ")
        recommend_places(direction, place_type)

    elif choice == "2":
        # Option: Purchase Resource
        resource_type = input("Enter the type of resource (food, daily need, room): ")
        state = input("Enter the state you want to choose (options are all Indian states): ")
        recommend_resources(resource_type, state)

    else:
        print("Invalid choice. Please select 1 or 2.")



# Function to recommend places based on direction and place type
def recommend_places(direction, place_type):
    try:
        with open('places.csv', 'r') as file:
            reader = csv.DictReader(file)
            recommended_places = []

            for row in reader:
                if direction.lower() == row['direction'].lower() and place_type.lower() == row['place_type'].lower():
                    recommended_places.append(row)

            if recommended_places:
                print("Recommended places based on your choices:")
                for place in recommended_places:
                    print(f"Place: {place['place_name']}")
                    print(f"Type of Place: {place['place_type']}")
                    print(f"State: {place['state']}")
                    print(f"Direction in India: {place['direction']}")
                    print("------------")
            else:
                print("No matching places found based on your choices.")
    except FileNotFoundError:
        print("Error: 'places.csv' file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



# Function to recommend resources based on resource type and state
def recommend_resources(resource_type, state):
    try:
        with open('resources.csv', 'r') as file:
            reader = csv.DictReader(file)
            recommended_resources = []

            for row in reader:
                if resource_type.lower() == row['resource_type'].lower() and state.lower() == row['state'].lower():
                    recommended_resources.append(row)

            if recommended_resources:
                print("Recommended resources based on your choices:")
                for resource in recommended_resources:
                    print(f"Resource Name: {resource['resource_name']}")
                    print(f"Type of Resource: {resource['resource_type']}")
                    print(f"State: {resource['state']}")
                    print(f"Resource Access Link: {resource['resource_access_link']}")
                    print("------------")
            else:
                print("No matching resources found based on your choices.")
    except FileNotFoundError:
        print("Error: 'resources.csv' file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to recommend places based on direction and place type
def recommend_places(direction, place_type):
    try:
        with open('places.csv', 'r') as file:
            reader = csv.DictReader(file)
            recommended_places = []

            for row in reader:
                if direction.lower() == row['direction'].lower() and place_type.lower() == row['place_type'].lower():
                    recommended_places.append(row)

            if recommended_places:
                print("Recommended places based on your choices:")
                for place in recommended_places:
                    print(f"Place: {place['place_name']}")
                    print(f"Type of Place: {place['place_type']}")
                    print(f"State: {place['state']}")
                    print(f"Direction in India: {place['direction']}")
                    print("------------")
            else:
                print("No matching places found based on your choices.")
    except FileNotFoundError:
        print("Error: 'places.csv' file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to recommend resources based on resource type and state
def recommend_resources(resource_type, state):
    try:
        with open('resources.csv', 'r') as file:
            reader = csv.DictReader(file)
            recommended_resources = []

            for row in reader:
                if resource_type.lower() == row['resource_type'].lower() and state.lower() == row['state'].lower():
                    recommended_resources.append(row)

            if recommended_resources:
                print("Recommended resources based on your choices:")
                for resource in recommended_resources:
                    print(f"Resource Name: {resource['resource_name']}")
                    print(f"Type of Resource: {resource['resource_type']}")
                    print(f"State: {resource['state']}")
                    print(f"Resource Access Link: {resource['resource_access_link']}")
                    print("------------")
            else:
                print("No matching resources found based on your choices.")
    except FileNotFoundError:
        print("Error: 'resources.csv' file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to allocate a resource
def allocate_resource(resource_name, state, access_link):
    try:
        with open('allocated_resources.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([resource_name, state, access_link])
        print("Resource allocated successfully.")
    except Exception as e:
        print(f"An error occurred while allocating resource: {str(e)}")

# Function to view allocated resources for the stakeholder
def view_allocated_resources():
    try:
        with open('allocated_resources.csv', 'r') as file:
            reader = csv.reader(file)
            print("Allocated Resources:")
            for row in reader:
                print(f"Resource Name: {row[0]}")
                print(f"State: {row[1]}")
                print(f"Resource Access Link: {row[2]}")
                print("------------")
    except FileNotFoundError:
        print("No allocated resources found.")
    except Exception as e:
        print(f"An error occurred while viewing allocated resources: {str(e)}")


@app.route('/get_travel_plan', methods=['GET', 'POST'])
def get_travel_plan():
    if request.method == 'POST':
        # Extract form data
        direction = request.form['direction']
        place_type = request.form['place_type']

        # Call recommend_places function and store the recommendations
        recommended_places = recommend_places(direction, place_type)

        if recommended_places:
            return render_template('recommended_places.html', places=recommended_places)
        else:
            message = "No matching places found based on your choices."
            return render_template('get_travel_plan.html', message=message)

    return render_template('get_travel_plan.html')


@app.route('/purchase_resource', methods=['GET', 'POST'])
def purchase_resource():
    if request.method == 'POST':
        # Extract form data
        resource_type = request.form['resource_type']
        state = request.form['state']

        # Call recommend_resources function and store the recommendations
        recommended_resources = recommend_resources(resource_type, state)

        if recommended_resources:
            return render_template('recommended_resources.html', resources=recommended_resources)
        else:
            message = "No matching resources found based on your choices."
            return render_template('purchase_resource.html', message=message)

    return render_template('purchase_resource.html')

@app.route('/view_allocated_resources')
def view_allocated_resources():
    # Call view_allocated_resources function to fetch allocated resources
    allocated_resources = get_allocated_resources()  # Replace with your function to fetch allocated resources

    if allocated_resources:
        return render_template('view_allocated_resources.html', resources=allocated_resources)
    else:
        message = "No allocated resources found."
        return render_template('view_allocated_resources.html', message=message)




@app.route('/')
def index():
    # Your homepage or landing page
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Implement user registration logic here
    if request.method == 'POST':
        # Extract form data
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Call register_user function with the extracted data
        register_user_result = register_user(email, username, password)

        if register_user_result:
            # Registration was successful, redirect to a success page or login page
            return redirect(url_for('login'))
        else:
            # Registration failed, display an error message
            error_message = "User with the same email or username already exists."
            return render_template('register.html', error_message=error_message)

    return render_template('register.html')

@app.route('/login')
def login():
    # Your login logic here
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
