---
layout: base
title: Blog
permalink: /blog/
lang: en
weight: 3
---

# Blog

Here you’ll find the latest insights, strategies, and tips from our consulting team.

<ul>
  {% assign filtered_posts = site.posts | where: "lang", page.lang %}
  {% for post in filtered_posts %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <span>{{ post.date | date: "%b %d, %Y" }}</span>
      </li>
  {% endfor %}
</ul>