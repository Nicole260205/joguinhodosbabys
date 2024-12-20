from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample Data
celebrities = [
    {"id": 1, "name": "Celebrity A", "gender": None},
    {"id": 2, "name": "Celebrity B", "gender": None}
]

leaderboard = {
    "Carina": 0,
    "Luiza": 0
}

guesses = []

@app.route('/')
def home():
    return render_template('index.html', celebrities=celebrities)

@app.route('/show_guesses')
def show_guesses():
    return render_template('guesses.html', guesses=guesses)

@app.route('/show_leaderboard')
def show_leaderboard():
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/judge_update')
def judge_update():
    return render_template('judge_update.html', leaderboard=leaderboard, celebrities=celebrities)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    player = request.form['player']
    celebrity_id = int(request.form['celebrity']) - 1
    gender = request.form['gender']

    guess = {
        "celebrity": celebrities[celebrity_id]['name'],
        "player": player,
        "guess": gender,
        "correct": None
    }
    guesses.append(guess)
    return redirect(url_for('show_guesses'))

@app.route('/add_celebrity', methods=['POST'])
def add_celebrity():
    name = request.form['name']
    new_id = len(celebrities) + 1
    celebrities.append({"id": new_id, "name": name, "gender": None})
    return redirect(url_for('judge_update'))

@app.route('/update_gender', methods=['POST'])
def update_gender():
    celebrity_id = int(request.form['celebrity']) - 1
    gender = request.form['gender']

    # Update celebrity gender
    celebrities[celebrity_id]['gender'] = gender

    # Update guesses correctness and leaderboard
    for guess in guesses:
        if guess['celebrity'] == celebrities[celebrity_id]['name']:
            guess['correct'] = (guess['guess'] == gender)
            if guess['correct']:
                leaderboard[guess['player']] += 1

    return redirect(url_for('show_guesses'))

@app.route('/update_scores', methods=['POST'])
def update_scores():
    player = request.form['player']
    points = int(request.form['points'])

    if player in leaderboard:
        leaderboard[player] += points

    return redirect(url_for('judge_update'))

if __name__ == '__main__':
    app.run(debug=True)
