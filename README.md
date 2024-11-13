# What is Day By Day?

Day by day is a self-hostable discord bot that attempts to gameify the tough work of actually sitting down and doing something on a project every day. 

# How does it intend to accomplish this?

The bot is intended to be used by a small community and features a leaderboard that individuals can compete for by making commits on their github repos. 
The bot reads incoming github webhooks and converts them into points, awarding more points for a user's first commit of the day and a small amout for every subsequent commit that day.

Every week, the bot will also ping anyone who hasn't pushed a change to a repo within that last week to remind them to do something!

# These are very loose and exploitable parameters, are you stupid?

They are! Both by design, and because I can't be bothered to go in any further depth. 
However in all seriousness, the lack of hard parameters (for example, how large a commit is) is intended, as I want to encourage myself to make a change regardless of size every day. 
The system is designed to be very kind to people who miss days or can't get a lot done at any point. 
Write 1000 lines of code or add a #TODO, your effort is valid, and is better than not doing anything at all. Be kind to yourself! <3

# How can I get this thing running?

At a base level you need to rename the `secret.json.tmp` file here to just `secret.json` and paste your token where it says "TOKEN_GOES_HERE" then you're free to host the thing. 
Add the github webhooks to your webhook channel, and run a test or push something to a repo to get an output.
Make sure to run the `$init_leaderboard` and `$init_webhook` commands in their respective channels, feeding the webhook bot's (not this bot's) id into the latter command. 
Finally you'll want each user to run `$register` feeding in their github username, and you should be good from there :)

If you're looking for anything more in depth, there are a good number of steps that go into this, including going through the discord developer portal and setting up the sever/ bot, 
so I'm not going to go through all the effort to define those steps here, as I don't anticipate anyone other than myself actually using this thing.
If, however, anyone IS going to do just that please feel free to open up an issue on this github and I'd be happy to either help you directly or just complete this section myself.

# Can I contribute?

Wow, what a self indulgent question to put on a README that no one will see! 
If you are, in fact, seeing this and do want to contribute, relevant PRs are more than welcome, (and I will give you free hugs if u open one).
