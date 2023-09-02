import random

def getRandomDefaultPic(first_name, last_name):
    first_initial = first_name[0] if not first_name == '' else ''
    last_initial = last_name[0] if not last_name == '' else ''

    # if both initials are not an alphabet, return the fallback default pic
    if first_initial.isalpha():
        letter = first_initial.upper()
    elif last_initial.isalpha():
        letter = last_initial.upper()
    else:
        return 'defaults/fallback.svg'

    pic_colors = ['cobalt_blue', 'bright_red', 'coral_red', 'dark_turquoise', 'gray', 'green', 'magenta', 'orange', 'pink', 'peach', 'yellow']

    random_color = random.choice(pic_colors)    

    random_default_pic = f'defaults/{random_color}/{letter}.png'

    return random_default_pic
