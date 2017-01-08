from flask import Flask
from flask_ask import Ask, statement, question, session
# import sys
import json
# import random

from ics import Calendar, Event
from urllib2 import urlopen
import arrow

app = Flask(__name__)
ask = Ask(app, "/")
config_file = "configs/config.json"


def get_cal():
    # looks at config.json and retrieves cal info from web link

    load = {}

    # open cal from url
    try:
        with open(config_file) as data:
            load.update(json.load(data))
    except IOError:
        print("file configs/config.json not found")
        raise

    assert 'ics_url' in load
    url = load['ics_url']

    c = Calendar(urlopen(url).read().decode('iso-8859-1'))

    #add ucl term dates as all day events
    e = Event()
    e.name = "First day of Term 1"
    e.begin = '20160926 00:00:00' #Monday 26 September 2016
    e.make_all_day()
    c.events.append(e)
    e = Event()
    e.name = "Last day of Term 1"
    e.begin = '20161216 00:00:00'  #Friday 16 December 2016
    e.make_all_day()
    c.events.append(e)
    e = Event()
    e.name = "First day of Term 2"
    e.begin = '20170109 00:00:00' #Monday 09 January 2017
    e.make_all_day()
    c.events.append(e)
    e = Event()
    e.name = "Last day of Term 2"
    e.begin = '20170324 00:00:00'  #Friday 24 March 2017
    e.make_all_day()
    c.events.append(e)
    e = Event()
    e.name = "First day of Term 3"
    e.begin = '20170424 00:00:00'  #Monday 24 April 2017
    e.make_all_day()
    c.events.append(e)
    e = Event()
    e.name = "Last day of Term 3"
    e.begin = '20170609 00:00:00'  #Friday 09 June 2017
    e.make_all_day()
    c.events.append(e)

    #save cal
    # todo cache cal rather than downloading each time
    #with open('my.ics', 'w') as f:
    #    f.writelines(c)

    return c


@ask.launch
def start_skill():
    welcome_message = 'Hello, do you want me to tell you what lectures you have today?'
    return question(welcome_message)


@ask.intent("YesIntent")
def get_lectures_today():
    cal = get_cal()  # returns cal object

    returnstr = ""

    #get datetime and store as arrow datetime obj
    dt = arrow.utcnow()

    #override the utcnow day  - for test purposes
    #dt = dt.replace(days=+1)

    dayNum = int(dt.format("d"))  # returns day as 1-7 for Mon-Sun
    weekend = [6, 7]

    if dayNum in weekend:
        # SAT OR SUN
        inc = 1 if dayNum == 7 else 2  # if sat then inc=2 otherwise sunday inc=1 add to dt to get to Mon
        lec = cal.events.on(dt.replace(days=+inc))

        if len(lec) < 1:
            returnstr = "It's a weekend and it looks like you don't have any Monday lectures. "
                        # "do you study humanities? Ahem"
        else:
            returnstr += "It's a weekend, but here are Monday's lectures: "
            for e in lec:
                returnstr += "'{}' starting {}".format(e.name, e.begin.humanize())

    else:
        # weekday -> return days lectures
        lec = cal.events.on(dt)
        if len(lec) < 1:
            returnstr += "Looks like you don't have any lectures."
        else:
            returnstr += "Today you have: "
            for e in lec:
                returnstr += "'{}' starting {}".format(e.name, e.begin.humanize())

    return statement(returnstr)


@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Ok goodbye'
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)
