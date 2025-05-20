from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Store games in memory (in a real app, use a database)
games = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    user_id = data.get('user_id')
    min_num = int(data.get('min', 1))
    max_num = int(data.get('max', 100))
    
    secret_number = random.randint(min_num, max_num)
    games[user_id] = {
        'secret_number': secret_number,
        'min': min_num,
        'max': max_num,
        'attempts': 0
    }
    
    return jsonify({
        'message': f'Game started! Guess a number between {min_num} and {max_num}',
        'min': min_num,
        'max': max_num
    })

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.json
    user_id = data.get('user_id')
    guess = int(data.get('guess'))
    
    if user_id not in games:
        return jsonify({'error': 'Game not found. Please start a new game.'}), 400
    
    game = games[user_id]
    game['attempts'] += 1
    
    if guess < game['min'] or guess > game['max']:
        return jsonify({
            'error': f'Your guess is out of range. Please guess between {game["min"]} and {game["max"]}'
        }), 400
    
    if guess < game['secret_number']:
        hints = [
            "Too low! My grandma could guess higher! Are you even trying?",
            "Nope, that's undercooked. Try a bigger number! Don't let the computer win!",
            "Think bigger! That number is hiding in the basement. Can you beat the odds?",
            "You need to aim higher, like your ambitions! Or are you scared to win?",
            "Come on, you can do better! The secret number is laughing at you.",
            "Is that your best shot? Go higher and show some guts!",
            "You call that a guess? My pet goldfish could do better. Try again!"
        ]
        import random
        return jsonify({
            'result': 'low',
            'attempts': game['attempts'],
            'hint': random.choice(hints)
        })
    elif guess > game['secret_number']:
        hints = [
            "Whoa, too high! This isn't the lottery jackpot. Are you just guessing wildly?",
            "Bring it down! That number is in the clouds. Can you get closer than this?",
            "Too much! Even my calculator is sweating. Don't let me win so easily!",
            "Try a smaller number, but not too small! Or are you afraid of success?",
            "Overshot! The secret number is rolling its eyes at you.",
            "You missed by a mile! Can you get it before I brag?",
            "That guess was ambitious! But can you actually win?"
        ]
        import random
        return jsonify({
            'result': 'high',
            'attempts': game['attempts'],
            'hint': random.choice(hints)
        })
    else:
        del games[user_id]  # Game over, remove from memory
        return jsonify({
            'result': 'correct',
            'attempts': game['attempts'],
            'secret_number': game['secret_number']
        })

if __name__ == '__main__':
    app.run(debug=True)