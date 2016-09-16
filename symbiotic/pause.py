

import datetime


ADJUST_UTC = 0
PAUSES = {10, 12, 16}
AROUND = {
    (-0.1, 0): "Il faut aller chercher les gens !",
    (0, 0.1): "On se regroupe dans le couloir",
    (0.1, 0.5): "Tout le monde est probablement déjà partit",
}
DEFAULT_MESSAGE = "Il va falloir patienter."


def detect():
    time = datetime.datetime.now()
    hour = (time.hour - ADJUST_UTC + (time.minute / 60)) % 24
    assert 0 <= hour <= 24
    # print('Heure: {}'.format(hour))
    to_print = None

    for pause_hour in PAUSES:
        for modifier, message in AROUND.items():
            min, max = modifier
            # print(min, max, hour, pause_hour+min < hour, hour <= pause_hour+max)
            if pause_hour-min < hour <= pause_hour+max:
                to_print = message
                break

    print(to_print if to_print else DEFAULT_MESSAGE)
