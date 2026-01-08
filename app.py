from flask import Flask, render_template_string, jsonify
import random
import string

app = Flask(__name__)

# Store used letters in memory (shared across all users - for single-user demo)
# For multi-user scenarios, use Flask sessions or database
used_letters = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Losowanie Litery - Państwa Miasta</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 2em;
        }
        
        .current-letter {
            font-size: 6em;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
            min-height: 120px;
            display: flex;
            justify-content: center;
            align-items: center;
            text-transform: uppercase;
        }
        
        .draw-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 20px 50px;
            font-size: 1.5em;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .draw-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .draw-button:active {
            transform: translateY(0);
        }
        
        .used-letters-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #eee;
        }
        
        .used-letters-title {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 15px;
        }
        
        .used-letters {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            min-height: 50px;
        }
        
        .letter-badge {
            background: #f0f0f0;
            color: #333;
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .no-letters {
            color: #999;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎲 Państwa - Miasta</h1>
        <div class="current-letter" id="currentLetter">?</div>
        <button class="draw-button" id="drawButton" onclick="drawLetter()">Wylosuj literę</button>
        
        <div class="used-letters-section">
            <div class="used-letters-title">Wykorzystane litery:</div>
            <div class="used-letters" id="usedLetters">
                <span class="no-letters">Brak wykorzystanych liter</span>
            </div>
        </div>
    </div>
    
    <script>
        function drawLetter() {
            fetch('/draw', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.letter) {
                    // Display the new letter with animation
                    const letterElement = document.getElementById('currentLetter');
                    letterElement.style.opacity = '0';
                    setTimeout(() => {
                        letterElement.textContent = data.letter;
                        letterElement.style.opacity = '1';
                    }, 200);
                    
                    // Update used letters
                    updateUsedLetters(data.used_letters);
                } else if (data.message) {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Wystąpił błąd podczas losowania litery');
            });
        }
        
        function updateUsedLetters(letters) {
            const container = document.getElementById('usedLetters');
            if (letters && letters.length > 0) {
                container.innerHTML = letters.map(letter => 
                    `<span class="letter-badge">${letter}</span>`
                ).join('');
            } else {
                container.innerHTML = '<span class="no-letters">Brak wykorzystanych liter</span>';
            }
        }
        
        // Load initial state
        window.addEventListener('DOMContentLoaded', () => {
            fetch('/get_used')
            .then(response => response.json())
            .then(data => {
                updateUsedLetters(data.used_letters);
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/draw', methods=['POST'])
def draw_letter():
    """Draw a random letter from the English alphabet"""
    # English alphabet
    alphabet = list(string.ascii_uppercase)
    
    # Remove already used letters
    available_letters = [letter for letter in alphabet if letter not in used_letters]
    
    if not available_letters:
        return jsonify({
            'message': 'Wszystkie litery zostały już wykorzystane!',
            'used_letters': used_letters
        })
    
    # Draw a random letter
    letter = random.choice(available_letters)
    used_letters.append(letter)
    
    return jsonify({
        'letter': letter,
        'used_letters': used_letters
    })

@app.route('/get_used', methods=['GET'])
def get_used():
    """Get list of used letters"""
    return jsonify({
        'used_letters': used_letters
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the game"""
    global used_letters
    used_letters = []
    return jsonify({
        'message': 'Gra została zresetowana',
        'used_letters': used_letters
    })

if __name__ == '__main__':
    # Development server - for production, use a WSGI server like gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
