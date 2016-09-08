#!/bin/bash

# Default values
user='mtgslackbot'
prefix='/opt'
systemd_dir='/etc/systemd/'
create_user=1

# Parse command line args
for i in "$@"; do
	case $i in
		# Get the directory prefix to install into
		--prefix=*)
		prefix="${i#*=}"
    	shift
    	;;
		--systemd-dir=*)
		systemd_dir="${i#*=}"
		shift
        ;;
		-u=*|--no-create-user=*)
		if [ -z "${i#*=}" ]; then
			user='root'
			create_user=0
		else
			user="${i#*=}"
		fi
		shift
		;;
		-h|--help)
		cat << EOM
This script adds mtgslackbot as a service on your system using systemctl to
control a systemd service. It installs the necessary files, sets up the python
environment, and installs the service.

OPTIONS:
--prefix=<prefix_dir>    Directory to install the bot to. Defaults to /opt

--systemd-dir            Directory systemd services are installed to. Defaults
                           to /etc/systemd

--no-create-user=[user]  Skip creating a dedicated user. Defaults to creating
 -u=[user]                 mtgslackbot system account. If [user] is given, it
                           will own the service. Otherwise, the service will be
                           owned by and run as root (NOT RECOMMENDED)

-h --help                Show this help message
EOM
		exit 0
		;;
	esac
done

if [[ $EUID -ne 0 ]]; then
	# Must be root to run
	echo 'This script must be run as root in order to set up systemd configs' 1>&2
	exit 1
fi

install_dir="$prefix/mtgslackbot"

# Create folder and copy files
mkdir -p $install_dir
cp mtg-slackbot.py settings.py requirements.txt $install_dir
cp private.py.example $install_dir/private.py

# Set up virtualenv
pushd $install_dir
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
popd

echo
# Ask the user for environment info
echo "Enter your Slack API token: "
read SLACK_TOKEN

echo "Enter your bot's username: "
read BOT_NAME

BOT_ID=`SLACK_TOKEN=$SLACK_TOKEN $install_dir/venv/bin/python find_user_id.py | grep $BOT_NAME | awk '{print substr($0, index($0, $2))}'`

cat > $install_dir/.env <<-EOM
SLACK_TOKEN=$SLACK_TOKEN
BOT_NAME=$BOT_NAME
BOT_ID=$BOT_ID
EOM

cat <<- EOM

Environment configuration stored at $install_dir/.env
If you are having problems with the bot connecting, please check that the
information in that file is correct.
EOM

# Create user and reset permissions
if [ $create_user > 0 ]; then
	useradd -r -s /bin/nologin $user
	chown -R $user:$user $install_dir
fi

systemd_file="$systemd_dir/system/mtgslackbot.service"
cat > $systemd_file <<- EOM
[Unit]
Description=Slack bot for looking up Magic cards
After=syslog.target

[Service]
Type=simple
User=$user
WorkingDirectory=${install_dir}
ExecStart=${install_dir}/venv/bin/python ${install_dir}/mtg-slackbot.py
Restart=on-failure
EnvrionmentFile=${install_dir}/.env

[Install]
WantedBy=multi-user.target
EOM

cat <<- EOM

Service installed at $systemd_dir/system/mtgslackbot.service
Run 'systemctl start mtgslackbot' to start the service, or 'systemctl enable
mtgslackbot' to run it on system start
EOM
