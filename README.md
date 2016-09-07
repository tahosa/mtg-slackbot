# mtg-slackbot
Something like a basic bot to attach to a slack server and respond to Magic: the Gathering based queries.

Requires:
* Python 3.4+
* mtgsdk
* slackclient
* Your own SLACK_TOKEN for your own bot in your own private.py

Basic Use:
The bot will respond to mention queries and do a pretty simple case-insensative search on card names. It also will respond to wiki/subreddit-bot style mid-sentence queries surrounded by [[<name>]]. Additionally, there is an advanced search feature that takes specific keys and will search with them. It does some formatting of the result(s) it returns, and does a substitution of the {} for :: to allow the use of slack's custom emoji to make the results look even nicer.

Notes:
The bot is not perfect and is still in very early alpha. It only gets the first copy of any given card it finds and returns that one, which sometimes means promos or alpha version. It does return the oracle text, but the image might be weird. Sometimes it won't get the image. Sometimes it will hang on a search. Sometimes it's dumb. Use at your own risk.

| Advanced Search Keys  |
| ---- |
| name |
| set  |
| cost* |
| cmc  |
| colors* |
| supertypes* |
| type* |
| subtypes* |
| rarity |
| power |
| toughness |

\* - still not fully tested

---
Examples:
```
Cody S [2:21 PM]  
@mtgcardbot fireball

MTGCardBotBOT [2:21 PM]  
1 results
Fireball  :mx::mr:
Sorcery
Common LEA
Fireball deals X damage divided evenly, rounded down, among any number of target creatures and/or players.
Fireball costs :m1: more to cast for each target beyond the first.

http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=197&type=card
```
---
```
Cody S [2:23 PM]  
@mtgcardbot set="ktk" cmc="4" subtypes="warrior"

MTGCardBotBOT [2:23 PM]  
3 results
Timely Hordemate  :m3::mw:
Creature — Human Warrior
Uncommon KTK
Raid — When Timely Hordemate enters the battlefield, if you attacked with a creature this turn, return target creature card with converted mana cost 2 or less from your graveyard to the battlefield.

http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=386699&type=card (126KB) 
Bellowing Saddlebrute  :m3::mb:
Creature — Orc Warrior
Uncommon KTK
Raid — When Bellowing Saddlebrute enters the battlefield, you lose 4 life unless you attacked with a creature this turn.

http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=386488&type=card (134KB) 
Unyielding Krumar  :m3::mb:
Creature — Orc Warrior
Common KTK
:m1::mw:: Unyielding Krumar gains first strike until end of turn.
_"The man whom I call father killed the orc who sired me, offering his world and his blade in return."_
http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=386710&type=card (135KB)
```
---
```
Cody S [2:24 PM]  
I finally got my [[elesh norn]] for my modern deck

MTGCardBotBOT [2:24 PM]  
1 results
Elesh Norn, Grand Cenobite  :m5::mw::mw:
Legendary Creature — Praetor
Special pJGP
Vigilance
Other creatures you control get +2/+2.
Creatures your opponents control get -2/-2.
_"The Gitaxians whisper among themselves of other worlds. If they exist, we must bring Phyrexia's magnificence to them."_
```