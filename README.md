# Takshi #
 *A bot for anyone who is frustrated of group management bots*

## Table of Contents ##
 So much recursion, so much wow.
 
 0. [Table of Contents](#table-of-contents)
 1. [What is it ?](#what-is-it-)
 2. [Disadvantages Of Group Management Bots](#disadvantages-of-group-management-bots)
 3. [What Is A Gateway Group ?](#what-is-a-gateway-group-)
 4. [What Is The Need Of A Bot In Gateway Group ?](#what-is-the-need-of-a-bot-in-gateway-group-)
 5. [Features](#features)
 6. [Quick Start](#quick-start)
 7. [Installation](#installation)
  - [Required](#required)
  - [Installing](#installing)
  - [Initialising Database Table](#initialising-database-table)
  - [Environment Variables](#environment-variables)
  - [Launching The Bot](#launching-the-bot)
 8. [Help Or Bugs](#help-or-bugs)
 9. [Enjoy](#enjoy)

## What Is It ? ##
 Takshi is a Telegram bot to help you maintain gateway groups with peace of heart. It automatically removes unverified users,
 reminds unapproved users, generates and refreshes invite link automatically.

## Disadvantages Of Group Management Bots ##
 Normally, when you make a super-group in Telegram, you add a group-management bot to moderate the group. Most of such bots come with
 support for captcha and spam removal. But do they really work ?
 
 1. With a lot of members, there could be silent spammers.
 2. In a public group, anyone can read the messages and harvest members list.
 3. A lot of our users are stuck under spammers personally messaging them.
 4. You can't take a risk by allowing a random bot to moderate the group.
 5. Even if you have a moderator bot, it doesn't prevent spammers from stealing the group data or pinging members in personal message.
    (Remember, to see members list in a public group, you need not me it's member !)

## What Is A Gateway Group ? ##
 Gateway group acts as a firewall to remove spammers. Only users who are verified from it can access original group.
 The working of a gateway group is simple.
 
 1. You make a super-group of the required name (gateway group).
 2. There you add only admins.
 3. The original group will be kept private (real group).
 4. Users who want to join the original group, has to message in the gateway group.
    Their message should convey admins that the person has real interest in joining the group and is not a **spammer**.
 5. If an admin finds the message legit, he or she approves the user and adds him / her to the private group.
 
## What Is The Need Of A Bot In Gateway Group ? ##
 The model of gateway group is unbeatable. The issue starts when admin needs to add a user to private group. let's see how.
 
 1. Not every user has a username or settings that allow them to be added to groups. So you need to ask them to change their privacy
    settings. This consumes time.
 2. A bad user (a rival from your past life), can prove they are legit, can prove they are legit. Then they may click on
    *Report Spam and Leave*. This reports your group and can end in serious trouble based on your luck.
 3. If your group is very popular, you may need to add a lot of members manually. This could hinder Telegram's flood limits and may get
    your account temporarily banned !
 
 With these issues, the only good solution is giving the users an invite link of the private group. But you can't send the link in public
 group. So you need to personal message them the link. But when you do so, a bad user (a rival to your pet) can *Report Spam and Block* you.
 
 To avoid this, you can ask the legit users to personal message you for an invite link. You send them the link and revoke it after the
 user joins.
 
**Short and simple, Takshi automates the above task for you.**
 
## Features ##
 1. Automatic reminders  
  Some users join the gateway group and just forget. The bot takes care of reminding them (without using water to wake them up).
 2. Periodic removals  
  There are some good users who join the gateway group and just never care about any reminders. The bot automatically removes them.
 3. Refreshes invite links  
  The bot refreshes the invite links to avoid being stolen.
 4. Integrated network  
  The bot links its personal message, gateway group, real group and admins group. This offers additional facility in moderation, as you will
  see in later sections.
 5. Written in Python, 100 % free and open source  
  You need not pay the developers, think of them or even thank them. Deploy the bot yourself, and enjoy life.

## Quick Start ##
 For you all, who are not ready to host the bot yourself, you can use the instance I host.
 It is available under name [@TakshiBot](http://t.me/TakshiBot). Start the bot and type `/create`.
 Then the bot will tell you what to do.
 Have a look at the [Wiki](https://github.com/J-Arun-Mani/Takshi/wiki) for description of commands and extras.
 Please be aware that this instance runs on a free plan in Heroku, so you know, anything unexpected may happen at expected times.

## Installation ##
 Deploying the bot is easy. Have some patience, a bottle of water, some good Internet connection. Keep any attacking items away to avoid
 hurting yourself.
 
### Required ###
 1. Python  
  The bot is written in [Python](https://python.org), so install it if not done already.
 2. Python Telegram Bot  
  The bot uses [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) package for interacting with Telegram API.
 3. PSYCOPG  
  To acces PostgreSQL databases, we need this [PSYCOPG](https://www.psycopg.org).
 4. A bot token  
  You can get this free of cost using Telegram's [@BotFather](https://t.me/BotFather).
 5. A place to host your bot  
  This may cost you money. There are free solutions available too, for example [Heroku](https://heroku.com). If you can keep your computer or
  laptop running for hours, you can **host the bot yourself** !
  For more info, refer to [Where to host bots ?](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots)
 6. PostgreSQL  
  This a powerful free and open source database. There is 99.9% chance your hosting solution offers this database. If you go for personal
  hosting, then you can easily setup PostgreSQL in your system.
  Check out [PostgreSQL website](www.postgresql.org).

### Installing ###
 If you have managed to set up the required, deploying the bot can be a breeze.
 1. [Clone this repository](https://www.wikihow.com/Clone-a-Repository-on-Github) into your hosting space or personal computer if you are deploying.
 2. Add the bot to required groups (gateway, private group and admins group), then make it admin with full rights.
 3. Setup the database table and environment variables (explained below).
 4. Start the bot.
 
### Initialising Database Table ###
 There is a good chance, PostgreSQL already made a database for you. If not, you need to [create](https://www.postgresqltutorial.com/postgresql-create-database/) it.
 After that, you need to create the table. Say you have cloned the repository to `Downloads` directory, then open a terminal and type :
 ```
  $ cd Takshi
  $ psql -f data/init.sql
 ```
 In short, you need to execute the file `Takshi data/init.sql` (or it's contents) in `PSQL`.

### Environment Variables ###
 The way to modify the working of bot is through [environment variables](https://en.wikipedia.org/wiki/Environment_variable).
 Specifying them depends on your hosting solution and operating system.

| Name               | Description                                                                       |
|--------------------|---------------------------------------------------------------------------------- |
| `ALLOW_CREATE`     | If `True`, allows others to use your bot in their group. Only affects new groups. |
| `DATABASE_URL`     | Database URL allows a connection to the database instance.                        |
| `PORT`             | The port the server and connections should be handled on.                         |
| `TOKEN`            | The token you obtained using Bot Father.                                          |
| `URL`              | URL of the hosted bot, not needed if hosted personally.                           |

#### More Info ####
 * What is Database URL ? - [Database URL](https://stackoverflow.com/questions/3582552/postgresql-connection-url)

### Launching The Bot ###
 Wow, you managed to come till here ! Running the bot is just a command.
 You need to open the terminal and set the directory to the cloned folder. In hosting solutions, it's quite a different way, look at the
 documentation of the hosting solution.
 If you are hosting on your own :
  ```
   $ python3 -m Takshi -p
  ```
 If you are hosting it in a dedicated solution :
  ```
   $ python3 -m Takshi
  ```

 After starting, open Telegram and message your bot. Send it a `/create` and follow the steps. That's it !

 If this didn't work, don't worry. Find what is causing the issue and try to tackle it. You may open an issue here if you want my help.
 Also, you can try the instance I [host](#quick-start).

## Help Or Bugs ##
 Please file an issue.
 
## Enjoy ##
 Everything should be working fine now. If not, tell me why.
