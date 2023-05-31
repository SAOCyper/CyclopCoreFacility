from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import filters

chatbot = ChatBot("Cyclop",
                  preprocessors=[
                        'chatterbot.preprocessors.clean_whitespace'
                    ],
                  
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  logic_adapters=[
                        {
                         'import_path':'chatterbot.logic.BestMatch',
                         'default_response':'Üzgünüm . Buna cevap veremem',
                         'maximum_similarity_threshold':0.80
                        },
                        {'import_path':'CyclopLogicAdapter.TimeLogicAdapter'},
                        {'import_path':'CyclopLogicAdapter.MathematicalAdapter'},
                        {'import_path':'CyclopLogicAdapter.CyclopLightsLogicAdapter'}
                    ],
                  filters=[filters.get_recent_repeated_responses],
                  database_uri='sqlite:///database.sqlite3',

                  )


conversation = [
    "Cyclop ışıkları kapatabilir misin ?",
    "Tabiki ışıklar kapatılıyor",
    "Teşekkürler ",
    "Başka bir isteğiniz var mıydı?",
    "Yapılacaklar listemi söyleyebilir misin ?",
    "Anlaşıldı.",
]
conversation2 = [
    "Nasılsın ?",
    "İyiyim sizleri sormalı",
    "Teşekkürler ben de iyiyim.",
    "Sen kimsin ?",
    "Ben Cyclop.Akıllı Ev Asistanı",
    "Neler yapabilirsin?",
    "Spotify , Netflix gibi uygulamalara bağlanabilir. İnternete erişim sağlayabilirim",
    "Bu nasıl olacak peki ?",
    "Birçok farklı sistem ve ekipmanla donatıldım.Ben bu iş için yaratıldım",
    "Sana nasıl güvenebiliriz?",
    "Bunu asla bilemezsin .D"
]

#Yaratıcılarım tarafından sadece sahiplerime hizmet etmek için yaratıldım.Onlar bile sistemime erişemezler.
trainer = ListTrainer(chatbot)
trainer.train(conversation)
trainer.train(conversation2)

while True:
    try:
        bot_input = chatbot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break