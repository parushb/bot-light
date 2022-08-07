import discord


class Profile:
    ENABLED = True
    ALIASES = ['p']
    DESCRIPTION = 'View your profile'

    class Image:
        ENABLED = True
        ALIASES = ['i']
        DESCRIPTION = 'View your profile image'


class Memes:
    ENABLED = True
    ALIASES = ['m']
    DESCRIPTION = 'Search for memes on tenor'
    TERMS = [
        "Error",
        "Excited",
        "Funny",
        "Happy",
        "Surprised",
        "Tired",
        "omg"
    ]

class Clear:
    ENABLED = True
    ALIASES = ['clean']
    DESCRIPTION = 'Clear the terminal'


class Ban:
    ENABLED = True
    ALIASES = ['b']
    DESCRIPTION = 'Ban a user from the server'


class UnBan:
    ENABLED = True
    ALIASES = ['ub']
    DESCRIPTION = 'Unban a user from the server'


class Kick:
    ENABLED = True
    ALIASES = ['k']
    DESCRIPTION = 'Kick a user from the server'


class Mute:
    ENABLED = True
    ALIASES = ['m']
    DESCRIPTION = 'Mute a user from the server'


class UnMute:
    ENABLED = True
    ALIASES = ['um']
    DESCRIPTION = 'Unmute a user from the server'


class Say:
    ENABLED = True
    ALIASES = ['s']
    DESCRIPTION = 'Make the bot say something'


class Translate:
    ENABLED = True
    ALIASES = ['t', 'trans']
    DESCRIPTION = "Translate text from one language to another"


class Prefix:
    ENABLED = True
    ALIASES = ['s']
    DESCRIPTION = 'Change the Bot\'s Prefix'

class boredom:
    ENABLED = True
