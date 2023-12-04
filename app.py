from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from datetime import datetime

import sqlite3
import secrets

secret_key = secrets.token_hex(16)
app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = secret_key 


#db connection can't handle to many operation at the same time
dbCon = sqlite3.connect('Restaurant.db', check_same_thread=False)
dbCursor = dbCon.cursor()



#registration form
class RegistrationForm(FlaskForm):
    username = StringField('User Name')
    numGuest = StringField('Number of Guests')
    date = StringField('Date (YYYY-MM-DD)', validators=[validators.DataRequired()])
    time = StringField('Time (HH:MM)', validators=[validators.DataRequired()])
    submit = SubmitField('Book !')



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/bookings', methods=['GET'])
def bookings():
    try:
        dbCursor.execute("SELECT * FROM guests")
        bookings = dbCursor.fetchall()
        return render_template('bookings.html', bookings=bookings)
    except sqlite3.Error as e:
        return f"Error: {str(e)}"



@app.route('/addBooking', methods=['GET', 'POST'] )
def addBooking():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        date_str = form.date.data
        time_str = form.time.data
        numGuest = form.numGuest.data

        try:
            # Set date (YYYY-MM-DD)
            datetime_str = f"{date_str} {time_str}"
            # From string to object datetime
            booking_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            
            # Convert time to string in the desired format "HH:MM"
            time_str = booking_datetime.strftime('%H:%M')

            # Esegui l'inserimento nel database
            dbCursor.execute("INSERT INTO guests (name, date, time, numGuest) VALUES (?, ?, ?, ?)",
                             (name, booking_datetime.date(), time_str, numGuest))
            # Salva le modifiche nel database
            dbCon.commit()
            return f"{name}, your booking has been accepted!"
        except (sqlite3.Error, ValueError) as e:
            dbCon.rollback()
            app.logger.error(f"Error during booking: {str(e)}")
            return "An error occurred during booking. Please try again."

    return render_template('add_Bookings.html', form=form)




@app.route('/delete_Bookings', methods=['GET', 'POST'])
def delete_Bookings():
    if request.method == 'POST':
        idField = request.form.get('idField')
        if idField is not None:

            dbCursor.execute("DELETE FROM guests WHERE id = ?", (idField,))

            dbCon.commit()
            return f"Booking with ID {idField} deleted successfully."

    return render_template('delete_Bookings.html')





if __name__ == "__main__":
    app.run()









