class ContentTooLong(Exception):

    def __str__(self):
        return 'max len of content should be less than 4096 symbols'

