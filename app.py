import pandas as pd
import numpy as np
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Load the CSV files
book_data = pd.read_csv('Book3.csv')
plant_data = pd.read_csv('Plant Data.csv')  # In case you need to use it later

# Constants
RECOVERY_OF_MANGANESE = 0.85  # Fixed recovery value per the new requirement

# Function to calculate final manganese content
def calculate_final_mn(grade, mn_type, initial_mn, amount_of_metal):
    # Fetch the range for manganese content based on the grade from Book3
    grade_data = book_data[book_data['Grade'] == grade]
    if grade_data.empty:
        return None, None  # Return None if grade not found

    mn_min = grade_data['Mn_min'].values[0]
    mn_max = grade_data['Mn_max'].values[0]

    # Select random manganese content based on the type
    if mn_type == "HC-Mn":
        ferroalloy_mn = np.random.uniform(0.78, 0.9)
    elif mn_type == "LC-Mn":
        ferroalloy_mn = np.random.uniform(0.6, 0.72)
    else:
        return None, None  # Invalid type

    # Select a random manganese content within the grade range
    range_mn_content = np.random.uniform(mn_min, mn_max)

    # # Apply the updated formula
    # mn_content = (((range_mn_content - initial_mn) / 100) * amount_of_metal * 1000) 
    # final_mn_content = mn_content / (ferroalloy_mn * RECOVERY_OF_MANGANESE)
    
    # # Calculate the final manganese percentage
    # final_mn_percentage = (final_mn_content / (amount_of_metal * 1000)) * 100

    # return final_mn_content, final_mn_percentage

    mn_content = (((range_mn_content - initial_mn) / 100) * amount_of_metal * 1000) 
    final_mn_content = mn_content / (ferroalloy_mn * RECOVERY_OF_MANGANESE)

    # # Calculate the final manganese percentage
    final_mn_percentage = (final_mn_content / (amount_of_metal * 1000)) * 100
    fnm = initial_mn + final_mn_percentage

    return final_mn_content, fnm

# Flask route to handle the prediction
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grade = request.form.get('grade')
        mn_type = request.form.get('mn_type')
        initial_mn = float(request.form.get('initial_mn'))
        amount_of_metal = float(request.form.get('amount_of_metal'))

        # Call the calculation function
        final_mn_content, final_mn_percentage = calculate_final_mn(
            grade, mn_type, initial_mn, amount_of_metal
        )

        # Pass the result to the frontend
        return render_template('index.html', final_mn_content=final_mn_content,
                               final_mn_percentage=final_mn_percentage)

    # Load grades for dropdown
    grades = book_data['Grade'].unique()
    return render_template('index.html', grades=grades)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
