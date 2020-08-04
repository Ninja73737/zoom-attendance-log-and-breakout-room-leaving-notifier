# zoom-attendance-log-and-breakout-room-leaving-notifier

This Flask project is designed to handle webhooks from Zoom, with the "Event Subscriptions" demonstrated in the following example:

![Example App](example-app.gif)

When setting up this project please create a symlink to the directory where you would like to back the logs up to in the project folder with the name "Webhooks Logs symlink", or alternatively remove that section from the code or edit the name to fit your symlink. This project uses a method of sending applescript notifications on Mac by running an `os.system` command. Please note that it also uses OS commands for moving, renaming, and outputting to log files so it may require some modifications to run on non-UNIX-based operating systems. I would be happy to approve changes that replace the shell scripts with a python-native method for performing these actions, I've simply used them for now because I'm much more familiar with bash scripting than python.
