# SkillBridge & CareerForge - Project Architecture and File Structure

This document provides a comprehensive overview of the `SkillBridge_careerForge` project, detailing its architecture, Django apps, templates, and key files.

## High-Level Architecture
The project is built using Django (Python) for the backend and HTML/CSS/JS (with Bootstrap 5) for the frontend. It follows a modular architecture divided into multiple specialized Django apps to separate concerns, making it easier to maintain and scale. It uses an SQLite database (`db.sqlite3`) for local development.

## Root Directory Structure
The root directory `k:\AI-DJANGO-FULL-STACK\SkillBridge_careerForge` contains the following key components:

- **`apps/`**: Contains all the functional Django applications (modules) that make up the platform.
- **`skillbridge_careerforge_project/`**: The main Django project configuration directory containing core settings, base URLs, ASGI/WSGI configurations, and global templates.
- **`manage.py`**: The Django command-line utility for administrative tasks.
- **`requirements.txt`**: Lists all Python dependencies required for the project.
- **`db.sqlite3`**: The local SQLite database file.
- **Documentation Markdown Files**:
  - `AI_PROFILING_GUIDE.md`: Guide specifically for the AI Profiling feature.
  - `DASHBOARD_INTEGRATION_GUIDE.md`: Guide detailing how features integrate into the main dashboard.
  - `INTEGRATION_VISUAL_GUIDE.md`: Visual representations (ASCII/Mermaid) of data flows and integrations.
  - `QUICK_REFERENCE.md`: Quick reference commands and shortcuts.

## Modular Django Apps (`apps/`)
The system's backend logic is distributed across 11 integrated Django apps:

1. **`accounts`**: Manages user authentication, registration, profiles, and custom user models (`accounts.User`).
2. **`core`**: Contains the main landing pages, centralized dashboards, and base site navigation logic.
3. **`skills`**: The central repository for the "AI Skill Profiling" feature. Handles skill extraction, master taxonomy, proficiency estimation, and the unified profile page backend.
4. **`jobs`**: Manages the "Smart Internship Provider" and job matching algorithms, connecting users to opportunities based on their skill profiles.
5. **`learning`**: Handles the "Personalized Roadmap" feature, offering step-by-step learning paths.
6. **`assessments`**: Contains the "Technical Assessment Engine" for role-specific MCQs and testing.
7. **`interviews`**: Powers the "AI Mock Interview System," driving technical and behavioral interview simulations.
8. **`resumes`**: Manages the "Smart Resume Builder," generating ATS-friendly resumes.
9. **`certifications`**: Handles the "Certification Recommendations" feature.
10. **`progress`**: Manages user analytics, progress tracking, and career insights.
11. **`api`**: A dedicated app for handling REST Framework (DRF) configurations and exposing API endpoints for potential external integrations or decoupled frontend work.

## Project Configuration (`skillbridge_careerforge_project/`)
The main project wrapper:
- **`settings.py`**: Configures all installed apps, database (`sqlite3`), static/media files, authentication backends, and Django Rest Framework mappings. Features modular configurations using `decouple.config` for environment variables.
- **`urls.py`**: The root URL router that connects incoming web requests to the specific endpoints defined within the individual apps.
- **`templates/`**: Global templates directory.
  - `templates/base.html`: The base HTML wrapper and layout for the application.
  - `templates/core/home.html`: The global landing page (pre-login).
  - `templates/core/index.html`: The alternative index or secondary landing page.
  - `templates/core/dashboard.html`: The central user dashboard (`/dashboard/`) containing the sidebar, widgets, tab integrations, and AJAX loading functionality.
  - `templates/core/profilepage.html`: The unified "AI Profiling" interface, integrating user identity, education, projects, skills, and NLP extraction status.

## Frontend Interaction Flow
The application heavily utilizes dynamic frontend rendering powered by AJAX to provide a Single-Page Application (SPA) feel, especially within the user dashboard.

**Example Flow (AI Profile Loading):**
1. User clicks the "Build AI Profile" button in `dashboard.html`.
2. A JavaScript AJAX fetch request calls the `/skills/profile/` endpoint.
3. The server's `skills.views.profile_page` view intercepts the request, returning the HTML structure of `profilepage.html`.
4. The frontend intercepts the HTML, injects it into a designated dashboard container (`profilingContainer`), and smoothly transitions the user without a hard page reload.

## Summary of Recent Development
Recent changes have successfully merged the legacy AI Profile components into a singular, unified `profilepage.html`. The dashboard layout, Javascript routing methods, and Django URLs have been refactored (from `ai_profiling_ajax` to `profile`) to support this new, cohesive approach.
