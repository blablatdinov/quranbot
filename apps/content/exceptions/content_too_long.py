class ContentTooLong(Exception):
    """Исключение вызывается если утренний контент получается слишком длинным."""

    def __str__(self):
        """Строковое представление."""
        return 'max len of content should be less than 4096 symbols'
