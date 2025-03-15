import random
import time
import msvcrt
import os
import re
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Azure Speech Service
try:
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    
    if not speech_key or not speech_region:
        raise ValueError("Speech credentials not found in .env file")
    
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async("Test").get()
    if result.reason == speechsdk.ResultReason.Canceled:
        raise Exception(f"Speech synthesis failed: {result.error_details}")
    
except Exception as e:
    print(f"Error initializing speech service: {str(e)}")
    print("Continuing without speech...")
    speech_config = None

# Create a list of the genealogy in order
genealogy_list = [
    "Jesus",
    "Joseph (of Heli)",
    "Heli",
    "Matthat",
    "Levi (son of Matthat)",
    "Melki (son of Levi)",
    "Jannai",
    "Joseph (of Mattathias)",
    "Mattathias (father of Joseph)",
    "Amos",
    "Nahum",
    "Esli",
    "Naggai",
    "Maath",
    "Mattathias (son of Maath)",
    "Semein",
    "Josek",
    "Joda",
    "Joanan",
    "Rhesa",
    "Zerubbabel",
    "Shealtiel",
    "Neri",
    "Melki (son of Neri)",
    "Addi",
    "Cosam",
    "Elmadam",
    "Er",
    "Joshua",
    "Eliezer",
    "Jorim",
    "Matthat (father of Jorim)",
    "Levi (son of Simeon)",
    "Simeon",
    "Judah (son of Joseph)",
    "Joseph (father of Judah)",
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
    "Judah (son of Jacob)",
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

def strip_parentheses(text):
    """Remove parenthetical information from text."""
    return re.sub(r'\s*\([^)]*\)', '', text)

def speak(text):
    """Speak the given text using Azure's Text-to-Speech service."""
    if speech_config is None:
        print(text)
        return
        
    try:
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.Canceled:
            print(text)
    except Exception as e:
        print(text)

def wait_for_keypress():
    """Wait for a keypress and return True if 'r' was pressed."""
    key = msvcrt.getch()
    return key.lower() == b'r'

def wait_for_input():
    """Wait indefinitely for input, return 'r' for restart, 'h' for hint, 'c' for continue."""
    while True:
        key = msvcrt.getch().lower()
        if key == b'r':
            return 'r'
        elif key == b'h':
            return 'h'
        else:
            return 'c'

def check_for_h():
    """Check if 'h' was pressed without blocking."""
    if msvcrt.kbhit():
        key = msvcrt.getch()
        return key.lower() == b'h'
    return False

def get_hint_state(name, current_hint_state):
    """Get hint based on current state and H key press."""
    clean_name = strip_parentheses(name)
    
    if check_for_h():
        if current_hint_state == "first":
            return "both", f"Next name starts with: {clean_name[0]} and ends with: {clean_name[-1]}"
        elif current_hint_state == "last":
            return "both", f"Next name starts with: {clean_name[0]} and ends with: {clean_name[-1]}"
        elif current_hint_state == "both":
            return "length", f"Next name has {len(clean_name)} letters"
        else:  # length or none
            return current_hint_state, None
    
    return current_hint_state, None

def get_initial_hint(name):
    """Get initial random hint (first or last letter)."""
    clean_name = strip_parentheses(name)
    if random.choice([True, False]):
        return "first", f"Next name starts with: {clean_name[0]}"
    else:
        return "last", f"Next name ends with: {clean_name[-1]}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_mode():
    """Let user select whether to show hints or not."""
    clear_screen()
    print("Select mode:")
    print("1. Show first letter hints")
    print("2. No hints")
    while True:
        try:
            key = msvcrt.getch()
            if key == b'1':
                return True
            elif key == b'2':
                return False
        except:
            pass

def get_random_hint(name):
    """Randomly return either first or last letter hint."""
    clean_name = strip_parentheses(name)
    if random.choice([True, False]):
        return f"Next name starts with: {clean_name[0]}"
    else:
        return f"Next name ends with: {clean_name[-1]}"

def get_progressive_hint(name, revealed_count):
    """Get a hint that reveals more letters of the name."""
    clean_name = strip_parentheses(name)
    if revealed_count == 0:
        # First hint is random (first or last letter)
        if random.choice([True, False]):
            return 1, f"Next name starts with: {clean_name[0]}"
        else:
            return 1, f"Next name ends with: {clean_name[-1]}"
    elif revealed_count == 1:
        # Second hint shows both first and last letters
        return 2, f"Next name starts with: {clean_name[0]} and ends with: {clean_name[-1]}"
    elif revealed_count == 2:
        # Third hint shows length
        return 3, f"Next name has {len(clean_name)} letters"
    else:
        # After that, progressively reveal more letters
        revealed = ['_'] * len(clean_name)
        revealed[0] = clean_name[0]  # First letter always shown
        revealed[-1] = clean_name[-1]  # Last letter always shown
        
        # Calculate how many additional letters to reveal
        to_reveal = min(revealed_count - 2, len(clean_name) - 2)  # -2 because first and last are already shown
        
        # Get indices of letters not yet revealed (excluding first and last)
        available_indices = list(range(1, len(clean_name) - 1))
        random.shuffle(available_indices)
        
        # Reveal additional letters
        for idx in available_indices[:to_reveal]:
            revealed[idx] = clean_name[idx]
        
        hint = "Next name: " + " ".join(revealed)
        return revealed_count + 1, hint

def genealogy_sequence():
    # Speak introduction
    clear_screen()
    speak("The Genealogy Game by Dayton Mullen")
    time.sleep(2)  # Give time for the introduction to be heard
    
    while True:
        show_hints = select_mode()
        current_person = "Jesus"
        sequence = [current_person]
        
        while True:
            clear_screen()
            # Print all sequences up to current
            for i in range(len(sequence)):
                # Strip parentheses from each name for display
                clean_sequence = [strip_parentheses(name) for name in sequence[:i+1]]
                print(" → ".join(clean_sequence))
            print("-" * 40)
            
            # Speak current sequence without parenthetical information
            clean_sequence = [strip_parentheses(name) for name in sequence]
            speak(" ".join(clean_sequence))
            
            # Get next father and handle hints
            current_father = genealogy[current_person]
            if show_hints:
                revealed_count = 0
                while True:
                    if revealed_count == 0:
                        revealed_count, hint = get_progressive_hint(current_father, revealed_count)
                        print(f"\n{hint}")
                    
                    print("\nPress H for more hints, any other key to continue")
                    key = wait_for_input()
                    
                    if key == 'h':
                        revealed_count, hint = get_progressive_hint(current_father, revealed_count)
                        print(f"\n{hint}")
                        # If all letters are revealed, wait for one more keypress before continuing
                        if revealed_count >= len(strip_parentheses(current_father)):
                            print("\nPress any key to continue")
                            wait_for_input()
                            break
                    else:
                        break
            
            sequence.append(current_father)
            current_person = current_father
            
            if current_person == "God":
                # Print final sequence
                clear_screen()
                for i in range(len(sequence)):
                    clean_sequence = [strip_parentheses(name) for name in sequence[:i+1]]
                    print(" → ".join(clean_sequence))
                print("\nPress 'r' to restart or any other key to quit")
                if wait_for_keypress():
                    break  # Break inner loop to restart
                else:
                    return  # Exit function to quit
            
            print("\nPress 'r' to restart or any other key to continue")
            if wait_for_keypress():
                break  # Break inner loop to restart
        
        continue  # Continue outer loop to restart

if __name__ == "__main__":
    genealogy_sequence()

