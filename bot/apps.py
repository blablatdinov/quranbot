from django.apps import AppConfig


# class InterstoreAppConfig(AppConfig):
#     name = "bot"  # Здесь указываем исходное имя приложения
#     verbose_name = "Бот"  # А здесь, имя которое необходимо отобразить в админке


class BotConfig(AppConfig):
    name = 'bot'
    verbose_name = "Бот"  # А здесь, имя которое необходимо отобразить в админке
