from slackclient import SlackClient
from private import SLACK_TOKEN

slack_client = SlackClient(SLACK_TOKEN)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user:
                print('{0:20}{1}'.format(user['name'], user.get('id')))
    else:
        print('Could not connecto to slack')
