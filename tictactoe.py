import random


async def tictactoe(channel, client, player1ID, player2ID=None, mode="pvp"):
    board = [[':blue_square:', ':blue_square:', ':blue_square:'],
             [':blue_square:', ':blue_square:', ':blue_square:'],
             [':blue_square:', ':blue_square:', ':blue_square:']]

    currentPlayer = player1ID  # Player 1 always starts
    ongoing = True

    if mode == "pvp":
        await channel.send(f"Player 1 (<@{player1ID}>) is X. Player 2 (<@{player2ID}>) is O.")
    else:
        await channel.send(f"Player (<@{player1ID}>) is X. You are playing against the computer (O).")

    await channel.send("Enter Row'-'Column (e.g., 0-2)")
    await printBoard(board, channel)

    def check(message):
        return message.channel == channel and message.author.id == currentPlayer and message.content.count('-') == 1

    while ongoing:
        try:
            if mode == "pvp" or (mode == "pvc" and currentPlayer == player1ID):
                # Wait for the player's move
                msg = await client.wait_for("message", check=check)
                move = msg.content.split('-')
                if len(move) != 2 or not (move[0].isdigit() and move[1].isdigit()):
                    raise ValueError("Invalid format")
                row, column = int(move[0]), int(move[1])

                if row not in [0, 1, 2] or column not in [0, 1, 2] or board[row][column] != ':blue_square:':
                    raise ValueError("Invalid move")

                # Place the current player's marker
                marker = ':regional_indicator_x:' if currentPlayer == player1ID else ':regional_indicator_o:'
                board[row][column] = marker

                playerName = "Player 1" if currentPlayer == player1ID else "Player 2"
                ongoing = await checkWinner(board, channel, playerName)


                # Switch turns or let computer play
                if ongoing:
                    currentPlayer = player1ID if currentPlayer == player2ID else player2ID

            else:
                await computerMove(board, channel)
                playerName = "Player 1" if currentPlayer == player1ID else "Computer"
                ongoing = await checkWinner(board, channel, playerName)

                if ongoing:
                    currentPlayer = player1ID if currentPlayer == player2ID else player2ID

        except ValueError as e:
            await channel.send(str(e) + " - please enter in the format 'Row-Column' with numbers between 0 and 2.")



# Computer calculated move, Needs a lot of work right now only picks random spots
async def computerMove(board, channel):
    # Find all empty spots on the board
    emptySpots = [(rowIDX, colIDX) for rowIDX, row in enumerate(board)
                   for colIDX, cell in enumerate(row) if cell == ':blue_square:']

    if not emptySpots:
        return  # No moves left

    # Choose a random empty spot for the computer's move
    row, column = random.choice(emptySpots)
    board[row][column] = ':regional_indicator_o:'


# Print current board state
async def printBoard(board, channel):
    await channel.send(f'{board[0][0]}{board[0][1]}{board[0][2]}\n'
                       f'{board[1][0]}{board[1][1]}{board[1][2]}\n'
                       f'{board[2][0]}{board[2][1]}{board[2][2]}')


async def checkWinner(board, channel, player):
    await printBoard(board, channel)
    won = False

    # Check for win
    if board[0][0] == board[0][1] == board[0][2] and board[0][0] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[1][0] == board[1][1] == board[1][2] and board[1][0] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[2][0] == board[2][1] == board[2][2] and board[2][0] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[0][0] == board[1][0] == board[2][0] and board[0][0] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[0][1] == board[1][1] == board[2][1] and board[0][1] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[0][2] == board[1][2] == board[2][2] and board[0][2] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[0][0] == board[1][1] == board[2][2] and board[0][0] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] in (':regional_indicator_x:', ':regional_indicator_o:'):
        won = True

    if won:
        await channel.send(f'{player} Won!')
        return False

        # Check for a draw
    if all(cell != ':blue_square:' for row in board for cell in row):
        await channel.send("It's a draw!")
        return False

    return True
