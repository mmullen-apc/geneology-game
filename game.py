import random
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
# Set a slightly slower rate for better clarity
engine.setProperty('rate', 150)

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

# Full Genealogy dictionary (child: father)
genealogy = {
    "Jesus": "Joseph", "Joseph": "Heli", "Heli": "Matthat", "Matthat": "Levi", "Levi": "Melki", "Melki": "Jannai", "Jannai": "Joseph", "Joseph": "Mattathias", "Mattathias": "Amos", "Amos": "Nahum", "Nahum": "Esli", "Esli": "Naggai", "Naggai": "Maath", "Maath": "Mattathias", "Mattathias": "Semein", "Semein": "Josek", "Josek": "Joda", "Joda": "Joanan", "Joanan": "Rhesa", "Rhesa": "Zerubbabel", "Zerubbabel": "Shealtiel", "Shealtiel": "Neri", "Neri": "Melki", "Melki": "Addi", "Addi": "Cosam", "Cosam": "Elmadam", "Elmadam": "Er", "Er": "Joshua", "Joshua": "Eliezer", "Eliezer": "Jorim", "Jorim": "Matthat", "Matthat": "Levi", "Levi": "Simeon", "Simeon": "Judah", "Judah": "Joseph", "Joseph": "Jonam", "Jonam": "Eliakim", "Eliakim": "Melea", "Melea": "Menna", "Menna": "Mattatha", "Mattatha": "Nathan", "Nathan": "David", "David": "Jesse", "Jesse": "Obed", "Obed": "Boaz", "Boaz": "Salmon", "Salmon": "Nahshon", "Nahshon": "Amminadab", "Amminadab": "Ram", "Ram": "Hezron", "Hezron": "Perez", "Perez": "Judah", "Judah": "Jacob", "Jacob": "Isaac", "Isaac": "Abraham", "Abraham": "Terah", "Terah": "Nahor", "Nahor": "Serug", "Serug": "Reu", "Reu": "Peleg", "Peleg": "Eber", "Eber": "Shelah", "Shelah": "Cainan", "Cainan": "Arphaxad", "Arphaxad": "Shem", "Shem": "Noah", "Noah": "Lamech", "Lamech": "Methuselah", "Methuselah": "Enoch", "Enoch": "Jared", "Jared": "Mahalalel", "Mahalalel": "Kenan", "Kenan": "Enosh", "Enosh": "Seth", "Seth": "Adam", "Adam": "God"
}

# Rhymes to help remember the relationships
genealogy_rhymes = {
    "Jesus": "Joseph's son was Jesus, who turned water into Reese's",
    "Joseph": "Heli's son was Joseph, who liked his coat and wouldn't lose it",
    "Heli": "Matthat's son was Heli, who ate peanut butter and jelly",
    "Matthat": "Levi's son was Matthat, who lost his sandals just like that",
    "Levi": "Melki's son was Levi, who drove a chariot like a Chevy",
    "Melki": "Jannai's son was Melki, who danced until his legs got shaky",
    "Jannai": "Joseph's son was Jannai, who rode camels like a Ferrari",
    "Mattathias": "Amos' son Mattathias, who had a beard that was contagious",
    "Amos": "Nahum's son was Amos, who played hide and seek and never found us",
    "Nahum": "Esli's son was Nahum, who built a tent but couldn't stay in 'em",
    "Esli": "Naggai's son was Esli, whose jokes were rather smelly",
    "Naggai": "Maath's son was Naggai, whose dance moves were quite swaggy",
    "Maath": "Mattathias' son was Maath, who took the world's longest bath",
    "Semein": "Josek's son Semein, who thought his goat was a marine",
    "Josek": "Joda's son was Josek, whose beard grew so long he'd trip on it",
    "Joda": "Joanan's son was Joda, who surfed on scrolls all over",
    "Joanan": "Rhesa's son Joanan, who thought his donkey was a penguin",
    "Rhesa": "Zerubbabel's son was Rhesa, who snored louder than a freezer",
    "Zerubbabel": "Shealtiel's son Zerubbabel, whose name was quite unpronounceable",
    "Shealtiel": "Neri's son was Shealtiel, who rang like a dinner bell",
    "Neri": "Melki's son was Neri, who rode a camel named Larry",
    "Addi": "Cosam's son was Addi, whose sandals were quite trendy",
    "Cosam": "Elmadam's son was Cosam, who kept his sheep in his awesome possum",
    "Elmadam": "Er's son was Elmadam, who juggled figs like BAM BAM BAM",
    "Er": "Joshua's son was Er, whose beard had quite a flair",
    "Joshua": "Eliezer's son was Joshua, whose walls went boom, see ya!",
    "Eliezer": "Jorim's son Eliezer, who kept his camels in a freezer",
    "Jorim": "Matthat's son was Jorim, who thought his tent was a forum",
    "Simeon": "Judah's son was Simeon, whose jokes kept everyone beamin'",
    "Judah": "Joseph's son was Judah, whose dance moves couldn't be smoother",
    "Jonam": "Eliakim's son was Jonam, who thought his sheep could program",
    "Eliakim": "Melea's son Eliakim, who taught his goats to swim",
    "Melea": "Menna's son was Melea, who painted all his sheep bright green, yeah",
    "Menna": "Mattatha's son was Menna, whose beard grew ever longer",
    "Mattatha": "Nathan's son Mattatha, who chased his chickens up the ladder",
    "Nathan": "David's son was Nathan, who loved to count his sheep while nappin'",
    "David": "Jesse's son was David, who played such tunes that lions behaved it",
    "Jesse": "Obed's son was Jesse, whose hair was wild and messy",
    "Obed": "Boaz's son was Obed, whose sandals always floated",
    "Boaz": "Salmon's son was Boaz, who tripped on robes that Ruth had sewed us",
    "Salmon": "Nahshon's son was Salmon, who swam upstream a-splashin'",
    "Nahshon": "Amminadab's boy Nahshon, who wore his robe back-to-front on",
    "Amminadab": "Ram's son was Amminadab, whose dance moves made the camels mad",
    "Ram": "Hezron's son was Ram, who thought his beard was made of ham",
    "Hezron": "Perez's son was Hezron, whose camel racing kept progressin'",
    "Perez": "Judah's son was Perez, who counted sheep to fight his stress",
    "Jacob": "Isaac's son was Jacob, who wrestled angels in a cake-up",
    "Isaac": "Abraham's son was Isaac, who laughed so hard he had to take a break quick",
    "Abraham": "Terah's son was Abraham, who counted stars and lost his gram",
    "Terah": "Nahor's son was Terah, whose beard was used as a mirror, yeah",
    "Nahor": "Serug's son was Nahor, who danced until he hit the floor",
    "Serug": "Reu's son was Serug, who thought his camel was a pug",
    "Reu": "Peleg's son was Reu, who painted all his sheep bright blue",
    "Peleg": "Eber's son was Peleg, who liked his eggs with extra keg",
    "Eber": "Shelah's son was Eber, who rode his donkey like a zebra",
    "Shelah": "Cainan's son was Shelah, who never met a joke he didn't tell ya",
    "Cainan": "Arphaxad's son was Cainan, whose beard was always tangled in his lion",
    "Arphaxad": "Shem's son was Arphaxad, whose tongue twisters drove everyone mad",
    "Shem": "Noah's son was Shem, who seasick got on Noah's hem",
    "Noah": "Lamech's son was Noah, who built a boat that was a showah",
    "Lamech": "Methuselah's son was Lamech, whose age math gave everyone a headache",
    "Methuselah": "Enoch's son Methuselah, whose birthday cakes were sky-high, yeah",
    "Enoch": "Jared's son was Enoch, who skipped the stairs straight to the top quick",
    "Jared": "Mahalalel's son was Jared, whose jokes were so bad everyone got scared",
    "Mahalalel": "Kenan's son Mahalalel, whose name was quite a tongue-twister, well",
    "Kenan": "Enosh's son was Kenan, whose beard was always weavin'",
    "Enosh": "Seth's son was Enosh, whose sandals had a golden swoosh",
    "Seth": "Adam's son was Seth, who named the animals till out of breath",
    "Adam": "God created Adam, who named the animals random"
}

genealogy_groups = {
    "A": list(genealogy.keys())[:20],
    "B": list(genealogy.keys())[20:40],
    "C": list(genealogy.keys())[40:]
}

def flashcard_game():
    print("Welcome to the Genealogy Flashcard Game!")
    speak("Welcome to the Genealogy Flashcard Game!")
    print("Choose a group to study: A, B, or C.")
    speak("Choose a group to study: A, B, or C.")
    group = input("Enter your choice: ").strip().upper()
    
    if group not in genealogy_groups:
        print("Invalid group selection. Defaulting to group A.")
        speak("Invalid group selection. Defaulting to group A.")
        group = "A"
    
    print(f"\nNames in group {group}:")
    speak(f"Names in group {group}")
    for name in genealogy_groups[group]:
        print(f"- {name}")
        speak(name)
    print("\nLet's begin the quiz!\n")
    speak("Let's begin the quiz!")
    
    score = 0
    question_count = 0
    max_questions = 20
    questions = genealogy_groups[group]
    
    # Initialize weights for both children and fathers in this group
    weights = {}
    for child in questions:
        weights[child] = 1  # weight for when child appears in question
        father = genealogy[child]
        if father not in weights:
            weights[father] = 1  # weight for when father appears in question
    
    while question_count < max_questions:
        # Keep selecting a new person until we find one that won't result in "Joseph" in the question
        # or a duplicate name that would be ambiguous
        while True:
            # Select child based on weights
            child = random.choices(questions, weights=[weights[q] for q in questions])[0]
            father = genealogy[child]
            question_type = random.choice(["son_of", "son_of_reverse"])
            
            # Skip if this would result in "Joseph" in the question
            if question_type == "son_of" and father == "Joseph":
                continue
            if question_type == "son_of_reverse" and child == "Joseph":
                continue
                
            # Skip if the name appears multiple times in the genealogy
            if question_type == "son_of_reverse":
                name_count = list(genealogy.keys()).count(child)
                if name_count > 1:
                    continue
            
            break
            
        if question_type == "son_of":
            # Ask "Who was the son of [father]?"
            question = f"Who was the son of {father}?"
            print(f"Question {question_count}/{max_questions}: {question}")
            speak(question)
            options = [child]  # child is the correct answer
            possible_wrong_answers = [name for name in genealogy.keys() if name != child and name != father]
            person_being_tested = father
        else:
            # Ask "Of whom was [child] the son?"
            question = f"Of whom was {child} the son?"
            print(f"Question {question_count}/{max_questions}: {question}")
            speak(question)
            options = [father]  # father is the correct answer
            possible_wrong_answers = [name for name in genealogy.values() if name != father and name != child]
            person_being_tested = child
        
        # Add two random wrong answers from the filtered list
        for _ in range(2):
            wrong_choice = random.choice(possible_wrong_answers)
            options.append(wrong_choice)
            possible_wrong_answers.remove(wrong_choice)  # Remove to avoid duplicates
        
        random.shuffle(options)
        question_count += 1
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
            speak(f"Option {i}. {option}")
        
        answer = input("Your choice (1-3): ")
        
        if answer.isdigit() and 1 <= int(answer) <= 3:
            correct_answer_for_type = child if question_type == "son_of" else father
            if options[int(answer) - 1] == correct_answer_for_type:
                print("Correct! ✅\n")
                speak("Correct!")
                score += 1
                weights[person_being_tested] = max(0.5, weights[person_being_tested] - 0.5)
            else:
                print("Incorrect ❌. The correct answer is:")
                print("(╯︵╰,)")
                print(f"{correct_answer_for_type}")
                speak(f"Incorrect. The correct answer is {correct_answer_for_type}")
                
                person_for_rhyme = correct_answer_for_type if question_type == "son_of" else child
                rhyme = genealogy_rhymes[person_for_rhyme]
                print(f"\nHere's a rhyme to help you remember:")
                print(f"🎵 {rhyme} 🎵\n")
                speak(rhyme)
                
                weights[person_being_tested] = weights[person_being_tested] * 2 + 1
        else:
            print("Invalid choice. Please enter a number between 1 and 3.\n")
            speak("Invalid choice. Please enter a number between 1 and 3.")
    
    final_message = f"Game over! You answered {max_questions} questions and scored {score} points."
    print(final_message)
    speak(final_message)

if __name__ == "__main__":
    flashcard_game()
