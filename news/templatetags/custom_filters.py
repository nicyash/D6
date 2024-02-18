from django import template
import string


register = template.Library()


# bad_words = ['дурак', 'редиска']



@register.filter()
def censor(text):
    text_list = text.split()
    censored_text_list = []
    bad_words = ['дурак', 'редиска']

    for word in text_list:
        clean_word = ''.join(c for c in word if c not in string.punctuation)
        if clean_word.lower() in bad_words:
            censored_word = clean_word[0] + (len(clean_word) - 1) * '*'
            censored_text_list.append(word.replace(clean_word, censored_word))
        else:
            censored_text_list.append(word)

    return ' '.join(censored_text_list)
