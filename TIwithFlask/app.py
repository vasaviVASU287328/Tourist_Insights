from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import re

app = Flask(__name__)
# Load user data from CSV (replace with your data file)
user_df = pd.read_csv('data/user.csv')
resource_df = pd.read_csv('data/resource.csv')
place_df = pd.read_csv('data/place.csv')
#login page executor
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']

        # Check if username or email and password match in user data
        if (((user_df['username'] == username_email) | (user_df['email'] == username_email)) & (user_df['password'] == password)).any():
            return redirect('/home')
        else:
            login_error = "Wrong username/email or password."
            return render_template('login.html', login_error=login_error)

    return render_template('login.html')

#signup page executor
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global user_df
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation checks
        if not re.match(r'^[a-zA-Z0-9]*$', username):
            signup_error = "Username can only contain letters and digits, without any special characters."
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            signup_error = "Invalid email address."
        elif not (len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[@]', password) and re.search(r'\d', password)):
            signup_error = "Password must have a maximum length of 8, contain at least one uppercase letter, '@', and a digit."
        elif password != confirm_password:
            signup_error = "Passwords do not match."
        else:
            new_user = pd.DataFrame({'full_name': [full_name], 'email': [email], 'username': [username], 'password': [password]})

            # Concatenate the new user DataFrame with the existing user_df
            user_df = pd.concat([user_df, new_user], ignore_index=True)

            # Save user data to CSV
            user_df.to_csv('data/user.csv', index=False)
            return redirect('/')

        return render_template('signup.html', signup_error=signup_error)

    return render_template('signup.html')

#travelplan
@app.route('/travelplan', methods=['GET', 'POST'])
def travelplan():
    global place_df
    print (place_df)
    if request.method == 'POST':
        direction = request.form['direction']
        place_type = request.form['place_type']

        # Filter places based on user input
        matching_places = place_df[(place_df['direction'] == direction) & (place_df['place_type'] == place_type)]
        print(matching_places)
        return render_template('travelplan.html', places=matching_places.to_dict(orient='records'))

    return render_template('travelplan.html')

@app.route('/purchase_resource', methods=['GET', 'POST'])
def purchase_resource():
    global resource_df
    if request.method == 'POST':
        state = request.form['state']
        resource_type = request.form['resource_type']

        # Filter resources based on user input
        matching_resources = resource_df[(resource_df['state'] == state) & (resource_df['resource_type'] == resource_type)]

        return render_template('purchase_resource.html', resources=matching_resources.to_dict(orient='records'))

    return render_template('purchase_resource.html')

@app.route('/upload_resource', methods=['GET', 'POST'])
def upload_resource():
    global resource_df
    # Define a list of all India states
    india_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
        "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
        "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
        "Uttarakhand", "West Bengal"
    ]

    if request.method == 'POST':
        resource_name = request.form['resource_name']
        state = request.form['state']
        resource_type = request.form['resource_type']
        resource_link = request.form['resource_link']

        # Update resource.csv
        new_resource = pd.DataFrame({
            'resource_name': [resource_name],
            'state': [state],
            'resource_type': [resource_type],
            'resource_link': [resource_link]
        })
        # Concatenate the new resource data with the existing resource_df
        resource_df = pd.concat([resource_df, new_resource], ignore_index=True)

        # Save the updated resource data to CSV
        resource_df.to_csv('data/resource.csv', index=False)

        # Update user's personal CSV file (my_resource_username.csv)
        # Replace 'username' with the actual username
        username = 'username'
        user_resource_df = pd.DataFrame({
            'resource_name': [resource_name],
            'state': [state],
            'resource_type': [resource_type],
            'resource_link': [resource_link]
        })

        user_resource_df.to_csv(f'data/my_resource_{username}.csv', index=False)

        return redirect('/home')

    return render_template('upload_resource.html')

# displays all resources
@app.route('/view_resource')
def view_resource():
    # Replace 'username' with the actual username
    username = 'username'

    try:
        # Load user's personal CSV file and get resource names
        user_resource_df = pd.read_csv(f'data/my_resource_{username}.csv')
        resource_names = user_resource_df['resource_name'].tolist()
    except FileNotFoundError:
        resource_names = []

    return render_template('view_resource.html', resource_names=resource_names)


# delete the resource
@app.route('/delete_resource', methods=['GET', 'POST'])
def delete_resource():
    # Replace 'username' with the actual username
    username = 'username'

    try:
        # Load user's personal CSV file and get resource names
        user_resource_df = pd.read_csv(f'data/my_resource_{username}.csv')
        user_resource_names = user_resource_df['resource_name'].tolist()
    except FileNotFoundError:
        user_resource_names = []

    # Load resource data from CSV
    resource_df = pd.read_csv('data/resource.csv')

    if request.method == 'POST':
        resources_to_delete = request.form.getlist('resource_to_delete')
        delete_button_values = request.form.getlist('delete_button')

        # Delete selected resources from user's personal CSV file
        user_resource_df = user_resource_df[~user_resource_df['resource_name'].isin(resources_to_delete)]
        user_resource_df.to_csv(f'data/my_resource_{username}.csv', index=False)

        # Delete selected resources from resource.csv
        resource_df = resource_df[~resource_df['resource_name'].isin(delete_button_values)]
        resource_df.to_csv('data/resource.csv', index=False)

        return redirect('/delete_resource')

    return render_template('delete_resource.html', resources=resource_df.to_dict(orient='records'))


@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
