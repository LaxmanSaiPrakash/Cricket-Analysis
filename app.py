

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, make_response
import mysql.connector
from KNear import main
from progress import calci
from decimal import Decimal
from constraint import constraint

app = Flask(__name__)
app.secret_key= '123'

# Configure MySQL
mydb = mysql.connector.connect(
    host="we4techi.mysql.pythonanywhere-services.com",
    user="we4techi",
    password="Wefourtechi@1",
    database="we4techi$cricketanalytics"
)
def conn():
    mydb = mysql.connector.connect(
    host="we4techi.mysql.pythonanywhere-services.com",
    user="we4techi",
    password="Wefourtechi@1",
    database="we4techi$cricketanalytics"
    )
    return mydb
# Example suggestions
suggestions = [
    "Deepak Chahar", "Mukesh Choudhary", "M Rahman", "Tushar Deshpande", "Matheesha Pathirana",
    "Anrich Nortje", "Lungi Ngidi", "Khaleel Ahmed", "Ishant Sharma", "Jhye Richardson", "Mukesh Kumar",
    "Spencer Johnson", "Kartik Tyagi", "Joshua Little", "Mohammed Shami", "Mohit Sharma", "Umesh Yadav",
    "Vaibhav Arora", "Chetan Sakariya", "D Chameera", "Mitchell Starc", "Harshit Rana", "Jaydev Unadkat",
    "T Natarajan", "Bhuvneshwar Kumar", "Fazal Farooqi", "Pat Cummins", "Gerald Coetzee", "Jasprit Bumrah",
    "Jason Behrendorff", "Romario Shepherd", "Dilshan Madushanka", "Reece Topley", "Alzarri Joseph",
    "Mohammed Siraj", "Yash Dayal", "Lockie Ferguson", "Nathan Ellis", "Kagiso Rabada", "Arshdeep Singh",
    "Harshal Patel", "Naveen-ul-Haq", "Yash Thakur", "Avesh Khan", "Navdeep Saini", "Trent Boult",
    "Sandeep Sharma", "Prasidh Krishna", "Maheesh Theekshana", "Kuldeep Yadav", "Praveen Dubey",
    "Jayant Yadav", "Rahul Tewatia", "Rashid Khan", "Noor Ahmad", "Suyash Sharma", "Mujeeb Ur Rahman",
    "Varun Chakaravarthy", "Mayank Markande", "Piyush Chawla", "Karn Sharma", "Rahul Chahar", "Amit Mishra",
    "Ravi Bishnoi", "Y Chahal", "Adam Zampa", "R Jadeja", "M Santner", "Moeen Ali", "Shivam Dube",
    "Rachin Ravindra", "Shardul Thakur", "Daryl Mitchell", "Axar Patel", "Lalit Yadav", "Mitchell Marsh",
    "Vijay Shankar", "Anukul Roy", "Venkatesh Iyer", "S Rutherford", "Andre Russell", "Sunil Narine",
    "Washington Sundar", "Shahbaz Ahmed", "Abhishek Sharma", "Marco Jansen", "Hardik Pandya", "M Nabi",
    "Shreyas Gopal", "Glenn Maxwell", "Mahipal Lomror", "Cameron Green", "Tom Curran", "Liam Livingstone",
    "Sikandar Raza", "Harpreet Brar", "Sam Curran", "Rishi Dhawan", "Chris Woakes", "Krunal Pandya",
    "Ayush Badoni", "Marcus Stoinis", "Deepak Hooda", "Krishnappa Gowtham", "Shivam Mavi", "David Willey",
    "Riyan Parag", "R Ashwin", "MS Dhoni", "Rishabh Pant", "Tristan Stubbs", "Shai Hope", "Abhishek Porel",
    "David Miller", "Manish Pandey", "Ramandeep Singh", "Rinku Singh", "Srikar Bharat", "Glenn Phillips",
    "Anmolpreet Singh", "Abdul Samad", "Heinrich Klaseen", "Nehal Wadhera", "Tim David", "Dewald Brevis",
    "Suyash Prabhudessai", "Dinesh Karthik", "Rilee Rossouw", "Jitesh Sharma", "Nicholas Pooran",
    "Shimron Hetmyer", "Rovman Powell", "Dhruv Jurel", "Devon Conway", "Ruturaj Gaikwad", "David Warner",
    "Prithvi Shaw", "Shubhman Gill", "Wriddhiman Saha", "Matthew Wade", "Rahmanullah Gurbaz", "Jason Roy",
    "KL Rahul", "Devdutt Padikkal", "Quinton de Kock", "Kyle Mayers", "Rohit Sharma", "Ishan Kishan",
    "Shikhar Dhawan", "Jonny Bairstow", "Prabhsimran Singh", "Yashasvi Jaiswal", "Jos Buttler",
    "Anuj Rawat", "Faf du Plessis", "Will Jacks", "Ajinkya Rahane", "Kane Williamson", "Harry Brook",
    "Shreyas Iyer", "Nitish Rana", "SuryaKumar Yadav", "Tilak Varma", "Sanju Samson", "Virat Kohli",
    "Rajat Patidhar", "Rahul Tripathi", "Aiden Markram", "Travis Head",
    # Added players
    "Mayank Agarwal", "Kohler Cadmore", "Atharva Taide", "Jake Fraser-McG", "Raghuvanshi",
    "Ashutosh Sharma", "Naman Dhir", "Samir Rizvi", "Shaik Rasheed", "Upendra Yadav", "Phill Salt",
    "Abhinav Manohar", "Swapnil Singh", "Arjun Tendulkar", "Shakib Al Hasan", "Sai Sudarshan",
    "Omarzai", "Ashton Turner", "Nithish Reddy", "Shahrukh Khan", "Shashank Singh",
    "Keshav Maharaj", "Sai Kishore", "Allah Ghazanfar",
    "Jofra Archer", "Kuldeep Sen", "Shemar Joseph", "Matt Henry", "Rasikh Dar", "Simarjeet Singh",
    "Mayank Yadav", "Mohsin Khan"
]



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username.lower()
    mydb = conn()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    print(user)
    if user:
        # User exists, redirect to the home page
        if username == "admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('newhome'))
    else:
        # User doesn't exist or incorrect password, redirect back to login page
        return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form
        if 'verify' in data.values():
            return redirect(url_for('verify'))
        if 'logout' in data.values():
            return redirect(url_for('login'))
        print(data)
        cat = list(data.values())[0]  # Convert dict_values object to list and access the first element
        session['cat'] = cat
        print(cat)
        return redirect(url_for('preview'))
    return render_template('admin.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        data = request.form
        if 'admin' in data.values():
            return redirect(url_for('admin'))
        username = data['data0']
        player_name = data['data1']
        sold_price = data['data2']
        if sold_price==None:
            return redirect(url_for(similar))
        mydb = conn()
        cursor = mydb.cursor()
        cursor.execute("""
            SELECT 'TopOrder' AS category FROM TopOrder WHERE player = %s
            UNION ALL
            SELECT 'MiddleOrder' AS category FROM MiddleOrder WHERE player = %s
            UNION ALL
            SELECT 'AllRounder' AS category FROM AllRounder WHERE player = %s
            UNION ALL
            SELECT 'Spinner' AS category FROM Spinner WHERE player = %s
            UNION ALL
            SELECT 'Pacer' AS category FROM Pacer WHERE player = %s
        """, (player_name, player_name, player_name, player_name, player_name))

        category = cursor.fetchone()
        print("Category: ", category)
        cursor.close()
        if 'accept' in data.values():
            # Create a cursor object
            mydb = conn()
            cursor = mydb.cursor()

            # Check if the player already exists in the table
            query = "SELECT COUNT(*) FROM {} WHERE player = %s".format(username)
            cursor.execute(query, (player_name,))
            result = cursor.fetchone()
            if result[0] == 0:
                # Create a cursor object
                mydb = conn()
                cursor = mydb.cursor()

                # Insert the new row
                insert_query = "INSERT INTO {} (player, category, sold_price) VALUES (%s, %s, %s);".format(username)
                cursor.execute(insert_query, (player_name, category[0], sold_price))
                mydb.commit()
                update_query = "UPDATE category SET isSold = TRUE WHERE player = %s"
                cursor.execute(update_query, (player_name,))
                mydb.commit()

            # Delete the corresponding row from the verify table
            delete_query = "DELETE FROM verify WHERE username = %s AND player = %s AND sold_price = %s AND category = %s;"
            cursor.execute(delete_query, (username, player_name,sold_price,category[0]))
            mydb.commit()

            # Fetch all rows from the verify table
            cursor.execute("SELECT * FROM verify")
            verify_player = cursor.fetchall()

            # Close the cursor
            cursor.close()
        if 'reject' in data.values():
            mydb = conn()
            cursor = mydb.cursor()
            delete_query = "DELETE FROM verify WHERE username = %s AND player = %s AND sold_price = %s AND category = %s;"
            cursor.execute(delete_query, (username, player_name,sold_price,category[0]))
            mydb.commit()

            # Fetch all rows from the verify table
            cursor.execute("SELECT * FROM verify")
            verify_player = cursor.fetchall()

            # Render the template with the result
        return render_template('verify.html', verify_player=verify_player)
    mydb = conn()
    cursor = mydb.cursor()
    cursor.execute("Select * from verify")
    verify_player = cursor.fetchall()
    cursor.close()
    return render_template('verify.html', verify_player=verify_player)

@app.route('/clear-tables', methods=['POST'])
def clear_tables():
    entered_password = request.form.get('password')
    correct_password = 'admin'

    if entered_password == correct_password:
        return clear_tables_post()
    else:
        print('Incorrect password. Please try again.')
        return redirect(url_for('verify'))  # Redirect back to the page with the form

def clear_tables_post():
    # List of tables and players to retain in each table
    tables_with_exceptions = {
        'bangalore': ["Virat Kohli", "Rajat Patidhar", "Yash Dayal"],
        'chennai': ["Ruturaj Gaikwad", "Matheesha Pathirana", "Shivam Dube", "R Jadeja", "MS Dhoni"],
        'delhi': ["Abhishek Porel", "Tristan Stubbs", "Axar Patel", "Kuldeep Yadav"],
        'hyderabad': ["Pat Cummins", "Abhishek Sharma", "Heinrich Klaseen", "Travis Head","Nithish Reddy"],
        'kolkata': ["Rinku Singh", "Varun Chakaravarthy", "Sunil Narine", "Andre Russell", "Harshit Rana", "Ramandeep Singh"],
        'mumbai': ["Jasprit Bumrah", "SuryaKumar Yadav", "Tilak Varma", "Rohit Sharma", "Hardik Pandya"],
        'punjab': ["Prabhsimran Singh","Shashank Singh"],
        'lucknow': ["Mayank Yadav","Ravi Bishnoi","Nicholas Pooran","Mohsin Khan","Ayush Badoni"],
        'rajasthan': ["Yashasvi Jaiswal", "Sanju Samson", "Riyan Parag", "Dhruv Jurel", "Shimron Hetmyer", "Sandeep Sharma"],
        'gujarat': ["Rashid Khan", "Shubhman Gill", "Rahul Tewatia","Sai Sudarshan","Shahrukh Khan"]

    }

    # Check if the form is submitted via POST
    if request.method == 'POST':
        # Get the MySQL connection
        mydb = conn()  # Assuming conn() is a function that returns a MySQL connection object
        cursor = mydb.cursor()

        try:
            # Iterate through the table list and delete all rows from each table, excluding the specified players
            for table, players_to_keep in tables_with_exceptions.items():
                # Create a condition to exclude players from deletion
                exclude_condition = " AND ".join([f"Player != '{player}'" for player in players_to_keep])
                delete_query = f"DELETE FROM {table} WHERE {exclude_condition}" if exclude_condition else f"DELETE FROM {table}"

                cursor.execute(delete_query)
                mydb.commit()# Commit after each deletion to ensure changes are saved

            exclude_players_condition = " AND ".join([f"Player != '{player}'" for player in players_to_keep])
            update_query = f"""
                UPDATE category
                SET isSold = 0
                WHERE {exclude_players_condition}
            """
            cursor.execute(update_query)
            mydb.commit()
            print("All rows cleared from specified tables, except the ones specified.")
            return redirect(url_for('verify'))

        except Exception as e:
            print(f"Error clearing tables: {e}")
            return f"An error occurred: {e}"

        finally:
            cursor.close()
            mydb.close()

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    cat = session.get('cat')
    print(cat)
    mydb = conn()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM {}".format(cat))
    rows = cursor.fetchall()
    cursor.close()
    dataset=[]
    for row in rows:
        if row[1] == "TopOrder" or row[1] == "MiddleOrder":
            mydb = conn()
            cursor = mydb.cursor()
            query = "SELECT player, overseas, credits, wicket_keeper FROM {} WHERE player = %s"
            cursor.execute(query.format(row[1]), (row[0],))
            result = cursor.fetchone()
            cursor.close()
            result_with_extra_info = (row[2],) + result + (row[1],)
            dataset.append(result_with_extra_info)
        else:
            mydb = conn()
            cursor = mydb.cursor()
            query = "SELECT player, overseas, credits FROM {} WHERE player = %s"
            cursor.execute(query.format(row[1]), (row[0],))
            result = cursor.fetchone()
            cursor.close()
            result_with_extra_info = (row[2],) + result + (0,)+ (row[1],)
            dataset.append(result_with_extra_info)
    const = []
    const = constraint(dataset)
    return render_template('preview.html', dataset=dataset, const=const)

@app.route('/newhome', methods= ['GET', 'POST'])
def newhome():
    return render_template('newhome.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact_us.html')

@app.route('/analysis')
def analysis():
    if request.method == 'POST':
        data = request.get_json()
        team_name = data.get('team')
    else:
        # For GET requests, use query parameter (fallback)
        team_name = request.args.get('team')

    if not team_name:
        return "Team not specified", 400

    # Process the team_name as needed
    print(f"Team selected: {team_name}")

    # cat = session.get('cat')
    # if not cat:
    #     return "Category not set in session", 400

    mydb = conn()
    cursor = mydb.cursor()

    try:
        cursor.execute("SELECT * FROM {}".format(team_name))
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching data for category {team_name}: {e}")
        return "Error retrieving data", 500
    finally:
        cursor.close()

    dataset = []
    for row in rows:
        try:
            if row[1] in ["TopOrder", "MiddleOrder"]:
                query = "SELECT player, overseas, credits, wicket_keeper FROM {} WHERE player = %s"
            else:
                query = "SELECT player, overseas, credits FROM {} WHERE player = %s"

            cursor = mydb.cursor()
            cursor.execute(query.format(row[1]), (row[0],))
            result = cursor.fetchone()
            cursor.close()

            if row[1] in ["TopOrder", "MiddleOrder"]:
                result_with_extra_info = (row[2],) + result + (row[1],)
            else:
                result_with_extra_info = (row[2],) + result + (0,) + (row[1],)

            dataset.append(result_with_extra_info)
        except Exception as e:
            print(f"Error processing row {row}: {e}")
    sold_price=[float(row[2]) for row in rows]
    print(sold_price)
    total_sold_price=sum(sold_price)
    if team_name not in ['kolkata','delhi']:
        rem_purse=120-total_sold_price
        print("Total sold price:", total_sold_price)
    elif team_name=='kolkata':
        rem_purse=108-total_sold_price
        print("Total sold price:", total_sold_price)
    elif team_name=='delhi':
        rem_purse=116.75-total_sold_price
    rem_purse=round(rem_purse,2)
    const=constraint(dataset)
    return render_template('analysis.html', dataset=dataset, const=const, rem_purse=rem_purse)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.form
        print(data)

        # Handle logout
        if 'logout' in data.values():
            return redirect(url_for('login'))

        # Handle search inputs
        if 'searchInput' in data.keys():
            player = request.form['searchInput']
            mydb = conn()
            cursor = mydb.cursor()
            cursor.execute("SELECT category, isSold FROM category WHERE player = %s", (player,))
            player_fetch = cursor.fetchone()
            if player_fetch:
                category, isSold = player_fetch
                session['category'] = category
                session['player'] = player
                session['isSold'] = isSold  # Store issold in the session
                # Redirect to the similar page with the player name
                return redirect(url_for('similar', player=player))
            return redirect(url_for('newhome'))

        elif 'searchInput1' in data.keys():
            player = request.form['searchInput1']
            mydb = conn()
            cursor = mydb.cursor()
            cursor.execute("SELECT category, isSold FROM category WHERE player = %s", (player,))
            player_fetch = cursor.fetchone()
            if player_fetch:
                category, isSold = player_fetch
                session['category'] = category
                session['player'] = player
                session['isSold'] = isSold  # Store issold in the session
                # Redirect to the similar page with the player name
                return redirect(url_for('similar', player=player))
            return redirect(url_for('similar'))

@app.route('/similar', methods=['GET', 'POST'])
def similar():
    if request.method == 'POST':
        data = request.form
        if 'roster' in data.values():
            return redirect(url_for('remain'))
        if 'search' in data.values():
            return redirect(url_for('home'))
        if 'logout' in data.values():
            return redirect(url_for('login'))
        stats= session.get('stats')
        category= session.get('category')
        isSold = session.get('isSold')
        print("isSold value: ", session.get('isSold'))
        player_name = stats[0]
        mydb = conn()
        cursor = mydb.cursor()

        # Execute query based on category
        if category in ["TopOrder", "MiddleOrder", "AllRounder", "Spinner", "Pacer"]:
            cursor.execute(f"SELECT * FROM {category}")
            dataset = cursor.fetchall()
        else:
            print("Invalid category")

        query = []
        indices = []
        c = 0
        query.append(player_name)
        print(request.form)
        rupees_value = None
        for key, value in data.items():
            if key == 'rupees':
                print(value)
                rupees_value = value
            else:
                indices.append(value)
        print(indices)
        print("Rupees: ", rupees_value)
        username = session.get('username')
        mydb = conn()
        cursor = mydb.cursor()
        cursor.execute("SELECT sold_price FROM {}".format(username))
        sold_prices = [row[0] for row in cursor.fetchall()]
        total_sold_price = sum(sold_prices)
        print("Total sold price:", total_sold_price)
        if rupees_value is not None:
            rupees_value_num = Decimal(rupees_value)
            total_sold_price += rupees_value_num
        print(total_sold_price)
        if rupees_value is not None and total_sold_price<=120:
            try:
                mydb = conn()
                cursor = mydb.cursor()

                # Check if the player already exists in the table
                query = "SELECT COUNT(*) FROM {} WHERE player = %s".format(username)
                cursor.execute(query, (player_name,))
                result = cursor.fetchone()
                # If player does not exist, insert the new record
                if result[0] == 0:
                    mydb = conn()
                    cursor = mydb.cursor()
                    insert_query = "INSERT INTO verify (username, player, sold_price, category, sufficient) VALUES (%s, %s, %s, %s, 1);"
                    cursor.execute(insert_query, (username, player_name, rupees_value, category))
                    mydb.commit()

                    print("Record inserted into verify table successfully.")
                else:
                    print("Player already exists in the table. Skipping insertion.")

            except mysql.connector.Error as err:
                print("Error:", err)
                mydb.rollback()  # Rollback changes in case of error
        elif total_sold_price>120:
            mydb = conn()
            cursor = mydb.cursor()
            insert_query = "INSERT INTO verify (username, player, sold_price, category, sufficient) VALUES (%s, %s, %s, %s, 0);"
            cursor.execute(insert_query, (username, player_name, rupees_value, category))
            mydb.commit()

        if category == "MiddleOrder" or category == "TopOrder":
            if '1' in indices:
                for x in dataset:
                    if x[0] == player_name:
                        query.append(x[1])
                        print(query)
                        c=c+1
                        break
            if '3' in indices:
                if c==1:
                    query.append(x[3])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[3])
                            print(query)
                            c=c+1
                            break
            if '4' in indices:
                if c==1:
                    query.append(x[4])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[4])
                            print(query)
                            c=c+1
                            break
            if '6' in indices:
                if c==1:
                    query.append(x[6])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[6])
                            print(query)
                            c=c+1
                            break
            if '7' in indices:
                if c==1:
                    query.append(x[7])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[7])
                            print(query)
                            c=c+1
                            break
            if '8' in indices:
                if c==1:
                    query.append(x[8])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[8])
                            print(query)
                            c=c+1
                            break
        elif category == "AllRounder":
            if '3' in indices:
                for x in dataset:
                    if x[0] == player_name:
                        query.append(x[3])
                        print(query)
                        c=c+1
                        break
            if '8' in indices:
                if c==1:
                    query.append(x[8])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[8])
                            print(query)
                            c=c+1
                            break
            if '10' in indices:
                if c==1:
                    query.append(x[10])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[10])
                            print(query)
                            c=c+1
                            break
            if '11' in indices:
                if c==1:
                    query.append(x[11])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[11])
                            print(query)
                            c=c+1
                            break
            if '7' in indices:
                if c==1:
                    query.append(x[7])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[7])
                            print(query)
                            c=c+1
                            break
            if '9' in indices:
                if c==1:
                    query.append(x[9])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[9])
                            print(query)
                            c=c+1
                            break
            if '1' in indices:
                if c==1:
                    query.append(x[1])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[1])
                            print(query)
                            c=c+1
                            break
            if '4' in indices:
                if c==1:
                    query.append(x[4])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[4])
                            print(query)
                            c=c+1
                            break
            if '6' in indices:
                if c==1:
                    query.append(x[6])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[6])
                            print(query)
                            c=c+1
                            break
        else:
            if '4' in indices:
                for x in dataset:
                    if x[0] == player_name:
                        query.append(x[4])
                        print(query)
                        c=c+1
                        break
            if '5' in indices:
                if c==1:
                    query.append(x[5])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[5])
                            print(query)
                            c=c+1
            if '3' in indices:
                if c==1:
                    query.append(x[3])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[3])
                            print(query)
                            c=c+1
                            break
            if '1' in indices:
                if c==1:
                    query.append(x[1])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[1])
                            print(query)
                            c=c+1
                            break
            if '6' in indices:
                if c==1:
                    query.append(x[6])
                    print(query)
                else:
                    for x in dataset:
                        if x[0] == player_name:
                            query.append(x[6])
                            print(query)
                            c=c+1
                            break
        indices= [int(index) for index in indices]
        if(len(indices)==0):
            return redirect(url_for('similar'))
        selected_data = [[t[index] for index in indices] for t in dataset]
        #print(len(selected_data))
        if rupees_value is None:
            neighbors = main(query,dataset, selected_data, k=10, distance_metric='euclidean')
        else:
            neighbors= None
        return render_template('similar.html',category=category,data=stats, neighbors=neighbors,isSold=isSold)
    player_name = session.get('player')  # Retrieve player name from query parameter
    print(player_name)
    #issold=session.get('issold')
    mydb = conn()
    cursor = mydb.cursor()
    category= session.get('category')
    if category == "TopOrder":
        cursor.execute("SELECT player, average, strike_rate, predicted FROM TopOrder WHERE player=%s", (player_name,))
        stats = cursor.fetchone()
    if category == "MiddleOrder":
        cursor.execute("SELECT player, average, strike_rate, predicted FROM MiddleOrder WHERE player=%s", (player_name,))
        stats = cursor.fetchone()
    if category == "AllRounder":
        cursor.execute("SELECT player, Batting_Average, Batting_strike_rate, predicted FROM AllRounder WHERE player=%s", (player_name,))
        stats = cursor.fetchone()
    if category == "Spinner":
        cursor.execute("SELECT player, avg, sr, predicted FROM Spinner WHERE player=%s", (player_name,))
        stats = cursor.fetchone()
    if category == "Pacer":
        cursor.execute("SELECT player, avg, sr, predicted FROM Pacer WHERE player=%s", (player_name,))
        stats = cursor.fetchone()
    print(stats)
    session['stats'] = stats
    isSold = session.get('isSold')
    print("isSold value: ", session.get('isSold'))
    neighbors = None  # Default value if neighbors are not calculated
    username = session.get('username')
    mydb = conn()
    cursor = mydb.cursor()
    cursor.execute("SELECT sold_price FROM {}".format(username))
    sold_prices = [row[0] for row in cursor.fetchall()]
    total_sold_price = sum(sold_prices)
    print("Total sold price:", total_sold_price)
    session['total_sold_price']= total_sold_price
    return render_template('similar.html',category= category,data=stats, neighbors=neighbors,isSold=isSold)

@app.route('/franchise', methods=['GET', 'POST'])
def franchise():
    franchise_name = session.get('username')
    mydb = conn()
    cursor = mydb.cursor()
    cursor.execute("SELECT player,sold_price FROM {}".format(franchise_name))
    rows = cursor.fetchall()
    players=[row for row in rows]
    print(players)
    sold_price=[float(row[1]) for row in rows]
    print(sold_price)
    total_sold_price=sum(sold_price)
    if franchise_name not in ['kolkata','delhi']:
        rem_purse=120-total_sold_price
        print("Total sold price:", total_sold_price)
    elif franchise_name=='kolkata':
        total_price=108
        rem_purse=total_price-total_sold_price
    elif franchise_name=='delhi':
        total_price=116.75
        rem_purse=total_price-total_sold_price
    rem_purse = round(rem_purse, 2)
    return render_template('franchisehome.html', players=players,rem_purse=rem_purse)
@app.route('/suggestions',methods=['GET'])
def get_suggestions():
    query = request.args.get('query', '')
    if query:
        filtered_suggestions = [s for s in suggestions if query.lower() in s.lower()]
        return jsonify(filtered_suggestions[:5])  # Limiting to 5 suggestions
    else:
        return jsonify([])
if __name__ == '__main__':
    app.run(debug=True)
