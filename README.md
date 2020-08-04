# zoom-attendance-log-and-breakout-room-leaving-notifier

This Flask project is designed to handle webhooks from Zoom, with the following "Event Subscriptions":

![Example App](example-app.gif)

This project uses a method of sending applescript notifications on Mac by running an `os.system` command. Please note that it also uses OS commands for moving, renaming, and outputting to log files so it may require some modifications to run on non-UNIX-based operating systems. I would be happy to approve changes that replace the shell scripts with a python-native method for performing these actions, I've simply used them for now because I'm much more familiar with bash scripting than python.
