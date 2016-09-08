from private import BOT_NAME, BOT_ID

# Search text to match for messages to the bot
AT_BOT = '<@' + BOT_ID + '>'

# How long to wait between checking slack
SLEEP_TIME = 1

# Max number of cards returned
MAX_CARDS = 10

# Ordered list that the logic in the bot can take
PARAM_LIST = [ 'name', 'set', 'cost', 'cmc', 'colors', 'supertypes', \
'type', 'subtypes', 'rarity', 'power', 'toughness' ]

# The help text
HELP_TEXT = "```To use this bot simply metion it and give it a name to search like 'elesh norn' or a word to search on.\n" \
+ "To perform an advanced search use the syntax @<MTGCardBot> name=\"<name>\" set=\"<set>\" etc. The allowed values are:" \
+ " name, set, cost, cmc, colors, supertypes, type, subtypes, rarity, power, toughness.```"
