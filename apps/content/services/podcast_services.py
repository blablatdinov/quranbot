from apps.content.models import Podcast


def get_random_podcast():
    random_podcast_queryset = Podcast.objects.order_by("?")[0:1]
    return random_podcast_queryset
