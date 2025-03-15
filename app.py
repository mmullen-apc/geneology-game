from flask import Flask, render_template, jsonify, request
import os
import re
from dotenv import load_dotenv
import random

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Create a list of the genealogy in order with indexed duplicates
genealogy_list = [
    "Jesus",
    "Joseph1",
    "Heli",
    "Matthat1",
    "Levi1",
    "Melki1",
    "Jannai",
    "Joseph2",
    "Mattathias1",
    "Amos",
    "Nahum",
    "Esli",
    "Naggai",
    "Maath",
    "Mattathias2",
    "Semein",
    "Josek",
    "Joda",
    "Joanan",
    "Rhesa",
    "Zerubbabel",
    "Shealtiel",
    "Neri",
    "Melki2",
    "Addi",
    "Cosam",
    "Elmadam",
    "Er",
    "Joshua",
    "Eliezer",
    "Jorim",
    "Matthat2",
    "Levi2",
    "Simeon",
    "Judah1",
    "Joseph3",
    "Jonam",
    "Eliakim",
    "Melea",
    "Menna",
    "Mattatha",
    "Nathan",
    "David",
    "Jesse",
    "Obed",
    "Boaz",
    "Salmon",
    "Nahshon",
    "Amminadab",
    "Ram",
    "Hezron",
    "Perez",
    "Judah2",
    "Jacob",
    "Isaac",
    "Abraham",
    "Terah",
    "Nahor",
    "Serug",
    "Reu",
    "Peleg",
    "Eber",
    "Shelah",
    "Cainan",
    "Arphaxad",
    "Shem",
    "Noah",
    "Lamech",
    "Methuselah",
    "Enoch",
    "Jared",
    "Mahalalel",
    "Kenan",
    "Enosh",
    "Seth",
    "Adam",
    "God"
]

# Create dictionary from the list
genealogy = {genealogy_list[i]: genealogy_list[i + 1] for i in range(len(genealogy_list) - 1)}

# Debug print to verify sequence
print("\nVerifying sequence:")
current = "Jesus"
seen = set()
while current != "God":
    if current in seen:
        print(f"ERROR: Found duplicate in sequence: {current}")
        break
    seen.add(current)
    next_name = genealogy[current]
    print(f"{current} -> {next_name}")
    current = next_name

# Verify specific section
print("\nVerifying Neri section:")
print(f"Neri -> {genealogy['Neri']}")
print(f"Melki2 -> {genealogy['Melki2']}")

def strip_parentheses(text):
    """Remove parenthetical information from text."""
    return re.sub(r'\s*\([^)]*\)', '', text)

def get_progressive_hint(name, revealed_count):
    """Get a hint that reveals more letters of the name."""
    # Strip any numbers from the end for the hint
    base_name = re.sub(r'\d+$', '', name)
    
    if revealed_count == 0:
        # First hint is random (first or last letter)
        if random.choice([True, False]):
            return {"count": 1, "hint": f"Next name starts with: {base_name[0]}"}
        else:
            return {"count": 1, "hint": f"Next name ends with: {base_name[-1]}"}
    elif revealed_count == 1:
        # Second hint shows both first and last letters
        return {"count": 2, "hint": f"Next name starts with: {base_name[0]} and ends with: {base_name[-1]}"}
    elif revealed_count == 2:
        # Third hint shows length of the base name (without numbers)
        num_letters = len(base_name)
        return {"count": 3, "hint": f"The name has {num_letters} letter{'s' if num_letters != 1 else ''}"}
    else:
        # After that, progressively reveal more letters
        revealed = ['_'] * len(base_name)
        revealed[0] = base_name[0]  # First letter always shown
        revealed[-1] = base_name[-1]  # Last letter always shown
        
        # Calculate how many additional letters to reveal
        to_reveal = min(revealed_count - 2, len(base_name) - 2)  # -2 because first and last are already shown
        
        # Get indices of letters not yet revealed (excluding first and last)
        available_indices = list(range(1, len(base_name) - 1))
        random.shuffle(available_indices)
        
        # Reveal additional letters
        for idx in available_indices[:to_reveal]:
            revealed[idx] = base_name[idx]
        
        hint = "Next name: " + " ".join(revealed)
        return {
            "count": revealed_count + 1,
            "hint": hint,
            "complete": revealed_count >= len(base_name)
        }

def get_random_start_name():
    """Get a random name from the genealogy list, excluding duplicates."""
    # Create a list of unique base names (without numbers)
    seen_names = set()
    unique_names = []
    for name in genealogy_list:
        base_name = re.sub(r'\d+$', '', name)
        if base_name not in seen_names:
            seen_names.add(base_name)
            unique_names.append(name)
    # Don't include 'God' as it's the end of the sequence
    unique_names.remove('God')
    return random.choice(unique_names)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/random-start', methods=['GET'])
def random_start():
    """Get a random starting name for the challenge mode."""
    return jsonify({
        "start_name": get_random_start_name()
    })

@app.route('/api/next', methods=['POST'])
def next_name():
    data = request.json
    current_name = data.get('current_name', 'Jesus')
    revealed_count = int(data.get('revealed_count', 0))
    
    if current_name == "God":
        return jsonify({
            "complete": True,
            "next_name": "God",
            "hint": "You've completed the sequence!",
            "revealed_count": 0
        })
    
    next_name = genealogy.get(current_name)
    if not next_name:
        return jsonify({"error": "Invalid name"})
    
    hint_data = get_progressive_hint(next_name, revealed_count)
    return jsonify({
        "next_name": next_name,
        "hint": hint_data["hint"],
        "revealed_count": hint_data["count"],
        "complete": next_name == "God"  # Set complete flag when reaching God
    })

@app.route('/api/total-names')
def get_total_names():
    return jsonify({'total': len(genealogy_list)})

if __name__ == '__main__':
    app.run(debug=True) 