# Latte-Rorschach

### Description
Latte Rorschach is a web page where visitors are presented with an image of latte art for that day. Users can then type an interpretation of the latte and upon submission, they are presented with other users’ comments and can upvote, downvote, or reply to their interpretations. Optionally, they can create an account to track their contributions. There will also be a gallery of all past daily lattes and their top interpretations. When a user gets a top comment of the day, they receive a bonus upvote they can use on future lattes. Admins can remove inappropriate comments and modify user status.


### Team Members
**Ethan Flot**: epf19@fsu.edu
**Dominic Miller**: dgm21@fsu.edu
**Aaron Garman**: aag15b@fsu.edu
**Chelsea Mensah**: Ckm20a@fsu.edu
**Alec Tremblay**: abt20c@fsu.edu


### Workload Split
#### Backend:
 - Django Server (web backend and auth): Alec, Dominic, Aaron, Chelsea, Ethan
 - SQL Database: Ethan, Aaron
 - Latte CDN: Ethan, Dominic

#### Frontend:
 - React: Chelsea, Alec
 - HTML/CSS: Alec, Aaron


### Requirement Fulfillment
#### Information Management
SQL Database that contains:
 - Per latte
    - Pointer to the image of the latte in the CDN
    - Interpretations, their votes
 - Per user (if logged in)
    - Name
    - Login hash
CDN that contains:
 - Latte images
Role Based Access Control
 - Standard users:
    - Don't need to log in, but can
 - Admins:
    - Can upload lattes
    - Moderate comments

#### Secure Computing
 - Log in with a password

#### Parallel or Distributed Computing
 - Users can submit interpretations and run local react frontend
