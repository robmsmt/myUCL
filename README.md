# ![myUCL](img/big-jezza-512.png)

## What is it?

A simple Alexa skill to reveal timetable for UCL students. Simply say "Alexa, open myUCL"!


## Install Guide

### Prerequisites
 1. You need an amazon AWS account with some credit (students recieve $100 for free with [AWS educate])(https://aws.amazon.com/education/awseducate/apply/)
 2. You need an Alexa Echo/Dot or have the ability to test [some other way](https://www.raspberrypi.org/blog/amazon-echo-homebrew-version/). 
 3. You need to have signed up for [Alexa skills kit](https://developer.amazon.com/edw/home.html#/) on the Developer link
 3. You need to locate your UCL ICS academic calender link. To do this: 
  1. Log into your [timetable](https://timetable.ucl.ac.uk/tt/homePage.do) with your UCL username and password.
  2. Click on the subcribe link on the top RHS of the calender:
  ![subscribe](img/subscribe.png)
  3. Copy and paste the URL given and save it, you'll need it later.
  ![url](img/url.png)
   *note- this should work for any ICS calender or any universtiy, not just UCL.*

### Setup 
 1. Let's make a new directory to put everything in. You can rename this or put in whatever directory you like but for the rest of the tutorial we will use this.
```bash
mkdir ~/myUCL
```
 2. Let's clone the github repo (don't forget the dot)
```bash
cd ~/myUCL; git clone https://github.com/rmsmith88/myUCL.git .
```

 3. We need a virtual environment for our Python folder to go in- let's install it. (* note - this is especially important in this tutorial because later we use Zappa to configure the automatic upload to AWS lambda)
```python
pip install virtualenv
```
 4. Now we need to create the virtual environment:
```bash
virtualenv ~/myUCL/py27
```
 5. We must activate this virtual environment so this new python folder is being used. As this command is run you'll notice the virtual environment name, in this case py27 will proceed the bash symbol.
```bash
source ~/myUCL/py27/bin/activate
```
 6. We are now ready to install the libaries with PIP
```python
pip install flask flask-ask unidecode ics zappa awscli
```
 7. Copy the example json config file found in configs folder and create a new file. Name the new file `config.json`. If you open this file you need to paste in the UCL ICS ID that you found earlier as a prereq. Please remove the `webcal://` part and have it in the same format as the example.
 
 8. It's a simple FLASK server so let's run it and see that it works:
 ```python
 python run.py
 ```
 ```bash
 python run.py 
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 142-139-224
 ```
 Ok great, we can cancel that by pressing CTRL+C
 

### Setting up AWSCLI & Zappa
Follow this YouTube tutorial to setup AWSCLI and Zappa
[![Setup](https://img.youtube.com/vi/mjWV4R2P4ks/0.jpg)](https://www.youtube.com/watch?v=mjWV4R2P4ks)

### Creating the Alexa Skill
If you've followed all of the YouTube tutorial above you'll have gone on to create the Alexa skill. I will assume you've not done this:
 1. Goto Alex Skill website. 
 
 2. Add the name and innvocation name as myUCL. Click next.
 ![skill name](img/skill_name.png)
 3. Set the intents to as follows:
 ```json
 {
    "intents": [{
        "intent": "YesIntent"
    },
                
    {
        "intent": "NoIntent"
    }]
}
```
 4. Set the sample utterances:  
  ```json  
YesIntent sure
YesIntent yes

NoIntent no
NoIntent go away
  ```
 5. For ENDPOINT you need to use HTTPS and use the AWS Lambda link that Zappa gave you OR you can use NGROK endpoint if you are testing locally. 
![endpoint](img/endpoint.png)
Don't forget on the next page to select the Certificate as `My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority`


That should be it! It should now work on your Alexa as a developer skill. To enable it open your Alexa app and select skills.
 
 
#### Option2 - test locally using NGROK instead of Zappa 

Remember that step earlier where we ran the run.py file to check that everything was working? We can use NGROK to route that local server so that Alexa can use it (this is instead of AWS Lambda)

 1. Download https://ngrok.com/download
 2. Put ngrok in the directory of your app
 3. Make sure that FLASK server is running again, `python run.py`
 4. Run ngrok with `ngrok http 5000`
 5. It will give you the url that can be accessed externally e.g. 
 `http://66c8dd9b.ngrok.io`  
 You can put this as your end point on the AWS page.


## Todo
 1. Add functionality (deadlines, command multiple weeks, date queries etc)
 2. Save cal to disk rather than requesting each time.
 3. TBC