

from flask import Flask,render_template,url_for, flash, redirect,request,jsonify, session
from forms import login,Regestrition

import random
import time

import os 

app = Flask(__name__)


app.config["SECRET_KEY"] = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"


games_data = {
    'memory': {
        'name': 'Memory Game',
        'description': 'Find matching pairs of cards',
        'completed': False,
        'score': 0,
        'best_time': None,
        'icon': '🧠'
    },
    'puzzle': {
        'name': 'Puzzle Game',
        'description': 'Arrange pieces to complete the picture',
        'completed': False,
        'score': 0,
        'pieces_solved': 0,
        'icon': '🧩'
    },
    'colors': {
        'name': 'Colors Game',
        'description': 'Match colors with correct objects',
        'completed': False,
        'score': 0,
        'matches': 0,
        'icon': '🎨'
    }
}


memory_cards = [
    {'id': 1, 'emoji': '🐱', 'name': 'Cat'},
    {'id': 2, 'emoji': '🐶', 'name': 'Dog'},
    {'id': 3, 'emoji': '🐰', 'name': 'Rabbit'},
    {'id': 4, 'emoji': '🐻', 'name': 'Bear'},
    {'id': 5, 'emoji': '🐼', 'name': 'Panda'},
    {'id': 6, 'emoji': '🦁', 'name': 'Lion'}
]


puzzle_data = {
    'animal': {
        'name': 'Cute Animal',
        'pieces': [
            {'id': 1, 'shape': 'circle', 'position': 'head', 'emoji': '🐱'},
            {'id': 2, 'shape': 'triangle', 'position': 'body', 'emoji': '📦'},
            {'id': 3, 'shape': 'rectangle', 'position': 'legs', 'emoji': '🦵'},
            {'id': 4, 'shape': 'square', 'position': 'tail', 'emoji': '🌀'}
        ]
    }
}


colors_data = [
    {'color': '#FF6B6B', 'name': 'Red', 'emoji': '🍎'},
    {'color': '#4ECDC4', 'name': 'Blue', 'emoji': '🔵'},
    {'color': '#FFE66D', 'name': 'Yellow', 'emoji': '🌞'},
    {'color': '#6A4C93', 'name': 'Purple', 'emoji': '🍇'}
]


tasks = []
events = []


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def loginform():
    form = login()
    
    if form.validate_on_submit():
        if form.email.data == "test@example.com" and form.password.data == "password":
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('new.html', title='Log In', form=form)

@app.route("/get_started")
def get_started():
    return "<h1>Welcome! This is the next page.</h1>"

@app.route("/about")
def about():
    return render_template('about.html', Title="ABOUT")

@app.route("/sign", methods=['GET', 'POST'])
def sign():
    form = Regestrition()
    
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('loginform'))
        
    return render_template('sign.html', form=form)

@app.route("/forget")
def forget():
    return render_template('forget.html')

@app.route("/confirm")
def confirm():
    return render_template('confirm.html')

@app.route("/home2")
def home2():
    return render_template("home2.html")

@app.route("/test")
def test():
    return render_template("test.html")


@app.route('/todo')
def todo():
    return render_template('todo.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect(url_for('todo'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('todo'))


@app.route("/events")
def events_page():
    return render_template("events.html", events=events)

@app.route("/add_event", methods=["POST"])
def add_event():
    name = request.form.get("name")
    if name:
        events.append(name)
    return redirect(url_for("events_page"))

@app.route('/games')
def games_dashboard():
    return render_template('games_dashboard.html', games=games_data)


@app.route('/game/memory')
def memory_game():
    cards = memory_cards * 2
    random.shuffle(cards)
    return render_template('memory_game.html', cards=cards, game_data=games_data['memory'])

@app.route('/api/memory/complete', methods=['POST'])
def memory_complete():
    data = request.json
    time_taken = data.get('time', 0)
    moves = data.get('moves', 0)
    
    score = max(100 - (time_taken // 10) - (moves * 2), 10)
    
    games_data['memory']['score'] = score
    games_data['memory']['completed'] = True
    
    if games_data['memory']['best_time'] is None or time_taken < games_data['memory']['best_time']:
        games_data['memory']['best_time'] = time_taken
    
    return jsonify({'status': 'success', 'score': score})


@app.route('/game/puzzle')
def puzzle_game():
    return render_template('puzzle_game.html', puzzle=puzzle_data['animal'], game_data=games_data['puzzle'])

@app.route('/api/puzzle/complete', methods=['POST'])
def puzzle_complete():
    data = request.json
    pieces_solved = data.get('pieces_solved', 0)
    time_taken = data.get('time', 0)
    
    score = min(pieces_solved * 25 + max(50 - time_taken, 0), 100)
    
    games_data['puzzle']['score'] = score
    games_data['puzzle']['completed'] = True
    games_data['puzzle']['pieces_solved'] = pieces_solved
    
    return jsonify({'status': 'success', 'score': score})


@app.route('/game/colors')
def colors_game():
    return render_template('colors_game.html', colors=colors_data, game_data=games_data['colors'])

@app.route('/api/colors/complete', methods=['POST'])
def colors_complete():
    data = request.json
    matches = data.get('matches', 0)
    time_taken = data.get('time', 0)
    
    score = min(matches * 25 + max(50 - time_taken, 0), 100)
    
    games_data['colors']['score'] = score
    games_data['colors']['completed'] = True
    games_data['colors']['matches'] = matches
    
    return jsonify({'status': 'success', 'score': score})

@app.route('/progress')
def progress():
    completed_games = sum(1 for game in games_data.values() if game['completed'])
    total_score = sum(game['score'] for game in games_data.values())
    
    return render_template('progress.html', 
                         games=games_data,
                         completed_games=completed_games,
                         total_score=total_score)

@app.route('/sound')
def sound():
    cards = {
        'shapes': [
            {'name': 'Circle', 'color': '#FF6B6B'},
            {'name': 'Square', 'color': '#4ECDC4'},
            {'name': 'Triangle', 'color': '#FFE66D'}
        ],
        'colors': [
            {'name': 'Red', 'color': '#FF0000'},
            {'name': 'Blue', 'color': '#0000FF'},
            {'name': 'Green', 'color': '#00FF00'}
        ],
        'animals': [
            {'name': 'Cat', 'color': '#FFA07A'},
            {'name': 'Dog', 'color': '#CD853F'},
            {'name': 'Bird', 'color': '#87CEEB'}
        ]
    }
    return render_template('speech_therapy.html', cards=cards)


@app.route('/ai_assistant')
def ai_assistant():
    return render_template('ai_assistant.html')


DEEPSEEK_API_KEY = "sk-your-api-key-here"  
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    try:
        user_message = request.json.get('message', '')
        

        system_prompt = """You are a friendly, patient AI assistant for children with Down syndrome. 
        Use simple language, short sentences, and be encouraging. 
        You can help with:
        - Learning colors, shapes, numbers
        - Telling simple stories
        - Playing educational games
        - Answering questions in a child-friendly way
        Always be positive, use emojis occasionally, and keep responses brief and clear."""
        
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",  
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 150,
            "stream": False
        }
        

        response = request.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        ai_response = response.json()['choices'][0]['message']['content']
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        print(f"Error calling DeepSeek API: {str(e)}")
      
        fallback_responses = [
            "That's a great question! Let me think about that. 🤔",
            "I'd love to help you with that! 😊",
            "What a fun thing to ask about! 🎉",
            "Let's explore that together! 🌟",
            "I'm here to help you learn and have fun! 🎈",
            "That's interesting! Tell me more about what you'd like to know! 💫"
        ]
        import random
        return jsonify({
            'success': False,
            'response': random.choice(fallback_responses)
        })


@app.route('/api/chat/free', methods=['POST'])
def chat_with_free_ai():

    try:
        user_message = request.json.get('message', '')
        
        system_prompt = """You are a friendly, patient AI assistant for children with Down syndrome. 
        Use simple language, short sentences, and be encouraging."""
    
        responses = {
            'hello': "Hello! I'm your learning friend! How are you today? 😊",
            'hi': "Hi there! I'm so excited to help you learn! What would you like to know? 🌟",
            'story': "Once upon a time, there was a little robot who loved helping children learn. Every day was a new adventure! Would you like to hear more? 📚",
            'color': "Colors are amazing! Red like a fire truck 🚒, blue like the ocean 🌊, green like a frog 🐸, and yellow like the sun ☀️!",
            'count': "Let's count together! 1, 2, 3, 4, 5... You're doing great! How high can we count? 🔢",
            'animal': "Animals are wonderful! Dogs say 'woof' 🐶, cats say 'meow' 🐱, cows say 'moo' 🐮, and birds sing beautiful songs 🎵!",
            'weather': "I think it's a perfect day for learning new things! The sun is shining in our hearts! ☀️",
            'game': "Let's play a fun learning game! We can match colors, find shapes, or learn new words! 🎮",
            'help': "I can help you with stories, games, colors, numbers, songs, and answering your questions! Just ask me anything! 💫"
        }
        
        lower_message = user_message.lower()
        response = "That sounds interesting! I'd love to help you learn more about that! What's your favorite thing to learn? 🌈"
        
        for key, resp in responses.items():
            if key in lower_message:
                response = resp
                break
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"Error in free AI: {str(e)}")
        return jsonify({
            'success': False,
            'response': "I'm here to help you learn and have fun! What would you like to know today? 😊"
        })

#33333333333333333333333

#333333333333333333333
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)