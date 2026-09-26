---
layout: default
title: Projects
permalink: /projects/
---

# Projects

{% for project in site.projects %}
## [{{ project.title }}]({{ project.url }})

{{ project.description }}

{% if project.status %}_Status: {{ project.status }}_{% endif %}

---
{% endfor %}
