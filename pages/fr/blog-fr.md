---
layout: base
title: Blogue
permalink: /blog/
lang: fr
weight: 3
---

# Blogue

Ici, vous trouverez les dernières perspectives, stratégies et conseils de notre équipe de consultants.

<ul>
  {% assign filtered_posts = site.posts | where: "lang", page.lang %}
  {% for post in filtered_posts %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <span>{{ post.date | date: "%b %d, %Y" }}</span>
      </li>
  {% endfor %}
</ul>