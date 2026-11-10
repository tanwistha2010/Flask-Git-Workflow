from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["FlaskDatabase"]
collection = db["students"]


# To-Do items collection
todo_collection = db["todo_items"]



# Test connection
try:
    client.admin.command('ping')
    print("MongoDB connected successfully!")

except Exception as e:
    print("MongoDB connection failed:", e)

# TASK 1: JSON API
@app.route('/api')
def api():

    with open('data.json', 'r') as file:
        data = json.load(file)

    return jsonify(data)


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Form submission
@app.route('/submit', methods=['POST'])
def submit():

    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()

        # Validate fields
        if not name or not email or not course:
            raise ValueError("All fields are required!")

        # Create student document
        student = {
            "name": name,
            "email": email,
            "course": course
        }

        # Insert into MongoDB
        collection.insert_one(student)

        # Redirect to success page
        return redirect(url_for('success'))

    except Exception as e:
        return render_template(
            'index.html',
            error=str(e),
            name=request.form.get('name', ''),
            email=request.form.get('email', ''),
            course=request.form.get('course', '')
        )


# TASK 3: Submit To-Do Item
@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():

    try:
        item_name = request.form.get('itemName', '').strip()
        item_description = request.form.get('itemDescription', '').strip()

        if not item_name or not item_description:
            return "Item Name and Item Description are required!", 400

        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        todo_collection.insert_one(todo_item)

        return "To-Do item saved successfully!"

    except Exception as e:
        return f"Error saving To-Do item: {str(e)}", 500











# Success page
@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)