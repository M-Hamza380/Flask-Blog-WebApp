import os, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[ [%(asctime)s] : %(name)s : %(levelname)s : %(module)s : %(message)s ]")

Project_Name = "flaskblog"

list_of_files = [
    f"src/{Project_Name}/errors/__init__.py",
    f"src/{Project_Name}/errors/handlers.py",
    f"src/{Project_Name}/main/__init__.py",
    f"src/{Project_Name}/main/routes.py",
    f"src/{Project_Name}/posts/__init__.py",
    f"src/{Project_Name}/posts/forms.py",
    f"src/{Project_Name}/posts/routes.py",
    f"src/{Project_Name}/static/main.css",
    f"src/{Project_Name}/templates/error/404.html",
    f"src/{Project_Name}/templates/about.html",
    f"src/{Project_Name}/templates/account.html",
    f"src/{Project_Name}/templates/create_post.html",
    f"src/{Project_Name}/templates/home.html",
    f"src/{Project_Name}/templates/layout.html",
    f"src/{Project_Name}/templates/login.html",
    f"src/{Project_Name}/templates/post.html",
    f"src/{Project_Name}/templates/register.html",
    f"src/{Project_Name}/templates/reset_request.html",
    f"src/{Project_Name}/templates/reset_token.html",
    f"src/{Project_Name}/templates/users_posts.html",
    f"src/{Project_Name}/sql-alchemy",
    f"src/{Project_Name}/users/forms.py",
    f"src/{Project_Name}/users/routes.py",
    f"src/{Project_Name}/users/utils.py",
    f"src/{Project_Name}/utils/__init__.py",
    f"src/{Project_Name}/__init__.py",
    f"src/{Project_Name}/config.py",
    f"src/{Project_Name}/models.py",
    "main.py",
    "requirements.txt"
]

for filepath in list_of_files:
    file_path = Path(filepath)

    file_dir, file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for the file: {file_name}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
            logging.info(f"Creating empty file: {file_path}")
    else:
        logging.info(f"{file_name} is already exists.")
