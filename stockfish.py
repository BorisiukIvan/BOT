import requests, json

def ind(sq):
    a = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i in range(0, len(a)): 
         if (sq[0] == a[i]): p1 = i
    p2 = 8 - int(sq[1])
    return p2 * 8 + p1


def getNextMove(fen):
    global our_color
    print(fen)
    try:
     move = json.loads(requests.post("https://chesshub.com/api/v1/fens.json", json={"fen" : fen, "rating" : 10000}).text).get("analysis").get("move")
     final = move.get("from") + move.get("to")
     if (final == "O-O"):
       if (our_color == "w"): return "e1g1"
       return "e8g8"
     elif (final == "O-O-O"):
       if (our_color == "w"): return "e1b1"
       return "e8b8"
     return final
    except Exception as e: print(e)
#    js0n = ["3" + fen]
#    return json.loads(requests.post("https://chesscompass.com/api/get_cache_moves", json=js0n).text)[0][1].get("move")

def convertPosToFEN(pos, lastMove, r1, r2, R1, R2, moves1, moves2, turn):
    res = ''
    k = 0
    for i in range(0, 64):
        if (pos[i] == ' '):
            k = k + 1
        else:
            if (k > 0):
               res = res + str(k)
               k = 0
            res = res + pos[i]
        if (i % 8 == 7):
           if (k > 0): res = res + str(k)
           if (i != 63): res = res + '/'
           k = 0
    res = res + ' ' + turn + ' '
    if (r2): res = res + 'K'
    if (r1): res = res + 'Q'
    if (R2): res = res + 'k'
    if (R1): res = res + 'q'
    if (not r1 + r2 + R1 + R2): res = res + '-'
    if (len(lastMove) == 4) and (pos[ind(lastMove[2] + lastMove[3])].lower() == 'p') and (abs( int(lastMove[3]) - int(lastMove[1]) ) == 2):
       res = res + ' ' + lastMove[2] + str( int ( ( int(lastMove[3]) + int(lastMove[1]) ) / 2 ) )
    else: res = res + ' -'
    res = res + ' ' + str(moves1) + ' ' + str(moves2)
    return res

def show_board(board):
    res = ""
    for i in range(0, len(board)):
         if (board[i] == " "):
              res = res + " . "
         else: res = res + " " + board[i] + " "
         if (i % 8 == 7): res = res + "\n"
    return res

def clear_sq(sq):
    global a
    if (sq == "g1"): squares = [ind("h1"), ind("f1")]
    if (sq == "c1"): squares = [ind("a1"), ind("d1")]
    if (sq == "c8"): squares = [ind("a8"), ind("d8")]
    if (sq == "g8"): squares = [ind("h8"), ind("f8")]
    a[squares[1]] = a[squares[0]]
    a[squares[0]] = " "
    return 1

def ind(sq):
    a = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i in range(0, len(a)): 
         if (sq[0] == a[i]): p1 = i
    p2 = 8 - int(sq[1])
    return p2 * 8 + p1


def uncode(uci):
    global a
    our_move = []
    if (len(uci) < 4): 
       print("<4Error")
       return 0
    if (len(uci) == 5):
          sq1 = uci[0] + uci[1]
          sq2 = uci[2] + uci[3]
          piece = uci[4]
          if (move % 2): 
              a[ind(sq2)] = piece.lower()
          else: a[ind(sq2)] = piece.upper()
          a[ind(sq1)] = " "
#          print("pawn-promote ", lastSq)
          return 1
    elif ( (uci[0] + uci[1] == "e1") and ( (uci[2] + uci[3] == "g1") or (uci[2] + uci[3] == "c1") ) )  or  ( (uci[0] + uci[1] == "e8") and ( (uci[2] + uci[3] == "g8") or (uci[2] + uci[3] == "c8") ) ):
          sq1 = uci[0] + uci[1]
          sq2 = uci[2] + uci[3]
          a[ind(sq2)] = a[ind(sq1)]
          a[ind(sq1)] = " "
#          print(sq1, sq2, ": O-O?")
          if (a[ind(sq2)].upper() == "K"): 
               clear_sq(sq2)
          return 1
    elif ( a[ind(uci[2] + uci[3])] == ' ' ) and ( a[ind(uci[0] + uci[1])].lower() == 'p' ) and (abs(ind(uci[2] + uci[3]) - ind(uci[0] + uci[1])) % 8):
          sq1 = uci[0] + uci[1]
          sq2 = uci[2] + uci[3]
          if (uci[3] == '3'):
             a[ind(uci[2] + '4')] = ' '
          else: a[ind(uci[2] + '5')] = ' '
          a[ind(sq2)] = a[ind(sq1)]
          a[ind(sq1)] = ' '
    elif (len(uci) == 4):
          a[ind(uci[2] + uci[3])] = a[ind(uci[0] + uci[1])]
          a[ind(uci[0] + uci[1])] = " "
#          print("normal-uci", ind(uci[0] + uci[1]), ' ', ind(uci[2] + uci[3]))
          lastSq = 1
          return 1
    else: return 0

def FENtranslate2(pos):
        global move
        res = []
        for i in range(0, len(pos)):
              if (pos[i] == "/"): continue
              if (pos[i] == " "): 
                   p = pos[i+1]
                   break 
              if (pos[i].isnumeric()):
                   n = int(pos[i])
                   for k in range(0, n): res.append(" ")
              else:
                 res.append(pos[i])
        if (p == "w"):
              move = 0
        else: move = 1
        return res

name = 'zarosyt'
calls = 0
accept_const = 1
move = 0
testMove = 0
api = "Bearer "+open("token").read().split("\n")[0]
k = 0
c2 = 0
while 1:
 r = requests.get(
    "https://lichess.org/api/stream/event",
    headers = {"Authorization" : api},
    stream = True
 )
 for i in r.iter_lines():
      if (i):
            i = i.decode('utf-8')
            print(json.loads(i), "TYPE: ", json.loads(i).get("type"))
            if (json.loads(i).get("type") == "gameStart"):
                      chlId = json.loads(i).get("game").get("id")
                      gameId = json.loads(i).get("game").get("id")
                      if (json.loads(i).get("game").get("secondsLeft")):
                          control = json.loads(i).get("game").get("secondsLeft") / 60
                      else: control = 30000
                      k = 1
                      startPosition = FENtranslate2(json.loads(i).get("game").get("fen"))
                      if (json.loads(i).get("game").get("isMyTurn")):
                           c2 = 1
                      else: c2 = 0
                      break
            if (json.loads(i).get("type") == "challengeDeclined"): continue
            chlId = json.loads(i).get("challenge").get("id")
            opponent = json.loads(i).get("challenge").get("challenger").get("name")
            rating = json.loads(i).get("challenge").get("challenger").get("rating")
            if ( json.loads(i).get("challenge").get("variant").get("short") != "Std" ):
                r = requests.post(
                     "https://lichess.org/api/challenge/"+chlId+"/decline",
                     headers = {"Authorization" : api},
                     json = {"reason" : "variant"}
                )
            else:
                if (not accept_const):
                    r = requests.post(
                     "https://lichess.org/api/challenge/"+chlId+"/decline",
                     headers = {"Authorization" : api},
                     json = {"reason" : "later"}
                    )
                else:
                    increment = json.loads(i).get("challenge").get("timeControl").get("increment")
                    control = json.loads(i).get("challenge").get("timeControl").get("limit")
                    if (json.loads(i).get("challenge").get("speed") == "correspondence") or ((increment < 4) and (control < 25*60)):
                        r = requests.post(
                           "https://lichess.org/api/challenge/"+chlId+"/decline",
                           headers = {"Authorization" : api},
                           json = {"reason" : "tooFast"}
                         )
                    elif (control):
                        control = control / 60
                        print("control: ", control)
                        break
                    else:
                         r = requests.post(
                           "https://lichess.org/api/challenge/"+chlId+"/decline",
                           headers = {"Authorization" : api},
                           json = {"reason" : "variant"}
                         )
 if (not k): startPosition = FENtranslate2("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
 a = startPosition.copy()
 rightMovesArray = []
 link = "https://lichess.org/api/challenge/"+chlId+"/accept"
 r = requests.post(
    link,
    headers = {"Authorization" : api}
 )
 gameId = chlId
 #print("OK")
 r = requests.get(
    "https://lichess.org/api/bot/game/stream/"+gameId,
     stream = True,
     headers = {"Authorization" : api}
 )
 print(r.status_code)
 skip = 0
 start = 0
 for i in r.iter_lines():
    if (i):
       if ( json.loads(i.decode('utf-8')).get("type") == "chatLine" ): continue
       if ( json.loads(i.decode('utf-8')).get("type") == "opponentGone" ): continue
       print(json.loads(i.decode('utf-8')))
       if (not start):
           if (json.loads(i.decode("utf-8")).get("white")) and (json.loads(i.decode("utf-8")).get("white").get("id") == name):
              our_color = 'w'
           else:
              our_color = 'b'
              skip = 1
           start = 1
       if (skip):
           skip = 0
           continue
       lastSq = ""
       a = startPosition.copy()
       move = 0
       #print("OK")
       moves = json.loads(i.decode('utf-8'))
       print(moves)
       if (not moves.get("state")) and (moves.get("status") != "started"): break
       moves = moves.get("moves")
       print(moves)
       if (moves): moves = moves.split(" ")
       #print(moves)
       k1 = 1
       q1 = 1
       K1 = 1
       Q1 = 1
       lastMove = ''
       moves1 = 0
       if moves:
           for i in moves:
                lastMove = i
                sq1 = ind(i[0] + i[1])
                sq2 = ind(i[2] + i[3])
                moves1 = moves1 + 1
                if ( (a[sq2] != ' ') or (a[sq1].lower() == 'p') ): moves1 = 0
                uncode(i)
                move = move + 1
                if (a[0] != "r"): K1 = 0
                if (a[4] != "k"):
                      K1 = 0
                      Q1 = 0
                if (a[7] != "r"): Q1 = 0
                if (a[63] != "R"): q1 = 0
                if (a[60] != "K"):
                      k1 = 0
                      q1 = 0
                if (a[56] != "R"): k1 = 0
       #show_board(a)
       our_move = getNextMove(convertPosToFEN(a, lastMove, k1, q1, K1, Q1, moves1, int( ( (move + 1) - (move % 2) ) / 2 ), our_color))
       #print("OK_AY")
       #print(our_move)
#       if (not our_move): break
       link = "https://lichess.org/api/bot/game/"+gameId+"/move/"+str(our_move)
       print("We want to move "+ str(our_move) + "..")
       r = requests.post(
            link,
            headers = {"Authorization" : api}
       )
       if (r.status_code == 200): 
              print("Successfully moved " + our_move)
              skip = 1
              start = 1
       else:
           print(r.text)
 calls = 0
 k = 0
 c2 = 0
