import os
from datetime import datetime
import random
import json
from pathlib import Path


"""""""""""""""""""""""""""
   CLASSES IMPLEMENTATION 
"""""""""""""""""""""""""""

class Profile:
    def __init__(self, name, level, xp, accuracy, best_time, avg_time, tries):
        self.name = name
        self.level = level
        self.xp = xp
        self.accuracy = accuracy
        self.best_time = best_time
        self.avg_time = avg_time
        self.tries = tries

    def __str__(self):
        return f"""
    --= =< P R O F I L E >= =--
    Name :        {self.name}
    _________________________
    Tries:        {self.tries}
    Accuracy:     {self.accuracy*100} %
    Best time:    {self.best_time:.2f}s
    Average time: {self.avg_time:.2f}s
    _________________________
    Level:        {self.level}
    XP:           {self.xp:.1f}
              """
        
    def add_xp(self, amount):
        self.xp += amount
        leveled = 0
        while True:
            xp_level_threshold = 100 * (1.1 * self.level)
            if self.xp >= xp_level_threshold:
                self.xp -= xp_level_threshold
                self.level += 1
                leveled += 1
            else:
                break
        if leveled:
            print(f"Level up ! You've reached level {self.level} !")
    
    # Adding 1 tries everytime player play a run.
    def add_tries(self):
        self.tries += 1

    # Computing accuracy/average_time/best_time again everytime player have a new accuracy from run.
    def compute_accuracy(self, new_accuracy):
        self.accuracy = (self.accuracy + new_accuracy) / self.tries

    def compute_avgtime(self, new_playedtime):
        self.avg_time = (self.avg_time + new_playedtime) / self.tries

    def compare_besttime(self, new_playedtime):
        if (new_playedtime > self.best_time):
            self.best_time = new_playedtime



"""""""""""""""""""""""""""
    DATA IMPLEMENTATION 
"""""""""""""""""""""""""""
# Profile:: (default) if player don't input their name
profile = Profile("", 0, 0, 0, 0, 0, 0)

# Data file::
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)   # If the base folder doesn't exist "data" folder. Make a new one.

data_file = DATA_DIR / "save.json"
history_file = DATA_DIR / "history.txt"

# Hiragana & Katakana alphabet and its Romaji::
hiragana = {'あ':{'a'}, 'い':{'i'} ,'う':{'u'}, 'え':{'e'} ,'お':{'o'},
            'か':{'ka'}, 'き':{'ki'}, 'く':{'ku'}, 'け':{'ke'}, 'こ':{'ko'},
            'さ':{'sa'}, 'し':{'shi', 'si'}, 'す':{'su'}, 'せ':{'se'}, 'そ':{'so'},
            'た':{'ta'}, 'ち':{'chi'}, 'つ':{'tsu'}, 'て':{'te'}, 'と':{'to'},
            'な':{'na'}, 'に':{'ni'}, 'ぬ':{'nu'}, 'ね':{'ne'}, 'の':{'no'},
            'は':{'ha'}, 'ひ':{'hi'}, 'ふ':{'fu'}, 'へ':{'he'}, 'ほ':{'ho'},
            'ま':{'ma'}, 'み':{'mi'}, 'む':{'mu'}, 'め':{'me'}, 'も':{'mo'},
            'ら':{'ra'}, 'り':{'ri'}, 'る':{'ru'}, 'れ':{'re'}, 'ろ':{'ro'},
            'や':{'ya'}, 'ゆ':{'yu'}, 'よ':{'yo'}, 'わ':{'wa'}, 'を':{'wo', 'o'}, 'ん':{'n'},
            'が':{'ga'}, 'ぎ':{'gi'}, 'ぐ':{'gu'}, 'げ':{'ge'}, 'ご':{'go'},
            'ざ':{'za'}, 'じ':{'zi', 'ji'}, 'ず':{'zu'}, 'ぜ':{'ze'}, 'ぞ':{'zo'},
            'だ':{'da'}, 'ぢ':{'di', 'ji'}, 'づ':{'du', 'ju'}, 'で':{'de'}, 'ど':{'do'},
            'ば':{'ba'}, 'び':{'bi'}, 'ぶ':{'bu'}, 'べ':{'be'}, 'ぼ':{'bo'},
            'ぱ':{'pa'}, 'ぴ':{'pi'}, 'ぷ':{'pu'}, 'ぺ':{'pe'}, 'ぽ':{'po'}}

katakana = {'ア':{'a'}, 'イ':{'i'}, 'ウ':{'u'}, 'エ':{'e'}, 'オ':{'o'},
            'カ':{'ka'}, 'キ':{'ki'}, 'ク':{'ku'}, 'ケ':{'ke'}, 'コ':{'ko'},
            'サ':{'sa'}, 'シ':{'shi', 'si'}, 'ス':{'su'}, 'セ':{'se'}, 'ソ':{'so'},
            'タ':{'ta'}, 'チ':{'chi'}, 'ツ':{'tsu'}, 'テ':{'te'}, 'ト':{'to'},
            'ナ':{'na'}, 'ニ':{'ni'}, 'ヌ':{'nu'}, 'ネ':{'ne'}, 'ノ':{'no'},
            'ハ':{'ha'}, 'ヒ':{'hi'}, 'フ':{'hu'}, 'ヘ':{'he'}, 'ホ':{'ho'},
            'マ':{'ma'}, 'ミ':{'mi'}, 'ム':{'mu'}, 'メ':{'me'}, 'モ':{'mo'},
            'ラ':{'ra'}, 'リ':{'ri'}, 'ル':{'ru'}, 'レ':{'re'}, 'ロ':{'ro'},
            'ヤ':{'ya'}, 'ユ':{'yu'}, 'ヨ':{'yo'}, 'ワ':{'wa'}, 'ヲ':{'wo', 'o'}, 'ン':{'n'},
            'ガ':{'ga'}, 'ギ':{'gi'}, 'グ':{'gu'}, 'ゲ':{'ge'}, 'ゴ':{'go'},
            'ザ':{'za'}, 'ジ':{'zi', 'ji'}, 'ズ':{'zu'}, 'ゼ':{'ze'}, 'ゾ':{'zo'},
            'ダ':{'da'}, 'ヂ':{'di', 'ji'}, 'ヅ':{'du', 'ju'}, 'デ':{'de'}, 'ド':{'do'},
            'バ':{'ba'}, 'ビ':{'bi'}, 'ブ':{'bu'}, 'ベ':{'be'}, 'ボ':{'bo'},
            'パ':{'pa'}, 'ピ':{'pi'}, 'プ':{'pu'}, 'ペ':{'pe'}, 'ポ':{'po'}}

# Merge (|) two dicts into one and use it for word checking::
kana_table = hiragana | katakana

"""""""""""""""""""""""""""
  FUNCTIONS IMPLEMENTATION 
"""""""""""""""""""""""""""
# Ask player for their name:
def ask_name():
    return input("\tWhat\'s your name: ")

# Helper::
def make_choice(prompt, default=None):
    s = input(prompt).strip()
    if s == "" and default is not None:
        return default
    try:
        return int(s)
    except ValueError:
        print("Value Error: Your choice must be integer.")
        return None
    
def clear():    # Used to clear the board before print or run anything.
    os.system('cls' if os.name == 'nt' else 'clear')


# File handlings::
def save_profile(profile, save_file=data_file):
    data = {
        "profile": {
            "name": profile.name,
            "level": profile.level,
            "xp": profile.xp,
            "tries": profile.tries,
            "accuracy": profile.accuracy,
            "best_time": profile.best_time,
            "avg_time": profile.avg_time
        }
    }
    if not os.path.exists(save_file):
        print("The save file is empty, creating a new one.")
    try:
        with open(save_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("Runtime Error: ", e)
        return False


def load_profile(save_file=data_file):
    global profile  # declare profile (current profile) for data loading.
    
    if not os.path.exists(save_file):
        print("Cannot find your saved file! Create a brand new profile.")
        profile.name = ask_name()
        return {"profile":profile}


    ## Load data from json file and install directly into current profile.
    with open(save_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    profile = Profile(**data["profile"])
    return {"profile":profile}


def save_history(mode, seconds, accuracy, mistakes, save_file=history_file):
    with open(save_file, 'a', encoding='utf-8') as f:
        f.write(str(datetime.now()))
        f.write("\n____________________")
        f.write(f"\nMode:        {mode}")
        f.write(f"\nPlayed Time: {seconds}s")
        f.write(f"\nAccuracy:    {accuracy*100}%")
        f.write(f"\nMistake(s):  {mistakes}")
        f.write("\n____________________\n\n\n\n")

# Comparing and checking:
def word_checking(word_from_system, word_typed):
    if word_typed.strip().lower() in kana_table.get(word_from_system, set()):
        return True
    else:
        return False


# Gameplay::
def gameplay(mode):
    clear()
    # Create random words from hiragana tables (default::50 words)
    words_default = 50 #    << CHANGE (FOR PURPOSE).

    # Based on gameplay mode that player want to play::
    if mode == "hiragana":
        words = random.choices(list(hiragana.keys()), k = words_default)
    elif mode == "katakana":
        words = random.choices(list(katakana.keys()), k = words_default)
    else:
        words = random.choices(list(kana_table.keys()), k = words_default*2) # Doubled number of words if player chose 'both' mode.
    
    # For analytics:
    words_played = 0
    mistakes = 0
    start = datetime.now()  # *Start counting played time*

    while words_played < words_default:    # Default:: 50 words per play
        # Title and input display:
        print(f"\n\t-<|   {words[words_played]}   |>-")
        print(f"\t\t\t[{words_played}/{words_default}]")

        # Player type the romaji and word checking:: (announce for player if it's right or wrong)
        word_type = input("\n\t > ")
        if word_checking(words[words_played], word_type):
            clear()
            print("\tおめでとう 🎉")
            words_played += 1
        else:
            clear()
            print("\tWrong! Type again.")
            mistakes += 1

    end = datetime.now()   # *End counting played time*

    # FINAL RESULT::
    played_time = end - start                      # Played time per run.
    accuracy = 1 - mistakes / words_default        # Since 50 words per run.
    xp_gained = 50 + (words_default * accuracy)    # 50 (based xp per run) + extra.

    # Print the result to player's screen and ask if they want to play again::
    clear()

        ## Formatting for played time display::
    seconds = played_time.total_seconds()
    if seconds >= 60:
        formatted_time = f"{int(seconds / 60)}m {int(seconds % 60)}s"
    else:
        formatted_time = f"{int(seconds)}s"

        ## Based on the mistake(s) that player made, grant them an encouragement::
    if mistakes == 0:
        congrats = random.choice(["\tYou\'ve made ZERO mistake. Are you aliens?",
                                 "\t0 mistake. What a genius !"
                                 "\tYou wasn't born in Earth, right?"])
    elif mistakes <= 5:
        congrats = random.choice(["\tThat\'s so good. Keep it better !",
                                 "\tFantastic. Keep going !"])
    elif 5 < mistakes <= 15:
        congrats = "That\'s good! Keep grinding, my friend."
    elif 15 < mistakes <= 25:
        congrats = "That\'s a great step. You can do much better !"
    else:
        congrats = "Don't worry! Your result could be better if you grind more."

        ## Print to the screen::
    print(f"""
    -= =< A N A L Y T I C S >= =-
        Played time: {formatted_time}
        Accuracy   : {(accuracy*100):.2f} %
        Mistakes   : {mistakes}
    ______________________________
    {congrats}
          """)
    
    # Transfer to player data and automatically save to file + history::
    profile.add_tries()
    profile.add_xp(xp_gained)
    profile.compute_accuracy(accuracy)
    profile.compute_avgtime(seconds)
    profile.compare_besttime(seconds)

    save_profile(profile)
    save_history(mode, seconds, accuracy, mistakes)


def handle_choice(choice):
    match choice:
        case 1:
            clear()
            gameplay("hiragana")

        case 2:
            clear()
            gameplay("katakana")

        case 3:
            clear()
            gameplay("both")

        case 4:
            clear()
            print(profile)

        case 5:
            clear()
            save_sure = make_choice("\tDo you want to save file?\n\t [YES]::1 | [NO]::0\n\n\t > ")
            if save_sure:
                save_profile(profile)
                print("File saved successfully.")

        case 6:
            clear()
            load_sure = make_choice("\tDo you want to load file?\n\t [YES]::1 | [NO]::0\n\n\t > ")
            if load_sure:
                if load_profile():
                    print("File loaded successfully.")
                else:
                    profile.name = ask_name()

        case 0:
            clear()
            print("\tAre you sure to exit?")
            print("\t [YES]::1 | [NO]::0")
            while True:
                exit = make_choice("\n\t > ")
                match exit:
                    case 1:
                        return True
                    case 0:
                        clear()
                        print("\tGoing back to menu.")
                        return False
                    case _:
                        pass

        case _:
            clear()
            print("Index Error: Your choice must be in bounds [1/2/3/4/0]")
            

def show_menu():
    print("""
    --= =< K A N A    G R I N D I N G >= =--
         [][][][][][][][][][][][][][][]
          
          <1> HIRAGANA PRACTICE
          <2> KATAKANA PRACTICE
          <3> BOTH PRACTICE
          <4> SHOW PROFILE
          <5> SAVE PROFILE
          <6> LOAD PROFILE
          <0> EXIT

          """)

def main():
    clear()
    # Ask player to load their saved file or make a brand new profile.
    load_sure = make_choice("\tDo you want to load file?\n\t [YES]::1 | [NO]::0\n\n\t > ")
    if load_sure:
        if load_profile():
            print("File loaded successfully.")
        else:
            profile.name = ask_name()
    else:
        profile.name = ask_name()

    # PROGRAM STARTS HERE::
    while True:
        show_menu()
        choice = make_choice("\t >> ")
        if handle_choice(choice):
            print("Good bye, my friend.")
            break

if __name__ == "__main__":
    main()