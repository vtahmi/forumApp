from  django.db import models
class LanguageChoices(models.TextChoices):
    PYTHON = 'PY', 'Python'
    JAVASCRIPT = 'JS', 'JavaScript'
    JAVA = 'JA', 'Java'
    CSHARP = 'CS', 'C#'
