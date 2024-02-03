import time, random, requests, json
import antihackers_engine

antihackers_engine.calls = 0
accept_const = 1
antihackers_engine.move = 0
antihackers_engine.testMove = 0
your_token = input("Enter token: ")
api = "Bearer "+your_token
k = 0
c2 = 0
allowed = ['Std']
while 1:
 try:
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
#                      k = 1
#                      startPosition = FENtranslate2(json.loads(i).get("game").get("fen"))
                      if (json.loads(i).get("game").get("color") == "black"):
                           our_color = 1
                      else: our_color = 0
                      if (json.loads(i).get("game").get("isMyTurn")):
                           c2 = 1
                      else: c2 = 0
                      break
            if (json.loads(i).get("type") == "challengeDeclined"): continue
            chlId = json.loads(i).get("challenge").get("id")
            opponent = json.loads(i).get("challenge").get("challenger").get("name")
            variant = json.loads(i).get("challenge").get("variant").get("short")
            try:
                allowed.index(variant)
            except:
                r = requests.post(
                     "https://lichess.org/api/challenge/"+chlId+"/decline",
                     headers = {"Authorization" : api},
                     json = {"reason" : "variant"}
                )
                antihackers_engine.append_to_jornal("Declined challenge from " + opponent + ": variant")
            control = json.loads(i).get("challenge").get("timeControl").get("limit")
            if (control):
                control = control / 60
                print("control: ", control)
                if (json.loads(i).get("challenge").get("timeControl").get("finalColor") == "black"):
                    our_color = 1
                else: our_color = 0
                break
            else:
                 r = requests.post(
                   "https://lichess.org/api/challenge/"+chlId+"/decline",
                   headers = {"Authorization" : api},
                   json = {"reason" : "variant"}
                 )
 except:
   time.sleep(60)
   continue
 startPosition = antihackers_engine.FENtranslate2("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
 antihackers_engine.a = startPosition.copy()
 antihackers_engine.rightMovesArray = []
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
# print(r.status_code)
 antihackers_engine.append_to_jornal("Antihackers_Botik playing game " + gameId + "..")
 skip = 0
 start = 0
 if (our_color) and (not k): skip = 1
 for i in r.iter_lines():
    if (i):
       if ( json.loads(i.decode('utf-8')).get("type") == "chatLine" ): continue
       print(json.loads(i.decode('utf-8')))
       if (not start):
           if (json.loads(i.decode("utf-8")).get("white")) and (json.loads(i.decode("utf-8")).get("white").get("id") == "abotwith3200rating"):
              our_color = 'w'
           else:
              our_color = 'b'
              skip = 1
           start = 1
       if (skip):
           skip = 0
           continue
       lastSq = ""
       antihackers_engine.a = startPosition.copy()
       antihackers_engine.move = 0
       #print("OK")
       moves = json.loads(i.decode('utf-8'))
       moves = moves.get("moves")
       if (moves): moves = moves.split(" ")
       #print(moves)
       if moves:
           for i in moves:
                antihackers_engine.uncode(i)
                antihackers_engine.move = antihackers_engine.move + 1
                #print(i, move)
       antihackers_engine.show_board(antihackers_engine.a)
       our_move = antihackers_engine.FENtranslate(antihackers_engine.a, 1)
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
           r = requests.post(
               "https://lichess.org/api/bot/game/"+gameId+"/move/e7e5",
               headers = {"Authorization" : api}
           )
           start = 1
 antihackers_engine.append_to_jornal("Game over")
 antihackers_engine.calls = 0
 k = 0
 c2 = 0
