def change_highscore(game, highscore):
    f = open("HighScore.txt")
    text = f.read().split()
    text = strify(text)
    f.seek(0)
    line = f.readline().strip()
    count = 0
    for word in text:
        count += 1
        if game in str(word):
            text[count] = highscore
    text = strify(text)
    text = ' '.join(text)
    f.close()
    f = open("HighScore.txt", 'w')
    f.write(text)
    f.close()
    

def get_highscore(game):
    f = open("HighScore.txt")
    text = f.read().split()
    count = 0
    for word in text:
        count += 1
        if game.lower() in str(word.lower()):
            f.close()
            return int(text[count])

def strify(item):
    return [str(i) for i in item]
