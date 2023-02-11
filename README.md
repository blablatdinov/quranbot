# Quranbot

[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Hits-of-Code](https://hitsofcode.com/github/blablatdinov/quranbot)](https://hitsofcode.com/github/blablatdinov/quranbot/view)

Функционал:
 - Каждое утро, вам будут приходить аяты из Священного Корана.
 - При нажатии на кнопку **Подкасты**, вам будут присылаться проповеди с сайта umma.ru.
 - В боте вы можете получать время намаза
 - Доступен поиск по ключевым словам

Также вы можете отправить номер суры, аята (например **4:7**) и получить: аят в оригинале, перевод на русский язык, транслитерацию и аудио

Ссылка на бота: [Quran_365_bot](https://t.me/Quran_365_bot?start=github)

Если хотите поучаствовать в разработке пишите - [telegram](https://t.me/ilaletdinov), [email](mailto:a.ilaletdinov@yandex.ru?subject=[GitHub]%20Quranbot) 

## Источники информации:

[umma.ru](https://umma.ru/)

[dumrt.ru](http://dumrt.ru/ru/)


## Prerequisites

You will need:

- `python3.10` (see `pyproject.toml` for full version)
- `postgresql` with version `13`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`


## Documentation

Full documentation is available here: [`docs/`](docs).

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [f95aa150a88969911c2489d3c67133e90e0b73c3](https://github.com/wemake-services/wemake-django-template/tree/f95aa150a88969911c2489d3c67133e90e0b73c3). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/f95aa150a88969911c2489d3c67133e90e0b73c3...master) since then.
