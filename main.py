import copy

def satisfies_greys(word, greys):
    """
    :param greys: { 0 : 'a' ...}
    :return:
    """
    return not any( (let in word) for let in greys)

def satisfies_yellow(word, yellows):
    """

    :param word:
    :param yellow: [ (0, 'a'), ... ]
    :return:
    """
    for ind, let in yellows:
        if not (let in word and word[ind] != let):
            return False
    return True


def satisfies_greens(word, greens):
    """

    :param word:
    :param greens: { 0 : 'a' ... }
    """
    return not any( [word[ind] != v for (ind, v) in greens.items() ] )


def generate_best_word(potential_words, dictionary, unique = False, greens = {}, yellows = {}, greys = set()):
    """
        generates the next best word by finding best highest frequency per letter

    """
    print('Word Choices')
    best_score = 0
    best_word = None
    for word in dictionary:
        if unique:
            if len(set(word)) != len(word):
                continue
        if greens and not satisfies_greens(word, greens):
            continue
        if yellows and not satisfies_yellow(word, yellows):
            continue
        if greys and not satisfies_greys(word, greys):
            continue

        word_score = 0
        for letter_i in range(len(word)):
            word_score += potential_words[letter_i].get(word[letter_i], 0)
        if word_score > best_score:
            best_score = word_score
            best_word = word
            print(best_word, best_score)
    return best_word


def main():
    tests()
    # generate letter frequencies by index
    dictionary_file = [line.strip() for line in open('5letters.txt').readlines()]
    freq = dict( (i, {}) for i in range(0, 5) )
    """
    freq: { 0 : 
            { 'a' : 1,
              'b' : 2, ...
            }
          ...}  
            
    
    """
    for word in dictionary_file:
        for index, d in freq.items():
            freq[index][word[index]] = freq[index].setdefault(word[index], 0) + 1

    potential_words = copy.deepcopy(freq)
    greens = {}
    greys = set()
    yellows = []
    generate_best_word(potential_words, dictionary_file, True, greens, yellows, greys)
    # INPUT
    while True:
        g = input('Input all greys like: a b c d:\n').rstrip().split(' ')
        if len(g) != 1:
            greys.update(g)
        y = input('Input all yellows like: 0 z 3 g:\n').rstrip().split(' ')
        if len(y) != 1:
            for token_i in range(0, len(y), 2):
                yellows.append((int(y[token_i]),y[token_i + 1] ))


        green = input('Input all greens like: 0 z 3 g:\n').rstrip().split(' ')
        if len(green) != 1:
            for token_i in range(0, len(green), 2):
                greens[int(green[token_i])] = green[token_i + 1]

        print('Greys:   ', greys)
        print('Yellows: ', yellows)
        print('Greens:  ', greens)
        generate_best_word(potential_words, dictionary_file, True, greens, yellows, greys)

def tests():
    greys = {'a', 'b'}
    word1 = 'abcde'
    word2 = 'edcba'
    assert(not satisfies_greys('bfklj', greys))
    assert(not satisfies_greys(word1, greys))
    assert(not satisfies_greys(word2, greys))
    assert(not satisfies_greys('bakdf', greys))
    assert(satisfies_greys('jfkdl', greys))

    yellows = [ (1, 'a') , (0, 'r') ]
    assert(satisfies_yellow('abref', yellows))
    assert( not satisfies_yellow('faifj', yellows))
    assert(satisfies_yellow('fjrak', yellows))
    assert(not satisfies_yellow('rbakd', yellows))

if __name__ == '__main__':
    main()
