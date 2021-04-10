from django.db import models

class Topic(models.Model):
    name = models.CharField("Тема", max_length = 30)
    description = models.TextField("Описание")
    urls = models.SlugField(max_length = 160, unique = True)

    def __str__(self):
        return self.name

class Word (models.Model):
    name = models.CharField("Слово",max_length = 30)
    translate = models.CharField("Перевод",max_length = 30)
    example = models.CharField("Пример",max_length = 100)
    id_topic = models.ForeignKey(Topic, on_delete = models.CASCADE)

    def __str__(self):
        return self.name


class Synonym(models.Model):
    id_word = models.ManyToManyField(Word, verbose_name = "Синоним", related_name = "word_syn")
    name = models.CharField("Синоним", max_length=30)

    def __str__(self):
        return self.name

class Userr (models.Model):
    id_login = models.PositiveIntegerField("ID", default =0)
    balls = models.PositiveIntegerField("Баллы", default =0)

class State(models.Model):
    id_user = models.ForeignKey(Userr, on_delete=models.CASCADE)
    id_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    status = models.BooleanField()



