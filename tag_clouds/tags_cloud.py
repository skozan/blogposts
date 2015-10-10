#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vi:expandtab:tabstop=4 shiftwidth=4 textwidth=79

import math

TAG_CLOUD_CSS_CLASSES = 3
"""
Let's have three separate css classes for our example
"""

TAG_CLOUD_CSS_CLASS_TEMPLATE = '.tag-cloud-%d'
"""
This can be a css template, with ".tags-cloud-1" for the less used tag and
".tags-cloud-3" for the most used tag (assuming 3 distinct classes)
"""

def get_tags_cloud(data):
    """
    data should be a list containing tags items. Each item should be a
    dictionary containing at least the `name` of the tag and the number of tag
    occurrences named as `usage`.

    Returns a list sorted by `name` plus two fields: a `css_class` and the
    linear value resulting from logarithmic interpolation.
    """
    if not data:
        return

    # Find the maximum and minimum usage
    maximum = max(data, key=lambda x: x['usage'])['usage']
    minimum = min(data, key=lambda x: x['usage'])['usage']

    # Do the math, find the common subtractor and divider and calculate log
    # value for each tag. Then, assuming that log value is linearized, find the
    # integer class from 1 to TAGS_CLOUD_CSS_CLASSES
    subtractor = math.log(float(minimum))
    divider = math.log(float(maximum)) - subtractor or 1.0 # 1.0 if min==max
    for item in data:
        log_value = (math.log(float(item['usage']))-subtractor) / divider
        d = int(round(log_value*(TAG_CLOUD_CSS_CLASSES-1) + 1))
        item['css_class'] = TAG_CLOUD_CSS_CLASS_TEMPLATE%d
        item['log_value'] = log_value

    # Sort results by name for displaying tags in an alphabetical order
    return sorted(data, key=lambda x: x['name'])


# An example

if __name__ == '__main__':
    import pprint

    TEST_SET = [
            {'name': 'popular tag', 'usage': 100},
            {'name': 'medium popularity tag', 'usage': 10},
            {'name': 'another medium popularity tag', 'usage': 15},
            {'name': 'obscure tag', 'usage': 2}
        ]

    pprint.pprint(get_tags_cloud(TEST_SET))



# This is a potential Django application of the tag cloud. Django code is
# untested, it is just to prove the concept. Let's assume two models, first
# model represents blog posts and second models tags being used in posts.
# 
# from django.db import models
# from django.db.models import Count
# 
# class BlogPost(models.Model):
# 
#     # Several blog fields defined here...
#     #
# 
#     tags = models.ManyToManyField("Tag", related_name='blog_posts')
# 
# 
# class Tag(models.Model):
# 
#     name = models.CharField(max_length=40)
# 
#     @staticmethod
#     def tags_cloud_data(limit=50):
#         data = (Tag.objects.
#                 values('name').
#                 annotate(usage=Count('blog_bosts')).
#                 order_by('-usage')[:limit])
#         data = [item for item in data if item['usage']]
#         return data
# 
#     @staticmethod
#     def tags_cloud(limit=50):
#         return get_tags_cloud(Tag.tags_cloud_data(limit))



