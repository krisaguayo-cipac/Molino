---
layout: default
title: Blog
permalink: /blog/
---

# Blog

{% for post in site.blog %}
## [{{ post.title }}]({{ post.url }})

{% if post.description %}{{ post.description }}{% endif %}

{% if post.date %}_{{ post.date | date: "%B %d, %Y" }}_{% endif %}

---
{% endfor %}
