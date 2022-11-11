from ohbot import ohbot


def ohbot_motor_reset():
    ohbot.reset()
    ohbot.move(ohbot.HEADTURN, 5)
    ohbot.move(ohbot.HEADNOD, 5)
    ohbot.wait(2)
    print("Ohbot motors reset!")
