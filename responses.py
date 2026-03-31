from random import choice, randint


def rollDice() -> str:
    dice = randint(1, 6)
    match dice:
        case 1:
            return ':one:'
        case 2:
            return ':two:'
        case 3:
            return ':three:'
        case 4:
            return ':four:'
        case 5:
            return ':five:'
        case 6:
            return ':six:'

def getResponse(userInput: str) -> str:
    lowered: str = userInput.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, Thanks!'
    elif 'bruh' in lowered:
        return 'bruh'
    elif 'gyat' in lowered:
        return 'gyat'
    elif 'roll dice' in lowered:
        return rollDice()
    else:
        return choice(['nuh uh',
                       'goofy ahh',
                       'skibidi ohio gyat rizz'])
