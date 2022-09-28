from ohbot import ohbot

def blinkLids():
    while BLINKING:
        ohbot.move(LIDBLINK, 0, spd = 10)
        ohbot.wait(0.1)
        ohbot.move(LIDBLINK, 10, spd=10)
        ohbot.wait(0.1)
        ohbot.wait(random.randrange(2,10))



t1 = threading.Thread(target=blinkLids, args=())
t1.start()