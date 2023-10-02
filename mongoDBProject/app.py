from flask import Flask, render_template, request, redirect, url_for
import pymongo
import re
import random
app = Flask(__name__)


# Set up a connection to MongoDB
client = pymongo.MongoClient("mongodb+srv://Vasavivasu:i63KCiAIZpUzWn6X@cluster0.zevtixc.mongodb.net/?retryWrites=true&w=majority")
db = client["TouristInsights"]
user_collection = db["user"]
resource_collection = db["resource"]
place_collection = db["place"]
current_user=""
# Define a secret key for session management (replace 'your_secret_key' with an actual secret key)
app.secret_key = 'your_secret_key'

def setuser(user):
    global current_user
    current_user+=user
def getuser():
    return current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']

        # Check if username or email and password match in user data
        user = user_collection.find_one(
            {
                "$or": [{"username": username_email}, {"email": username_email}],
                "password": password
            }
        )

        if user:
            setuser(str(user["username"]))
            return redirect('/home')
        else:
            login_error = "Wrong username/email or password."
            return render_template('login.html', login_error=login_error)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
            existing_user = user_collection.find_one({"$or": [{"username": username}, {"email": email}]})
            if existing_user:
                signup_error = "Username or email is already taken."
                return render_template('signup.html', signup_error=signup_error)
            else:
                # Insert user data into MongoDB
                user_collection.insert_one({
                    "full_name": full_name,
                    "email": email,
                    "username": username,
                    "password": password
                })
                
                setuser(username)

            return render_template('home.html')

        return render_template('signup.html', signup_error=signup_error)

    return render_template('signup.html')

def generate_unique_resource_id():
    while True:
        resource_id = random.randint(1, 999)
        # Check if the resource_id already exists in the collection
        existing_resource = resource_collection.find_one({"resource_id": resource_id})
        if not existing_resource:
            return resource_id
        
@app.route('/upload_resource', methods=['GET', 'POST'])
def upload_resource():
    if request.method == 'POST':
        resource_name = request.form['resource_name']
        state = request.form['state']
        resource_type = request.form['resource_type']
        resource_link = request.form['resource_link']
        image_link=request.form['image_link']
        # Insert resource data into MongoDB
        resource_id = generate_unique_resource_id()
        resource = {
            "resource_id":resource_id,
            "resource_name": resource_name,
            "state": state,
            "resource_type": resource_type,
            "resource_link": resource_link,
            "image_link":image_link,
            "count":0
        }
        resource_collection.insert_one(resource)

        # Update user's personal MongoDB collection (my_resources) instead of a separate CSV file
        # Replace 'username' with the actual username
        username = getuser()
        user_resources = db[username + "_resources"]
        user_resources.insert_one(resource)

        return redirect('/home',user=getuser())

    return render_template('upload_resource.html')


@app.route('/view_resource')
def view_resource():
    # Replace 'username' with the actual username
    username = getuser()

    user_resources = db[username + "_resources"]
    resource=list(user_resources.find())
    return render_template('view_resource.html', resource_data=resource)

@app.route('/delete_resource', methods=['GET', 'POST'])
def delete_resource():
    # Replace 'username' with the actual username
    username = getuser()

    user_resources = db[username + "_resources"]

    if request.method == 'POST':
        resources_to_delete = request.form.getlist('resource_to_delete')
        delete_button_values = request.form.getlist('delete_button')

        # Delete selected resources from user's personal MongoDB collection
        user_resources.delete_many({"resource_name": {"$in": resources_to_delete}})


        return redirect('/delete_resource')

    # Retrieve user-specific resources for display
    user_resource_names = [resource["resource_name"] for resource in user_resources.find()]


    return render_template('delete_resource.html',user_resources=user_resource_names)


@app.route('/travelplan', methods=['GET', 'POST'])
def travelplan():
    if request.method == 'POST':
        direction = request.form['direction']
        
        place_type = request.form['place_type']
        print(direction,place_type)
        
        # Query places based on user input from the place_collection
        matching_places = place_collection.find({"direction": direction, "place_type": place_type})
        print(matching_places)
        return render_template('travelplan.html', places=list(matching_places))

    return render_template('travelplan.html')


@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    if request.method == 'POST':
        place_name = request.form['place_name']
        place_type=request.form['place_type']
        direction=request.form['direction']
        location_link = request.form['location_link']
        image_link=request.form['image_link']

        # Insert the new place into the place_collection
        new_place = {
            "place_name": place_name,
            "place_type":place_type,
            "direction":direction,
            "location_link": location_link,
            "image_link":image_link
        }
        place_collection.insert_one(new_place)

        # Redirect back to the travelplan page
        return redirect('/travelplan')

    return render_template('add_place.html')



@app.route('/purchase_resource', methods=['GET', 'POST'])
def purchase_resource():
    if request.method == 'POST':
        state = request.form['state']
        resource_type = request.form['resource_type']

        # Query resources based on user input from the resource_collection
        matching_resources = resource_collection.find({"state": state, "resource_type": resource_type})

        # Convert the cursor result to a list of dictionaries
        resources = list(matching_resources)

        # Increment count for each matched resource
        for resource in resources:
            resource_collection.update_one(
                {"_id": resource["resource_id"]},
                {"$inc": {"count": 1}}
            )

        return render_template('purchase_resource.html', resources=resources)

    return render_template('purchase_resource.html')


@app.route('/home')
def home():
    print (getuser())
    return render_template('home.html',user=getuser())
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)