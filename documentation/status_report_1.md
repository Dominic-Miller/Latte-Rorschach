## Status Report 1

See [Our Wireframe](https://github.com/Dominic-Miller/Latte-Rorschach/blob/main/documentation/Final%20Wireframe%20Latte%20Project.PNG) for our current planning progress.

![wireframe of app](https://github.com/Dominic-Miller/Latte-Rorschach/blob/main/documentation/Final%20Wireframe%20Latte%20Project.PNG)

We've currently made a simple login page in flask which we'll be remaking with django, as well as the other pages we've wireframed:
- Login
- Account creation
- "Rorschach of the day"
- "Top Responses of the day"
  - has a scrollable area with likable comments
  - depending on the rate of our progress, we may support emoji reactions
- Nav Menu
  - we may make this a sidebar, but for the sake of simplicity, we will first implement it as a page
- Account
  - users can view their account's contributions
  - if we add other account features, they'll be here
- Historical responses
  - currently, for MVP, we think a datepicker will be the simplest to implement, with the same UI as "Rorschach of the day" below
  - however, depending on the rate of our progress, we would like to implement a scrollable grid view to select previous days

What we plan to complete by next increment:
- Swap from Flask to Django.
- Finish the user login system.
- Finish comment entry page.
- Finish interpretation viewing page (We will likely save the like system for the final increment).
- Populate database with sample values.
