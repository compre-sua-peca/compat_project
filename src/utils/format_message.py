def format_message(message: str) -> str:
    '''
    Função responsável por transformar uma string do tipo "teste" em "Teste."

    Args:
        message (str): a mensagem a ser formatada.

    Returns:
        (str): a mensagem formatada.
    '''

    if message is None:
        return message

    new_message = message.strip()
    new_message = new_message[0].upper() + new_message[1:]

    last_punctuations = ['.', '?', '!', ';', ':', '¿', '¡']

    if new_message[-1] not in last_punctuations:
        new_message += '.'

    return new_message
