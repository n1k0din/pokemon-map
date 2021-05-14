from django.db import models  # noqa F401


class Pokemon(models.Model):    
    title = models.CharField('Порода по-русски', max_length=200)
    title_en = models.CharField('Порода по-английски', max_length=200)
    title_jp = models.CharField('Порода по-японски', max_length=200)
    image = models.ImageField('Изображение', upload_to='images', null=True, blank=True)
    description = models.TextField('Описание', null=True, blank=True)

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
    lon = models.FloatField('Координаты, долготоа')
    pokemon = models.ForeignKey(Pokemon, verbose_name='Порода покемона', on_delete=models.CASCADE)
    appeared_at = models.DateTimeField('Дата и время появления')
    disappeared_at = models.DateTimeField('Дата и время исчезновения')

    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье')
    strength = models.IntegerField('Сила')
    defence = models.IntegerField('Защита')
    stamina = models.IntegerField('Выносливость')

    def __str__(self):
        return f'{self.pokemon.title} lvl {self.level}'
