
BOT_NAME = 'MTGCardBot'

BOT_ID = 'U2660SL06'

AT_BOT = '<@' + BOT_ID + '>'

SLEEP_TIME = 1

MAX_CARDS = 10

PARAM_LIST = [ 'name', 'set', 'cost', 'cmc', 'colors', 'supertypes', \
'type', 'subtypes', 'rarity', 'power', 'toughness' ]

HELP_TEXT = "```To use this bot simply metion it and give it a name to search like 'elesh norn' or a word to search on.\n" \
+ "To perform an advanced search use the syntax @<MTGCardBot> name=\"<name>\" set=\"<set>\" etc. The allowed values are:" \
+ " name, set, cost, cmc, colors, supertypes, type, subtypes, rarity, power, toughness.```"