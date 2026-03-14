from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# bad_words = ['bad', 'ugly', 'stupid']
#
# def bad_word_validator(value: str):
#     for bad_word in bad_words:
#         if bad_word in value.lower():
#             raise ValidationError(f'The content contains inappropriate language: {bad_word}')
@deconstructible
class BadWordValidator:
    def __init__(self, bad_words=None, message=None):
        self.bad_words = bad_words
        self.message = message
        
    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, value):
        self.__message = value or 'The content contains inappropriate language'

    def __call__(self, value: str):
        for bad_word in self.bad_words:
            if bad_word in value.lower():
                raise ValidationError(self.message)
