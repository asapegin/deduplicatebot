# deduplicatebot
Telegram bot that removes new duplicate messages from the group and issues a warning.

You need to run this bot on your server and register it using id and password received from BotFather. If you would like my hosted bot to do a service for you instead, feel free to contact me then.

The bot reads all new messages from the group (channels/topics are also supported) and saves them in the local DB. If the database will be bigger than 20k messages, the bot will delete first 10k messages from it. In case the same user publishes the same message in the same group/topic, bot will delete it and write a warning text mentioning the username (text is now hardcoded in the code). If the user deletes the original message and publish it again, the bot will be able to recognise it and allow  re-publishing. The deletion check is realised via pinning and then immediately unpinning the message (deleted message cannot be pinned).
