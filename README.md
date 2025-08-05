# ProManager

A Django-based project management tool with a visual editor for adding, resizing, moving, and deleting text and image elements to a project editor.

## Features
- User authentication (sign up, login, logout)
- Create, view, edit and delete projects
- Visual editor for each project:
  - Add text elements
  - Upload and add images
  - Drag and resize elements within the editor
  - Delete individual elements (removes associated files for images)
- Delete a project (removes all associated elements and their files)
- Inline editing of project title

## Requirements
- Python 3.8+
- Django 4.x or 5.x
- SQLite

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tanajoji/promanager.git
   cd promanager
   ```
2. Install dependencies:
   ```bash
   pip install django
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Project
```bash
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- Sign up and log in.
- Create a new project.
- Click 'Open Editor' to open a project's visual editor.
- Add text or upload images/SVGs.
- Drag and resize elements on the canvas.
- Click the delete icon on an element to remove it.
- Click the project title to edit it inline.
- Delete a project to remove all its elements and associated files.

## Notes
- When deleting an element or project, associated image/SVG files are also deleted.
- The editor uses jQuery for drag, resize, and AJAX operations.
- Text elements scale their font size proportionally as you resize them.
