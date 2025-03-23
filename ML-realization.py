import numpy as np


class User:
    """Класс пользователей площадкой ФильмоПоиск"""

    instances = []  # Список для хранения экземпляров

    def __init__(self, username):
        self.username = username  # Имя пользователя
        self.movie_ratings = {}  # Оценки фильмов пользователя
        self.genre_ratings = {}  # Оценки жанров пользователя
        self.genre_preferences = []  # Любимые жанры пользователя
        User.instances.append(
            self
        )  # Добавляем текущий экземпляр в список всех экземпляров класса

    def add_genre_preferences(self):
        """При регистрации нового пользователя, ему предлагается указать его любимые жанры"""
        print(
            f"Укажите ваши любимые жанры через запятую!\n"
            f"Пример: Фантастика, Триллер, Драма\n"
            f"Жанры представленные на площадке ФильмоПоиск: Фантастика, Драма, Триллер, Экшн, Ужасы, Анимация, Комедия, Детектив, Криминал"
        )
        input_genres_preferences = input("Введите ваши любиме жанры: ")
        genres_preferences_list = input_genres_preferences.split(", ")
        self.genre_preferences = genres_preferences_list
        return Recommendations.recommendation_for_the_new_user(self)

    def add_movie_rating(self, movie, score):
        """Оценка фильма пользователем"""
        self.movie_ratings[movie] = score
        movie.add_rating(score)
        """Присвоение оценки жанру фильма"""
        if movie.genre not in self.genre_ratings:
            self.genre_ratings[movie.genre] = []
        self.genre_ratings[movie.genre].append(score)

    def get_movie_ratings(self):
        """Получение оценок фильмов пользователя"""
        movie_rating_dict = {}
        for movie, score in self.movie_ratings.items():
            movie_rating_dict[movie.title] = score
        return movie_rating_dict

    def get_avg_genre_ratings(self):
        """Получение средней оценки жанров пользователя"""
        avg_genre_ratings = {}
        for genre, ratings in self.genre_ratings.items():
            avg_genre_ratings[genre] = sum(ratings) / len(ratings)
        return avg_genre_ratings

    def __str__(self):
        return f"Пользователь - {self.username}"


class Movie:
    """Класс фильмов на площадке ФильмоПоиск"""

    instances = []  # Список для хранения экземпляров

    def __init__(self, author, title, genre):
        self.author = author  # Имя и фамилия автора
        self.title = title  # Название фильма
        self.genre = genre  # Жанр фильма
        self.ratings = []  # Список оценок пользователей
        Movie.instances.append(
            self
        )  # Добавляем текущий экземпляр в список всех экземпляров класса

    def add_rating(self, score):
        """Добавление оценки пользователя"""
        self.ratings.append(score)

    def get_avg_rating(self):
        """Подсчет средней оценки фильма пользователями"""
        if self.ratings == []:
            return None
        avg_rating = sum(self.ratings) / len(self.ratings)
        avg_rating = round(avg_rating, 1)
        return avg_rating

    def __str__(self):
        return f"'{self.title}': автор {self.author}, жанр - {self.genre}, оценка - {self.get_avg_rating()}"


class Recommendations:
    """Класс с функциями рекомендаций контента пользователям"""

    @staticmethod
    def euclidean_distance(user1, user2):
        """Рассчет расстояния между двумя пользователями на основе оценок одинаковых жанров"""
        similar_genres = (
            user1.get_avg_genre_ratings().keys() & user2.get_avg_genre_ratings().keys()
        )
        if len(similar_genres) == 0:
            return None

        distance = 0
        for genre in similar_genres:
            user1_avg_genre_score = user1.get_avg_genre_ratings()[genre]
            user2_avg_genre_score = user2.get_avg_genre_ratings()[genre]
            distance += (user1_avg_genre_score - user2_avg_genre_score) ** 2
        distance = np.sqrt(distance)
        return distance

    @staticmethod
    def get_avg_genre_rating(genre):
        """Получение средней оценки жанра фильмов"""
        genre_ratings = []
        for movie in Movie.instances:
            if movie.genre == genre:
                movie_avg_rating = movie.get_avg_rating()
                genre_ratings.append(movie_avg_rating)
        avg_genre_rating = sum(genre_ratings) / len(genre_ratings)
        return avg_genre_rating

    @staticmethod
    def recommendation_for_the_new_user(current_user):
        """Рекомендация фильмов для нового пользователя на основе его любимых жанров"""
        recommended_movie = []
        for genre in current_user.genre_preferences:
            avg_genre_rating = Recommendations.get_avg_genre_rating(genre)
            for movie in Movie.instances:
                """Если оценка фильма выше средней оценки фильмов такого же жанра - рекомендуем"""
                if movie.genre == genre and movie.get_avg_rating() > avg_genre_rating:
                    recommended_movie.append(movie.title)
        return f"Рекомендуемые фильмы для нового пользователя {current_user.username}\n{recommended_movie}"

    @staticmethod
    def recommendation_for_the_regular_user(current_user, k):
        """Рекомендация фильмов для регулярного пользователя используя алгоритм k-ближайших соседей"""

        # Определение расстояния до всех пользователей сервиса
        distance_from_current_user_to_users = {}
        for user in User.instances:
            if current_user == user:
                continue
            if Recommendations.euclidean_distance(current_user, user) != None:
                distance_from_current_user_to_users[user] = (
                    Recommendations.euclidean_distance(current_user, user)
                )
        # Сортировка таблицы с расстояниями до всех пользователей по значениям ключей в порядке возрастания
        sorted_distance_from_current_user_to_users = sorted(
            distance_from_current_user_to_users.items(), key=lambda item: item[1]
        )

        # Определение k-ближайших пользователей
        k_nearest_neighbors = sorted_distance_from_current_user_to_users[:k]

        # Определяем список фильмов оцененых ближайшими соседями
        movies_rated_by_nearest_neighbors = []
        for neighbor in k_nearest_neighbors:
            for movie in neighbor[0].movie_ratings:
                movies_rated_by_nearest_neighbors.append(movie)

        # Формируем список рекомендуемых фильмов
        # Если средняя оценка фильма среди ближайших соседей выше 8, то фильм рекомендуется к просмотру
        recommended_movie = []
        for movie in movies_rated_by_nearest_neighbors:
            # Если фильму уже есть в рекомендуемом списке или пользователь уже оценил его, то переидти к следующей итерации цикла
            if movie.title in recommended_movie or movie in current_user.movie_ratings:
                continue
            movie_rating = 0
            rates_count = 0
            for neighbor in k_nearest_neighbors:
                if movie in neighbor[0].movie_ratings:
                    movie_rating += neighbor[0].movie_ratings[movie]
                    rates_count += 1
            avg_movie_rating = movie_rating / rates_count
            if avg_movie_rating > 8:
                recommended_movie.append(movie.title)

        return f"Рекомендации фильмов для {current_user.username}:\n{recommended_movie}"


"""Создание фильмов"""

inception = Movie("Кристофер Нолан", "Начало", "Фантастика")
interstellar = Movie("Кристофер Нолан", "Интерстеллар", "Фантастика")
the_matrix = Movie("Лана и Лилли Вачовски", "Матрица", "Фантастика")
the_shawshank_redemption = Movie("Фрэнк Дарабонт", "Побег из Шоушенка", "Драма")
forrest_gump = Movie("Роберт Земекис", "Форрест Гамп", "Драма")
the_godfather = Movie("Фрэнсис Форд Коппола", "Крестный отец", "Драма")
seven = Movie("Дэвид Финчер", "Семь", "Триллер")
gone_girl = Movie("Дэвид Финчер", "Исчезнувшая", "Триллер")
the_silence_of_the_lambs = Movie("Джонатан Демме", "Молчание ягнят", "Триллер")
the_dark_knight = Movie("Кристофер Нолан", "Темный рыцарь", "Экшн")
mad_max_fury_road = Movie("Джордж Миллер", "Безумный Макс: Дорога ярости", "Экшн")
gladiator = Movie("Ридли Скотт", "Гладиатор", "Экшн")
the_conjuring = Movie("Джеймс Ван", "Заклятие", "Ужасы")
it = Movie("Анди Мускетти", "Оно", "Ужасы")
hereditary = Movie("Ари Астер", "Реинкарнация", "Ужасы")
finding_nemo = Movie("Эндрю Стэнтон", "В поисках Немо", "Анимация")
toy_story = Movie("Джон Лассетер", "История игрушек", "Анимация")
shrek = Movie("Эндрю Адамсон", "Шрек", "Анимация")
the_intouchables = Movie("Оливье Накаш", "1+1", "Комедия")
superbad = Movie("Грег Моттола", "Суперперцы", "Комедия")
groundhog_day = Movie("Гарольд Рэмис", "День сурка", "Комедия")
knives_out = Movie("Риан Джонсон", "Достать ножи", "Детектив")
murder_on_the_orient_express = Movie(
    "Кеннет Брана", "Убийство в Восточном экспрессе", "Детектив"
)
the_girl_with_the_dragon_tattoo = Movie(
    "Дэвид Финчер", "Девушка с татуировкой дракона", "Детектив"
)
the_godfather_part_ii = Movie("Фрэнсис Форд Коппола", "Крестный отец 2", "Криминал")
pulp_fiction = Movie("Квентин Тарантино", "Криминальное чтиво", "Криминал")
goodfellas = Movie("Мартин Скорсезе", "Славные парни", "Криминал")


"""Создание пользователей и их оценок фильмов"""
user1 = User("user1")
user1.add_movie_rating(inception, 8)
user1.add_movie_rating(the_dark_knight, 9)
user1.add_movie_rating(the_godfather, 10)
user1.add_movie_rating(superbad, 7)
user1.add_movie_rating(the_conjuring, 6)

user2 = User("user2")
user2.add_movie_rating(interstellar, 9)
user2.add_movie_rating(the_shawshank_redemption, 10)
user2.add_movie_rating(gone_girl, 7)
user2.add_movie_rating(mad_max_fury_road, 8)
user2.add_movie_rating(pulp_fiction, 9)
user2.add_movie_rating(hereditary, 5)

user3 = User("user3")
user3.add_movie_rating(hereditary, 5)
user3.add_movie_rating(it, 6)
user3.add_movie_rating(the_matrix, 8)
user3.add_movie_rating(gladiator, 9)

user4 = User("user4")
user4.add_movie_rating(the_intouchables, 10)
user4.add_movie_rating(groundhog_day, 9)
user4.add_movie_rating(the_girl_with_the_dragon_tattoo, 8)
user4.add_movie_rating(seven, 7)
user4.add_movie_rating(the_silence_of_the_lambs, 9)
user4.add_movie_rating(inception, 6)
user4.add_movie_rating(mad_max_fury_road, 8)

user5 = User("user5")
user5.add_movie_rating(finding_nemo, 10)
user5.add_movie_rating(toy_story, 9)
user5.add_movie_rating(hereditary, 4)
user5.add_movie_rating(the_conjuring, 5)
user5.add_movie_rating(murder_on_the_orient_express, 8)

user6 = User("user6")
user6.add_movie_rating(the_godfather_part_ii, 10)
user6.add_movie_rating(goodfellas, 9)
user6.add_movie_rating(the_intouchables, 8)
user6.add_movie_rating(superbad, 7)

user7 = User("user7")
user7.add_movie_rating(the_matrix, 9)
user7.add_movie_rating(interstellar, 8)
user7.add_movie_rating(the_dark_knight, 10)
user7.add_movie_rating(groundhog_day, 6)
user7.add_movie_rating(pulp_fiction, 7)

user8 = User("user8")
user8.add_movie_rating(pulp_fiction, 9)
user8.add_movie_rating(gone_girl, 7)
user8.add_movie_rating(hereditary, 5)
user8.add_movie_rating(the_conjuring, 6)
user8.add_movie_rating(mad_max_fury_road, 8)
user8.add_movie_rating(inception, 7)

user9 = User("user9")
user9.add_movie_rating(the_shawshank_redemption, 10)
user9.add_movie_rating(gladiator, 9)
user9.add_movie_rating(the_girl_with_the_dragon_tattoo, 8)
user9.add_movie_rating(seven, 7)

user10 = User("user10")
user10.add_movie_rating(finding_nemo, 10)
user10.add_movie_rating(toy_story, 9)
user10.add_movie_rating(the_intouchables, 8)
user10.add_movie_rating(groundhog_day, 7)
user10.add_movie_rating(the_silence_of_the_lambs, 9)

user11 = User("user11")
user11.add_movie_rating(the_dark_knight, 10)
user11.add_movie_rating(mad_max_fury_road, 9)
user11.add_movie_rating(the_godfather, 10)
user11.add_movie_rating(hereditary, 4)
user11.add_movie_rating(it, 5)
user11.add_movie_rating(gladiator, 8)

user12 = User("user12")
user12.add_movie_rating(the_matrix, 8)
user12.add_movie_rating(interstellar, 9)
user12.add_movie_rating(the_conjuring, 6)
user12.add_movie_rating(superbad, 7)

user13 = User("user13")
user13.add_movie_rating(the_shawshank_redemption, 10)
user13.add_movie_rating(goodfellas, 9)
user13.add_movie_rating(the_girl_with_the_dragon_tattoo, 8)
user13.add_movie_rating(seven, 7)
user13.add_movie_rating(gladiator, 9)

user14 = User("user14")
user14.add_movie_rating(the_intouchables, 10)
user14.add_movie_rating(superbad, 9)
user14.add_movie_rating(groundhog_day, 8)
user14.add_movie_rating(inception, 5)
user14.add_movie_rating(interstellar, 6)

user15 = User("user15")
user15.add_movie_rating(seven, 10)
user15.add_movie_rating(gone_girl, 9)
user15.add_movie_rating(the_silence_of_the_lambs, 10)
user15.add_movie_rating(finding_nemo, 6)
user15.add_movie_rating(toy_story, 7)

user16 = User("user16")
user16.add_movie_rating(the_shawshank_redemption, 10)
user16.add_movie_rating(the_godfather, 10)
user16.add_movie_rating(forrest_gump, 9)
user16.add_movie_rating(hereditary, 5)

user17 = User("user17")
user17.add_movie_rating(the_conjuring, 9)
user17.add_movie_rating(hereditary, 8)
user17.add_movie_rating(it, 10)

user18 = User("user18")
user18.add_movie_rating(mad_max_fury_road, 10)
user18.add_movie_rating(the_dark_knight, 9)
user18.add_movie_rating(gladiator, 8)
user18.add_movie_rating(the_godfather, 7)
user18.add_movie_rating(groundhog_day, 6)

user19 = User("user19")
user19.add_movie_rating(pulp_fiction, 9)
user19.add_movie_rating(goodfellas, 8)
user19.add_movie_rating(the_matrix, 7)
user19.add_movie_rating(the_intouchables, 10)
user19.add_movie_rating(hereditary, 5)

user20 = User("user20")
user20.add_movie_rating(finding_nemo, 10)
user20.add_movie_rating(toy_story, 9)
user20.add_movie_rating(shrek, 8)
user20.add_movie_rating(the_conjuring, 5)
user20.add_movie_rating(hereditary, 4)


"""Реализация рекомендательной системы"""

# Рекомендации для регулярного пользователя используя алгоритм k-ближайших соседей
user21 = User("user21")
user21.add_movie_rating(finding_nemo, 10)
user21.add_movie_rating(the_intouchables, 7)
user21.add_movie_rating(knives_out, 1)
user21.add_movie_rating(the_dark_knight, 6)
user21.add_movie_rating(hereditary, 6)
user21.add_movie_rating(forrest_gump, 9)
print(Recommendations.recommendation_for_the_regular_user(user21, 4))
print('\n')

# Рекомендации для нового пользователя на основе выбранных пользователем им любимых жанров
user22 = User("user22")
print(user22.add_genre_preferences())
