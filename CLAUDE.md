# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static, single-page educational cybersecurity awareness website in Portuguese for AEMS (Associação Educacional Magsul). No build system, package manager, or frameworks — pure HTML/CSS/JavaScript deployed via GitHub Pages.

## Running Locally

Open `index.html` directly in a browser, or use any static file server:

```bash
# Python
python3 -m http.server 8000

# Node (if available)
npx serve .
```

There are no build, lint, or test commands.

## Architecture

Three files make up the entire app:

- **[index.html](index.html)** — Full single-page structure with all content sections: hero popup, introduction, real news cases (Casos Reais), scam types (Tipos de Golpes), prevention tips, reporting guide, team section, and rating form.
- **[style.css](style.css)** — Dark cybersecurity aesthetic with red/black/cyan palette, glassmorphism effects (`backdrop-filter`), and responsive breakpoint at 900px.
- **[script.js](script.js)** — All interactivity: typewriter animation, hero popup, card tilt effect on mousemove, scroll-triggered fade-in animations, star rating system, and dynamic team member rendering.

## Key Patterns

**Team data** is defined as a JavaScript array near line 96 in [script.js](script.js). Each member has `nome`, `github`, and `img` fields. The `img` field is a local path under `images/`; if the image fails to load, a GitHub avatar URL is used as fallback.

**Star rating** submits to a Google Forms endpoint via `fetch` with `mode: 'no-cors'`. The form entry ID is `entry.971847553`. No response handling is needed since no-cors returns an opaque response.

**Scroll animations** use `IntersectionObserver`-style manual scroll events — elements get `opacity` and `transform` applied directly on scroll.

**Card tilt** uses `mousemove`/`mouseleave` on `.news-card`, `.tip-card`, and `.prevention-card` elements to apply 3D `rotateX`/`rotateY` transforms.

## Deployment

The site is hosted on GitHub Pages from the `main` branch. Push to `main` to deploy. The current working branch is `feature/security-form`.
