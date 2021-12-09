#!.venv/bin/python
import os
from pathlib import Path
from typing import List, Optional

import typer
from git import Repo

CHECKED_FILES_EXTENSIONS = [
    'py',
    'md',
    'html',
]


def check_files_exists(files: List[str]):
    """Проверить есть ли файлы для линтера."""
    if not files:
        typer.echo(typer.style('No files to check', fg=typer.colors.GREEN))
        raise typer.Exit()


def find_filer_for_speller(files: List[str]) -> List[str]:
    """Ищет файлы для проверки на орфографию.

    Не проверяются файлы: тестов, миграций
    Проверяются: файлы с расширениями .py, .md, .html

    r'((^| )[^tests].*?(py|md|html))'
    """
    def _check(file: str):
        if 'tests' in file or 'migrations' in file or 'fixtures' in file:
            return False

        if file.endswith(tuple(CHECKED_FILES_EXTENSIONS)):
            return True

    result = list(filter(_check, files))
    check_files_exists(result)
    return result


def find_for_linter(files: List[str]) -> List[str]:
    """Найти файлы для линтера."""
    def _check(file: str):
        return file.endswith('py')

    result = list(filter(_check, files))
    check_files_exists(result)
    return result


def lint_files(changed_files_list: List[str], show_files: bool = False):
    """Проверить линтером файлы и отсортировать импорты."""
    finded_files = find_for_linter(changed_files_list)
    if show_files:
        print_files(finded_files)
    os.system('isort {}'.format(' '.join(finded_files)))
    lint_files_out = os.system(
        'flake8 {}'.format(
            ' '.join(finded_files),
        ),
    )

    if lint_files_out:
        raise typer.Exit(1)


def spelling_files(changed_files_list: List[str], show_files: bool = False):
    """Проверить на орфографию."""
    finded_files = find_filer_for_speller(changed_files_list)
    if show_files:
        print_files(finded_files)

    os.system(
        'yaspeller -l ru {}'.format(
            ' '.join(finded_files),
        ),
    )


def print_files(files: List[str]):
    """Вывести файлы в консоль."""
    typer.echo(typer.style('\nFiles list:\n', fg=typer.colors.GREEN))
    files_list = ''.join([f'\t{x}\n' for x in files])
    typer.echo(files_list)


def get_files_list(file_paths: List[str]) -> List[str]:
    """Получаем список файлов.

    Могут передаваться директории, функция составит список файлов в директориях
    """
    result = list()
    for file_path in file_paths:
        if os.path.isdir(file_path):
            for directory, _, files in os.walk(file_path):
                if directory.startswith('./.venv'):
                    continue
                result += [f'{directory}/{file_path}' for file_path in files]

        else:
            result.append(file_path)

    return result


def main(
    files: Optional[List[str]] = typer.Argument(None, help='Передайте список файлов для проверки.'),
    speller: Optional[bool] = typer.Option(
        None, '--speller', help='Укажите, если нужно проверить опечатки в документации.',
    ),
    show_files: Optional[bool] = typer.Option(
        None, '--show-files', help='Укажите, если нужно показать файлы, которые будут проверяться.',
    ),
):
    """Скрипт для проверки измененных файлов линтером."""
    if files:
        changed_files_list = get_files_list(list(files))
    else:
        repo = Repo(Path(__file__).resolve().parent.parent)
        changed_files_list = repo.git.diff('master..HEAD', name_only=True).split('\n')

    if speller:
        finded_files = find_filer_for_speller(changed_files_list)
        spelling_files(finded_files, show_files)
    else:
        finded_files = find_for_linter(changed_files_list)
        lint_files(finded_files, show_files)

    raise typer.Exit()


if __name__ == '__main__':
    typer.run(main)
