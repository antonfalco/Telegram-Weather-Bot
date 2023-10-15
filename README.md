# Telegram-Weather-Bot
A bot that uses a weather API to fetch current, forecast or hourly weather data based on the city provided.

You will first need to go and get a free API code from here:  https://www.weatherapi.com/

Once you have this code, you will need to install Telegram, create a weather bot, and get an API from there. You search for BotFather in the Telegram search. After following the prompts, you'll create a bot and acquire an API that you'll use in the script. 

After making the bot and acquiring both the APIs for the bot and from weatherapi.com, replace the placeholder information in the script with your information and your Telegram bot should provide you with presentable information pulled directly from the API. 

Note: you will need to have this script running at all times. Otherwise, any API requests from Telegram will not be received. In my case, I have a Raspberry PI 4 acting as an always on server with this python script installed, so I can make requests anytime. You don't need a PI, of course, but wherever you have your script running (current PC, VM, old laptop, etc) must stay running with this script. 

Example results on Telegram app:
![Screenshot_20231015-164128](https://github.com/antonfalco/Telegram-Weather-Bot/assets/108304747/74da87c5-db39-40fd-8251-43522bc847aa)
![Screenshot_20231015-164111](https://github.com/antonfalco/Telegram-Weather-Bot/assets/108304747/f39b53fe-428c-4aae-a2e4-a92763cf84dd)


