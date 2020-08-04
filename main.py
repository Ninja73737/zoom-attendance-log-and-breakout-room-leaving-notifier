from flask import Flask, request, Response
import os
import subprocess
import json
import dateutil.parser
import pytz
import tzlocal
from dateutil import tz
from datetime import datetime,tzinfo,timedelta

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

@app.route('/webhook', methods=['POST'])
def respond():
    data = request.json
    event = data['event']
    if event == "meeting.started":
        os.system("echo Participant,Type,Action,Time > log.csv")
    elif event == "meeting.ended":
        # Getting meeting start time
        rawTime = data['payload']['object']['start_time']
        parsedTime = dateutil.parser.parse(rawTime)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utcTime = parsedTime.replace(tzinfo=from_zone)
        localTime = utcTime.astimezone(to_zone)
        formattedStartTime = localTime.strftime('%A, %B %-d, %H %M %S')

        # Getting meeting end time
        rawTime = data['payload']['object']['end_time']
        parsedTime = dateutil.parser.parse(rawTime)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utcTime = parsedTime.replace(tzinfo=from_zone)
        localTime = utcTime.astimezone(to_zone)
        formattedEndTime = localTime.strftime('%H %M %S')

        command = "mv log.csv 'logs/" + formattedStartTime + " - " + formattedEndTime + ".csv'"
        os.system(command)
    elif event == "meeting.participant_joined":
        type = data['payload']['object']['type']
        userName = data['payload']['object']['participant']['user_name']
        rawTime = data['payload']['object']['participant']['join_time']
        parsedTime = dateutil.parser.parse(rawTime)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utcTime = parsedTime.replace(tzinfo=from_zone)
        localTime = utcTime.astimezone(to_zone)
        formattedTime = localTime.strftime('%H:%M:%S')
        action = "join"
        outputCommand = "echo '" + userName + "," + str(type) + "," + action + "," + formattedTime + "' >> log.csv"
        os.system(outputCommand)
    elif event == "meeting.participant_left":
        type = data['payload']['object']['type']
        userName = data['payload']['object']['participant']['user_name']
        rawTime = data['payload']['object']['participant']['leave_time']
        parsedTime = dateutil.parser.parse(rawTime)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utcTime = parsedTime.replace(tzinfo=from_zone)
        localTime = utcTime.astimezone(to_zone)
        formattedTime = localTime.strftime('%H:%M:%S')
        action = "leave"
        try:
            checkActionCommand = "tail -r log.csv | grep -m 1 \"" + str(userName) + "\" | grep leave"
            lastAction = subprocess.check_output(checkActionCommand, shell=True)
            os.system("osascript -e 'display notification \"" + userName + "\" with title \"Someone May Have Left or Moved\"'") 
        except subprocess.CalledProcessError as e:
            pass
        outputCommand = "echo '" + userName + "," + str(type) + "," + action + "," + formattedTime + "' >> log.csv"
        os.system(outputCommand)

    return Response(status=200)
