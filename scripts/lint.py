#!.venv/bin/python
import os
from pathlib import Path
from typing import Optional

import typer
from git import Repo

CHECKED_FILES_EXTENSIONS = [
    'py',
    'md',
    'html',
]


def check_files_exists(files: list[str]):
    """Проверить есть ли файлы для линтера."""
    if not files:
        typer.echo(typer.style('No files to check', fg=typer.colors.GREEN))
        raise typer.Exit()


def find_filer_for_speller(files: list[str]) -> list[str]:
    """Ищет файлы для проверки на орфографию.

    Не проверяются файлы: тестов, миграций
    Проверяются: файлы с расширениями .py, .md, .html

    r'((^| )[^tests].*?(py|md|html))'
    """
    def _check(file: str):
        if 'tests' in file or 'migrations' in file:
            return False

        if file.endswith(tuple(CHECKED_FILES_EXTENSIONS)):
            return True

    result = list(filter(_check, files))
    check_files_exists(result)
    return result


def find_for_linter(files: list[str]) -> list[str]:
    """Найти файлы для линтера."""
    def _check(file: str):
        return file.endswith('py')

    result = list(filter(_check, files))
    check_files_exists(result)
    return result


def lint_files(finded_files: list[str]):
    """Проверить линтером файлы и отсортировать импорты."""
    finded_files = ' '.join(finded_files)
    os.system(f'isort {finded_files}')
    if os.system(f'flake8 {finded_files}'):
        raise typer.Exit(1)


def spelling_files(finded_files: list[str]):
    """Проверить на орфографию."""
    finded_files = ' '.join(finded_files)
    os.system(f'yaspeller -l ru {finded_files} --only-errors')


def print_files(show_files: bool, files: list[str]):
    """Вывести файлы в консоль."""
    if not show_files:
        return
    typer.echo(typer.style('\nFiles list:\n', fg=typer.colors.GREEN))
    files_list = ''.join([f'\t{x}\n' for x in files])
    typer.echo(files_list)


def main(
    speller: Optional[bool] = typer.Option(None, '--speller'),
    show_files: Optional[bool] = typer.Option(None, '--show-files'),
):
    """Функция выполняемая, при запуске скрипта."""
    repo = Repo(Path(__file__).resolve().parent.parent)
    files_list = repo.git.diff('master..HEAD', name_only=True).split('\n')
    if speller:
        finded_files = find_filer_for_speller(files_list)
        print_files(show_files, finded_files)
        spelling_files(finded_files)
    else:
        finded_files = find_for_linter(files_list)
        print_files(show_files, finded_files)
        lint_files(finded_files)

    typer.echo(typer.style('Success', fg=typer.colors.GREEN))
    raise typer.Exit()


if __name__ == '__main__':
    typer.run(main)
