from typing import Dict

from django import template

from imagesApp.models import ImageStatistic, ImageWithContent

register = template.Library()


@register.inclusion_tag('inc/_userStatistic.html')
def get_user_stats(user_id: str) -> Dict[str, Dict[str, int]]:
    query = ImageWithContent.objects.filter(publisher__pk=user_id).select_related('statistic')
    images_count = query.count()
    views_on_images = 0
    all_likes = 0
    all_dislikes = 0
    
    for query_object in query:
        views_on_images += query_object.statistic.views
        all_likes += query_object.statistic.likes
        all_dislikes += query_object.statistic.dislikes
        
    return {'stats' : {"Количество загруженных фото": images_count, 
                       "Количество просмотров на фото": views_on_images,
                       "Количество лайков на фото": all_likes,
                       "Количество дизлайков на фото": all_dislikes}}