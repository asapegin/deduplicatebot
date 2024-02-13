# deduplicatebot
Telegram bot that removes new duplicate messages from the group and issues a warning.

You need to run this bot on your server and register it using id and password received from BotFather. If you would like my hosted bot to do a service for you instead, feel free to contact me then.

The bot reads all new messages from the group (channels/topics are also supported) and saves them in the local DB. In case the same user publishes the same message in the same group/topic, bot will delete it and write a warning text mentioning the username (text is now hardcoded in the code). If the user deletes the original message and publish it again, the bot will be able to recognise it and allow  re-publishing. The deletion check is realised via pinning and then immediately unpinning the message.



Copyright 2024 Dr. Andrey Sapegin
Licensed under the "Attribution-NonCommercial-ShareAlike" Vizsage
Public License (the "License"). You may not use this file except
in compliance with the License. Roughly speaking, non-commercial
users may share and modify this code, but must give credit and 
share improvements. However, for proper details please 
read the full License, available at
https://github.com/asapegin/licenses/blob/main/Vizsage-License-BY-NC-SA
and the handy reference for understanding the full license at 
https://github.com/asapegin/licenses/blob/main/Vizsage-Deed-BY-NC-SA
Please contact the author for any other kinds of use.
Unless required by applicable law or agreed to in writing, any
software distributed under the License is distributed on an 
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
either express or implied. See the License for the specific 
language governing permissions and limitations under the License.
