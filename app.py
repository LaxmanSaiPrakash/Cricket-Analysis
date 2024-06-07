from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mysql.connector
from KNear import main
from progress import calci
from decimal import Decimal
from constraint import constraint

app = Flask(__name__)
app.secret_key= '123'

# Configure MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="sqluser",
    password="password",
    database="lokesh"
)

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
    "Suyash Prabhudessai", "Dinesh Karthik", "Rilee Rossouw", "jitesh Sharma", "Nicholas Pooran",
    "Shimron Hetmyer", "Rovman Powell", "Dhruv Jurel", "Devon Conway", "Ruturaj Gaikwad", "David Warner",
    "Prithvi Shaw", "Shubhman Gill", "Wriddhiman Saha", "Matthew Wade", "Rahmanullah Gurbaz", "Jason Roy",
    "KL Rahul", "Devdutt Padikkal", "Quinton de kock", "Kyle Mayers", "Rohit Sharma", "Ishan Kishan",
    "Shikhar Dhawan", "Jonny Bairstow", "Prabhsimran Singh", "Yashasvi Jaiswal", "Jos Buttler",
    "Anuj Rawat", "Faf du plessis", "Will Jacks", "Ajinkya Rahane", "Kane Williamson", "Harry Brook",
    "Shreyas Iyer", "Nitish Rana", "SuryaKumar Yadav", "Tilak Varma", "Sanju Samson", "Virat Kohli",
    "Rajat Patidhar", "Rahul Tripathi", "Aiden Markram", "Travis Head"
]


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    print(user)
    if user:
        # User exists, redirect to the home page
        if username == "admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    else:
        # User doesn't exist or incorrect password, redirect back to login page
        return redirect(url_for('login'))
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form
        print(data)
        cat = list(data.values())[0]  # Convert dict_values object to list and access the first element
        session['cat'] = cat
        print(cat)
        return redirect(url_for('preview'))
    return render_template('admin.html')
@app.route('/preview', methods=['GET', 'POST'])
def preview():
    cat = session.get('cat')
    print(cat)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM {}".format(cat))
    rows = cursor.fetchall()
    cursor.close()
    dataset=[]
    for row in rows:
        if row[1] == "TopOrder" or row[1] == "MiddleOrder":
            cursor = mydb.cursor()
            query = "SELECT player, overseas, credits, wicket_keeper FROM {} WHERE player = %s"
            cursor.execute(query.format(row[1]), (row[0],))
            result = cursor.fetchone()
            cursor.close()
            result_with_extra_info = result + (row[1],)
            dataset.append(result_with_extra_info)
        else:
            cursor = mydb.cursor()
            query = "SELECT player, overseas, credits FROM {} WHERE player = %s"
            cursor.execute(query.format(row[1]), (row[0],))
            result = cursor.fetchone()
            cursor.close()
            result_with_extra_info = result + (0,)+ (row[1],)
            dataset.append(result_with_extra_info)
    const = []
    const = constraint(dataset)
    return render_template('preview.html', dataset=dataset, const=const)
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        player = request.form['searchInput']
        cursor = mydb.cursor()
        cursor.execute("SELECT category FROM category WHERE player = %s", (player,))
        player_fetch = cursor.fetchone()
        if player_fetch:
            category = player_fetch[0]
            session['category']= category
            session['player'] = player
            # Pass player as a query parameter when redirecting
            return redirect(url_for('similar', player=player))

    # Render the home template for GET requests
    return render_template('home.html')

@app.route('/similar', methods=['GET', 'POST'])
def similar():
    if request.method == 'POST':
        data = request.form
        if 'roster' in data.values():
            return redirect(url_for('roster'))
        if 'search' in data.values():
            return redirect(url_for('home'))
        if 'logout' in data.values():
            return redirect(url_for('login'))
        stats= session.get('stats')
        category= session.get('category')
        player_name = stats[0]
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
                rupees_value = value
            else:
                indices.append(value)
        print(indices)
        print("Rupees: ", rupees_value)
        username = session.get('username')
        cursor = mydb.cursor()
        cursor.execute("SELECT sold_price FROM {}".format(username))
        sold_prices = [row[0] for row in cursor.fetchall()]
        total_sold_price = sum(sold_prices)
        print("Total sold price:", total_sold_price)
        if rupees_value is not None:
            rupees_value_num = Decimal(rupees_value)
            total_sold_price += rupees_value_num
        print(total_sold_price)
        if rupees_value is not None and total_sold_price<=100:
            try:
                cursor = mydb.cursor()

                # Check if the player already exists in the table
                query = "SELECT COUNT(*) FROM {} WHERE player = %s".format(username)
                cursor.execute(query, (player_name,))
                result = cursor.fetchone()
                # If player does not exist, insert the new record
                if result[0] == 0:
                    insert_query = "INSERT INTO {} (player, category, sold_price) VALUES (%s, %s, %s);".format(username)
                    cursor.execute(insert_query, (player_name, category, rupees_value))
                    mydb.commit()
                    print("Record inserted successfully.")
                else:
                    print("Player already exists in the table. Skipping insertion.")

            except mysql.connector.Error as err:
                print("Error:", err)
                mydb.rollback()  # Rollback changes in case of error

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
        print(indices)
        selected_data = [[t[index] for index in indices] for t in dataset]
        print(len(selected_data))
        if rupees_value is None:
            neighbors = main(query,dataset, selected_data, k=10, distance_metric='euclidean')
        else:
            neighbors= None
        return render_template('similar.html',category=category,data=stats, neighbors=neighbors)
    player_name = session.get('player')  # Retrieve player name from query parameter
    print(player_name)
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
    neighbors = None  # Default value if neighbors are not calculated
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT sold_price FROM {}".format(username))
    sold_prices = [row[0] for row in cursor.fetchall()]
    total_sold_price = sum(sold_prices)
    print("Total sold price:", total_sold_price)
    session['total_sold_price']= total_sold_price
    return render_template('similar.html',category= category,data=stats, neighbors=neighbors)
@app.route('/roster', methods=['GET', 'POST'])
def roster():
    if request.method == 'POST':
        data = request.form
        if 'home' in data.values():
            return redirect(url_for('home'))
        if 'similar' in data.values():
            return redirect(url_for('similar'))
        username = session.get('username')
        playerName = request.form.get('player')
        cursor = mydb.cursor()
        query = "DELETE FROM {} WHERE player = %s".format(username)
        cursor.execute(query, (playerName,))
        mydb.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
    username = session.get('username')
    cursor= mydb.cursor()
    cursor.execute("SELECT category, COUNT(*) AS category_count FROM {} GROUP BY category;".format(username))
    table= cursor.fetchall()
    Catcount = [0, 0, 0, 0, 0]
    left=[2, 2, 1, 2, 2, 0]
    for i in range(len(table)):
        if table[i][0]== "MiddleOrder":
            Catcount[1]= table[i][1]
            left[1] = 2 - Catcount[1]
            if left[1] < 0:
                left[5]+= abs(left[1])
                left[1] = 0
        elif table[i][0] == "TopOrder":
            Catcount[0]= table[i][1]
            left[0] = 2 - Catcount[0]
            if left[0] < 0:
                left[5]+= abs(left[0])
                left[0] = 0
        elif table[i][0] == "AllRounder":
            Catcount[2]= table[i][1]
            left[2] = 1 - Catcount[2]
            if left[2] < 0:
                left[5]+= abs(left[2])
                left[2] = 0
        elif table[i][0] == "Spinner":
            Catcount[3]= table[i][1]
            left[3] = 2 - Catcount[3]
            if left[3] < 0:
                left[5]+= abs(left[3])
                left[3] = 0
        else:
            Catcount[4]= table[i][1]
            left[4] = 2 - Catcount[4]
            if left[4] < 0:
                left[5]+= abs(left[4])
                left[4] = 0
    cursor= mydb.cursor()
    cursor.execute("Select * from {}".format(username))
    Bid = cursor.fetchall()
    length = len(Bid)
    progress = calci(Catcount, left)
    cursor = mydb.cursor()
    cursor.execute("SELECT sold_price FROM {}".format(username))
    sold_prices = [row[0] for row in cursor.fetchall()]
    total_sold_price = sum(sold_prices)
    print("Total sold price:", total_sold_price)
    return render_template('roster.html', Catcount= Catcount, left=left, length= length, Bid=Bid, progress=progress, total_sold_price=total_sold_price)


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
