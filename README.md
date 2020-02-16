# MCStatus Discord Bot

This bot was made to keep track of how many players are in a minecraft server at a time. It will display current players and max players in the bot's status like so:

![](https://i.imgur.com/cZ9T8pl.png)

```
usage: bot.py [-h] [-ip IP] [-p PORT]

optional arguments:
  -h, --help                            show this help message and exit
  -ip IP, --ip IP                       the address of a minecraft server
  -p PORT, --port PORT                  the port of a minecraft server
  -f FREQUENCY, --frequency FREQUENCY   amount of time (in seconds) the bot will wait to refresh the discord status

```

Command Prefix: `?`
### Commands:
- players: displays an embed of the amount of players online, as well as a list of their names

---

## Getting Started:

create credentials.json in the same directory as bot.py

it should look something like this:

```
{
    "discord_secret_key":"actual_stuff_here",
}
```

To start the bot with docker, first build the image

```
docker build -t mcstatus .
```

after the image is built, you can run it and pass arguments for ip and port

```
docker run -d mcstatus -ip "localhost" -p "25565"
```