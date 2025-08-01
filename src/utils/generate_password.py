import random
import string


def generate_password(length: int, letters=True, digits=True, punctuation=False) -> str:
    '''
    Função responsável por gerar uma senha aleatória.

    Args:
        length (int): a quantidade de caracteres da senha.
        letters (bool): se a senha deve conter letras.
        digits (bool): se a senha deve conter dígitos.
        punctuation (bool): se a senha deve conter símbolos.

    Returns:
        string: a senha gerada.
    '''

    character_set = letters * string.ascii_letters + digits * \
        string.digits + punctuation * string.punctuation
    if not character_set:
        return ''
    return ''.join(random.choice(character_set) for _ in range(length))
