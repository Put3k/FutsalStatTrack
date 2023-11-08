
# Futsal Stat Track

**TL;DR**: A Django web application created for quick and easy input and storage of weekly statistics for mini futsal tournaments played among friends.

The application was initially created with the idea of storing statistics within one 'league,' but with the desire for self-improvement and a thirst for knowledge, I expanded the capability to store statistics for multiple leagues.

After registering (I have not yet implemented email confirmation), the user has the option to create their own league or join an existing league to which they have been invited. The league owner can create Match Days, during which 3 teams participate in the matches. When creating a Match Day, the owner assigns players to each team. They can use previously created players or add new ones. In order for their friends to view the league and its statistics, the owner must invite them using a one-time link. After creating a Match Day, the owner gains the ability to add individual matches and assign goals scored by players. Users have access to view team and individual player statistics on Match Day, display statistics for a specific player, and display statistics for all players in the league.
## Features

- Storing players statistics;
- Access to statistics summary per league, matchday, player;
- Creating and managing multiple leagues;
- Invitation system;
- Generating PDF report files;
- Storing reports on GCS;



## Known Issues Iam working on

- In league home view, the summary of top 5 players statistics is summarized in context of all leagues that player participate in;
- Statistics summary is calculated dynamicly each time user makes a request;
- In matchday create view after user assigned players to teams and adds new player to league, all teams forms resets;

These are the problems I encountered while using the app with my friends. If you have encountered any problems or have any suggestions, I would appreciate it if you would send me your comments to the following e-mail address: kwiniarczyk99@gmail.com




## Planned Features

- Email confirmation during the registration process
- Make an accessible REST API
- Link Discord to manage app through API
## Run Locally

Clone the project

```bash
  git clone https://github.com/Put3k/FutsalStatTrack.git
```

Go to the project directory

```bash
  cd FutsalStatTrack
```

Create .env file and paste in following:
```
DJANGO_DEBUG=True
DJANGO_SECRET_KEY='not_a_secret_key'

DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
```

Run docker-compose

```bash
  docker-compose up --build
```

Django superuser credentials:
- Username: ```admin```
- Email: ```admin@email.com```
- Password: ```testpass123```

Superuser credentials will raise an exception if used elsewhere than in the admin panel due to lack of player assigned to it.

Use register button to create new user to access web app.

**Google Cloud Storage** is unavailable in local environment because I do not provide you GCS credentials.