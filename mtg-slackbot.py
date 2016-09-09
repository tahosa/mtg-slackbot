import time
from os import environ
import private
import settings
import logging
import re
from slackclient import SlackClient
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import MtgException

# Initialize the client
sc = SlackClient( private.SLACK_TOKEN )

## FORMATTING FUNCTIONS
def format_cost( cost ):
	if cost is not None:
		ret = cost.replace( '{', settings.EMOJI_PREFIX ).replace( '}', settings.EMOJI_SUFFIX )
	else:
		ret = cost
	return ret

def format_nameline( name, cost ):
	fmt_string = ''
	fmt_cost = format_cost( cost )
	fmt_string = '{0}'.format( name )
	if cost is not None:
		fmt_string += '  {0}'.format( fmt_cost )
	return fmt_string

def format_flavor( text ):
	fmt_string = ''
	if text is None:
		return fmt_string
	fmt_string = '_{0}_'.format( text.replace( '\n', '_\n_' ) )
	return fmt_string

def format_link( link ):
	fmt_string = ''
	if link is None:
		return fmt_string
	return link

## LOGIC FUNCTIONS
# Wrapper to perform the actual search and return the results
def get_cards( card_name='', card_set='', card_mana_cost='', card_cmc='', card_colors='', \
	card_supertypes='', card_type='', card_subtypes='', card_rarity='', card_power='', card_toughness='' ):
	try:
		cards = Card.where( name=card_name, set=card_set, mana_cost=card_mana_cost, cmc=card_cmc, \
			colors=card_colors, supertypes=card_supertypes, type=card_type, subtypes=card_subtypes, \
			rarity=card_rarity, power=card_power, toughness=card_toughness ).all()
	except MtgException as err:
		cards = []
		logging.critical('Error with card search:\n{}'.format(err))
	return cards

# Peform the query and return the cards as an array of formatted strings
def get_formatted_cards( card_name='', card_set='', card_mana_cost='', card_cmc='', card_colors='', \
	card_supertypes='', card_type='', card_subtypes='', card_rarity='', card_power='', card_toughness='' ):
	responses = []
	unique_cards = []
	cards = get_cards( card_name, card_set, card_mana_cost, card_cmc, \
		card_colors, card_supertypes, card_type, card_subtypes, \
		card_rarity, card_power, card_toughness )
	
	logging.debug('Formatting {} cards'.format(len(cards)))
	for card in cards:
		if card.name in unique_cards:
			continue
		nameline = format_nameline( card.name, card.mana_cost )
		typeline = '{0}'.format( card.type )
		raresetline = '{0} {1}'.format( card.rarity, card.set )
		textline = '{0}'.format( format_cost( card.text ) )
		flavorline = '{0}'.format( format_flavor( card.flavor ) )
		linkline = '{0}'.format( format_link( card.image_url ) )
		unique_cards.append( card.name )
		responses.append( '\n'.join( [nameline, typeline, raresetline, textline, flavorline, linkline] ) )
	return responses

# Parser to understand the rtm output the bot sees and only do something if it's @bot or [[something]]
def parse_input( slack_rtm_output ):
	output_list = slack_rtm_output
	if output_list and len( output_list ) > 0:
		for output in output_list:
			logging.debug( output )
			if output and 'text' in output and settings.AT_BOT in output['text']:
				search = output['text'].split( settings.AT_BOT )[1].strip().lower()
				logging.debug('Bot DMed with term \'{}\' in #{}'.format(search, output['channel']))
				return ([search], output['channel'])
			elif output and 'text' in output and '[[' in output['text']:
				strip_searches = []
				searches = output['text'].split('[[')
				for entry in searches:
					if entry.find(']]') > -1:
						strip_searches.append( entry.split(']]')[0] )
				logging.debug('Found wiki style card(s) \'{}\' in #{}'.format(strip_search, output['channel']))
				return (strip_searches, output['channel'])
	return ([], None)

# Turn an advanced query into a dictionary we can use
def parse_advanced( command ):
	cmd_dict = dict()
	commands = command.split( '\" ' )
	for cmd in commands:
		if cmd.find( ':' ) > -1:
			delim = ':'
		elif cmd.find( '=' ) > -1:
			delim = '='
		param, args = cmd.split( delim, 1 )
		args = args.replace( '\"', '' )
		cmd_dict[param] = args
	return cmd_dict

# Use a dictionary of arguments to perform the search
def adv_get_cards( param_dict ):
	args_dict = dict()
	for param in settings.PARAM_LIST:
		try:
			args_dict[param] = param_dict[param]
		except KeyError:
			args_dict[param] = ''
	return get_formatted_cards( args_dict['name'], args_dict['set'], args_dict['cost'], \
		args_dict['cmc'], args_dict['colors'], args_dict['supertypes'], \
		args_dict['type'], args_dict['subtypes'], args_dict['rarity'], \
		args_dict['power'], args_dict['toughness'] )

# Logic for acting on the basic commands and returns a response to the channel passed in
def handle_command( command, channel ):
	help = False
	response = 'If you can read this, something went wrong.'
	if command.find( '\"' ) > -1:
		cmd_dict = parse_advanced( command )
		cards = adv_get_cards( cmd_dict )
	elif command.startswith( 'help' ):
		response = settings.HELP_TEXT
		cards = None
		help = True
	else:
		if command.find( '|' ) > -1:
			card, set = command.split( '|', 1 )
		else:
			card = command
			set = ''
		cards = get_formatted_cards( card, set )
	if cards is None or len( cards ) < 1:
		if help is False:
			response = 'No cards matching that search.'
	elif len( cards ) > settings.MAX_CARDS:
		response = '{} results.\nMore than {} cards found, please be more specific.'.format( len(cards), settings.MAX_CARDS )
	else:
		cards.insert( 0, '{0} results'.format( len( cards ) ) )
		response = '\n'.join( cards )

	logging.debug( 'Posting {} to #{}'.format( response, channel ) )
	sc.api_call( 'chat.postMessage', channel=channel, \
		text=response, as_user=True )

## Main function
if __name__ == '__main__':
	if 'LOG_LEVEL' in environ:
		logging.basicConfig( level=int( environ['LOG_LEVEL'] ) )
	
	logging.info( 'Starting application' );
	logging.info( 'Connecting to Slack...' );

	if sc.rtm_connect():
		while True:
			command_array, channel = parse_input( sc.rtm_read() )
			if len(command_array) > 0:
				for command in command_array:
					handle_command( command, channel )
			time.sleep( settings.SLEEP_TIME )
	else:
		logging.critical( 'Connection Failed' )
