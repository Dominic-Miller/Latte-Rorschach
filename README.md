# Latte-Rorschach

## Description
Latte Rorschach is a web page where visitors are presented with an image of latte art for that day. Users can then type an interpretation of the latte and upon submission, they are presented with other users’ comments and can upvote, downvote, or reply to their interpretations. Optionally, they can create an account to track their contributions. There will also be a gallery of all past daily lattes and their top interpretations. When a user gets a top comment of the day, they receive a bonus upvote they can use on future lattes. Admins can remove inappropriate comments and modify user status.


## User Manual
### Compilation & Execution
First navigate to the Latte-Rorschach folder:
```bash
cd Latte-Rorschach
```
Next activate the virtual environment:
```bash
venv\Scripts\activate
```
Then navigate to the latterorschach folder:
```bash
cd latterorschach
```
Now run the program locally with your python interpreter, for example:
```bash
python manage.py runserver
```
Navigate to the IP:port given in the output in your web browser. The default is `localhost:8000/`.

## Libraries & Resources
### Main Resources
 - Django
 - Python3
    - datetime
    - random
    - uuid



## Separation of Work
### Backend:
 - Django Server:
    - Alec, Dominic, Aaron, Chelsea, Ethan
 - Data Models and Database Operations:
    - Ethan, Aaron, Alec, Chelsea, Dominic

### Frontend:
 - HTML/CSS:
    - Alec, Aaron, Dominic, Chelsea, Ethan
 - User Content:
    - pokemon_guy99

### Requirements Satisfaction:
- Information Management(RBAC):
    - Django User System, Login/Logout functionailty with roles:
         - Guest
         - Standard User
         - Admin
- Secure Computing:
    - Django Password Encryption and User system 😴
- Distributed Computing:
    - Django is a web framework, so this app is capable of being deployed to a web server for distributed user interaction with one database
