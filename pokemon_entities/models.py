from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Порода по-русски', max_length=200)
    title_en = models.CharField('Порода по-английски', max_length=200, blank=True)
    title_jp = models.CharField('Порода по-японски', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='images', null=True, blank=True)
    description = models.TextField('Описание', blank=True)

    prev_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='next_evolution',
        verbose_name='Эволюционирует из',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField('Координаты, ширина')
    lon = models.FloatField('Координаты, долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        related_name='pokemon_entities',
        verbose_name='Порода покемона',
        on_delete=models.CASCADE,
    )
    appeared_at = models.DateTimeField('Дата и время появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Дата и время исчезновения', null=True, blank=True)

    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title} lvl {self.level}'
