import matplotlib.pyplot as plt
specials = ['END', 'Opening Credits', 'Closing Credits', 'Commercial Break']
phrases = ['good morning', 'good night', 'i love you', 'we were on a break', 'my eyes', 'mom', 'dad']


# This function finds how many lines each character has.
# It follows only the main character
# Returns the result as dictionary with keys = names and values = number of lines
def most_script(text, words):
    dict = {'Joey': 0, 'Monica': 0, 'Phoebe': 0, 'Chandler': 0, 'Ross': 0, 'Rachel': 0}
    for line in text:
        for name in dict.keys():
            if line.startswith(name):
                if words:
                    words_count = len(line.split()) - 1
                    dict[name] += words_count
                else:
                    dict[name] += 1
                break
    return dict


# This function removes the show directions from the text which are nested within different kind of brackets.
# It returns the entire text
def remove_brackets(line):
    result = ''
    paren = 0
    for ch in line:
        if ch == '(':
            paren = paren + 1
            result = result
        elif (ch == ')') and paren:
            result = result
            paren = paren - 1
        elif not paren:
            result += ch
    return result


# This function is responsible for cleaning the script in order to get the raw text of the show
# It removes director comments, signs, directions, titles, credits and more
# It returns the clean text for further functions
def get_clean_text(text, limit):
    count = limit
    split_string = text.split('\n')
    new_text = []
    for p in split_string:
        if not (p.isupper()) and not (p in specials) and not (p.startswith('Written') or p.startswith('[')):
            result = remove_brackets(p)
            if result != "":
                new_text.append(result)
        if count != -1:
            if count == 0:
                return new_text
            else:
                count -= 1
    return new_text


# This functions checks number of appearances for a single phrase
def phrase_look_up(text, phrase):
    count = 0
    for line in text:
        count += line.lower().count(phrase)
    return count


# This functions responsible for searching for different phrases in the show.
# It already has few phrases to check and the user is able to add another one
# As a result, it returns a dictionary where keys = phrases and values = number of appearances
def check_phrases(text):
    print("The current phrases I'm looking for are:")
    print(phrases)
    print('You are free to add phrases of you own!')
    phrase = input('For Example: add \'how you doin?\':\n->')
    if phrase != "":
        phrases.append(phrase)
    dict = {}
    for p in phrases:
        dict[p] = phrase_look_up(text, p)
    return dict


# Self explanatory...
def creat_graph(x_side, y_side, dict):
    keys = dict.keys()
    names = []
    results = []
    for k in keys:
        names.append(k)
        results.append(dict[k])
    plt.scatter(names, results)
    plt.xlabel(x_side)
    plt.ylabel(y_side)
    plt.rcParams.update({'font.size': 10})
    plt.tick_params(labelrotation=45)
    plt.show()


# Self explanatory...
def creat_graph_bars(x_side, y_side, dict):
    keys = dict.keys()
    names = []
    results = []
    left = []
    count = 0
    for k in keys:
        names.append(k)
        results.append(dict[k])
        count += 1
        left.append(count)
    plt.bar(left, results, tick_label=names,
            width=0.8, color=['red', 'green'])
    plt.xlabel(x_side)
    plt.ylabel(y_side)
    plt.rcParams.update({'font.size': 10})
    plt.tick_params(labelrotation=-45)
    plt.show()


# This function collects all the line of a specific character, chosen by the user
# It allows free choice, which in case of no character will have 0 lines.
# After creating the file, as txt file, it prints and returns the number of lines of the character.
def chose_character(text):
    character = input("chose character:\n").lower().capitalize()
    file_lines = 0
    new_file = []
    for line in text:
        if line.startswith(character):
            new_file.append(line + '\n')
            file_lines += 1
    if file_lines <= 0:
        print('no lines were found!\n')
        return -1
    else:
        with open('all_characters_lines.txt', 'w') as f:
            f.writelines(new_file)
            print(f'All of {character} lines are written at the \'all_characters_lines.txt\' file\n')
            print(f'{file_lines} lines in total\n')
        return file_lines


# This function prints a specific line of the file that was created
# It handles numbers that are too big or too small by choosing line number 2.
def print_specific_line(file_lines):
    line = input(f'chose a number between 1-{file_lines}:\n')
    if not(int(line) in range(1, file_lines+1)):
        print('Number mot in range, default line number -> 2 instead\n')
        line = 2

    file = open("all_characters_lines.txt")
    for index, line_content in enumerate(file):
        if index == int(line) - 1:
            print(line_content)
    file.close()


def main():
    path_of_file = 'Friends_Transcript.txt'
    text = open(path_of_file, 'r').read()
    text = get_clean_text(text, -1)
    sentences_for_character = most_script(text, False)
    words_for_character = most_script(text, True)
    phrases_count = check_phrases(text)
    creat_graph('character', 'sentences', sentences_for_character)
    creat_graph('character', 'words', words_for_character)
    creat_graph_bars('phrase', 'count', phrases_count)
    file_lines = chose_character(text)
    if file_lines > 0:
        print_specific_line(file_lines)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
