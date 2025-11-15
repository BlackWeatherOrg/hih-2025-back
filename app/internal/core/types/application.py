from enum import Enum


class ApplicationCategoryEnum(Enum):
    interesting = 'Интересное'
    all_apps = 'Все приложения'
    finance = 'Финансы'
    government = 'Государственные'
    utilities = 'Полезные инструменты'
    transport = 'Транспорт и навигация'
    shopping = 'Покупки'
    communication = 'Общение'
    entertainment = 'Развлечения'
    classifieds = 'Объявления и услуги'
    business = 'Бизнес-сервисы'
    health = 'Здоровье'
    travel = 'Путешествия'
    education = 'Образование'
    books = 'Книги'
    lifestyle = 'Образ жизни'
    sport = 'Спорт'
    news = 'Новости и события'
    parents = 'Родителям'
    pets = 'Питомцы'
    betting = 'Ставки и лотереи'
    food = 'Еда и напитки'

    @classmethod
    def values_list(cls) -> list[str]:
        return [e.value for e in cls]

    @classmethod
    def values_dict(cls) -> dict:
        res = {}
        for e in cls:
            res[e.name] = e.value
        return res

