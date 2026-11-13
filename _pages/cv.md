---
layout: cv
permalink: /cv/
title: CV
nav: true
nav_order: 3
cv_pdf: /assets/pdf/Yoontae_Cho_CV.pdf
cv_format: rendercv
---

<style>
  /* The theme's Tailwind build has no list reset for .list-group, so every entry got a stray bullet. */
  .cv ul.list-group {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .cv .list-group-item {
    padding: 0.9rem 0;
  }

  /* Rows rendered by _includes/cv/figure_entry.liquid */
  .cv .cv-figure img {
    display: block;
    width: 100%;
    max-width: 180px;
    height: auto;
  }
  .cv .cv-logo img {
    max-width: 84px;
    padding: 4px;
    border-radius: 50%;
    background: #fff;
  }
  @media (min-width: 576px) {
    .cv .cv-logo img {
      margin: 0 auto;
    }
  }
  .cv .cv-line {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;
  }
  .cv .cv-line h6 {
    margin: 0 0 0.35rem;
  }
  .cv .cv-subtitle {
    font-size: 0.95rem;
  }
  .cv .cv-side {
    flex-shrink: 0;
    font-size: 0.9rem;
    color: var(--global-text-color-light);
  }
</style>
