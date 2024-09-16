import json, os, time, requests, cloudscraper

from discord_webhook import DiscordWebhook, DiscordEmbed
from webserver import keep_alive

keep_alive()

os.system(f'title Bloxflip Rain Notifier MADE BY R1K ^')

with open("config.json", "r") as config:
  config = json.load(config)

webhook_enable = config['webhook_enabled']
webhookurl = config['webhook']
winnotif = config['windows_notification']
minimum = config['minimum_amount']
ping = config['webhook_ping']
refresh = config['refresh_rate']

if webhook_enable == "True":
  webhook = DiscordWebhook(url=webhookurl, content=f"{ping}")



while True:
    try:
     
      scraper = cloudscraper.create_scraper()
      r = scraper.get('https://rest-bf.blox.land/chat/history').json()
      check = r['rain']
      if check['active'] == True:
          if check['prize'] >= minimum:
            grabprize = str(check['prize'])[:-2]
            prize = (format(int(grabprize),","))
            host = check['host']
            getduration = check['duration']
            convert = (getduration/(1000*60))%60
            duration = (int(convert))
            waiting = (convert*60+10)
            sent = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(int(time.time())))
            print(f"Bloxflip Rain! (MADE BY R1K)\nRain amount: {prize} R$\nExpiration: {duration} minutes\nHost: {host}\nTimestamp: {sent}\n\n")
            if webhook_enable == "True":
              userid = requests.get(f"https://api.roblox.com/users/get-by-username?username={host}").json()['Id']
              thumburl = (f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&height=50&width=50&format=png")
              embed = DiscordEmbed(title=f"{host} is hosting a chat rain!", url="https://bloxflip.com", color=0x0011ff)
              embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
              embed.add_embed_field(name="Expiration", value=f"{duration} minutes")
              embed.add_embed_field(name="Host", value=f"[{host}](https://www.roblox.com/users/{userid}/profile)")
              embed.set_timestamp()
              embed.set_thumbnail(url=thumburl)
              webhook.add_embed(embed)
              webhook.execute()
              webhook.remove_embed(0)
          else:
            time.sleep(130)

          time.sleep(waiting)
      elif check['active'] == False:
        time.sleep(refresh)
    except Exception as e:
      print(e)
      time.sleep(refresh)
      
keep_alive()
