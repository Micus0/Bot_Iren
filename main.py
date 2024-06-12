from bot import Bot
from data_manager import DataManager

username = str(input("Inserire l'username: "))
password = str(input("Inserire la password: "))

bot = Bot()
bot.log_in(username, password)
bot.go_to_activity()
data = bot.get_data()

data_manager = DataManager(data)
data_manager.create_csv()

