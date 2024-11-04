---
layout: blog
group: blog
title: Blog
description: Here you’ll find the latest insights, strategies, and tips from our consulting team.
page_heading: Our blog posts 
empty: coming soon
resent: Resent posts
permalink: /blog/
lang: en
weight: 3
---

# Blog 
<h2>{{posts.size}}</h2>

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