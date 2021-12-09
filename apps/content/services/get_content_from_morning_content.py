def get_content(ayats, additional_content):
    """Получить утренний контент."""
    result = ''
    if additional_content != '':
        result += f'{additional_content}\n\n'
    for ayat in ayats:
        result += f'<b>{ayat.sura.number}:{ayat.ayat})</b> {ayat.content}\n'
    if result != '':
        result += f"\nСсылка на источник: <a href='https://umma.ru{ayats[0].sura.link}'>umma.ru</a>"
    return result
