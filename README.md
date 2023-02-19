# Scoreboard Bot (WIP)
This is a private development build. Don't deploy to any real servers without first changing the bot's scope and intents.

## Setup
CMD sucks. Use Git Bash to run the following:<br>
Or do it manually I guess.

Run the following in the **GIT BASH** terminal (while in the project folder):<br>
&emsp;`sh sh/venv.py` -> if you want a virtual environment (optional, but recommended)<br>
&emsp;`sh sh/init.py` -> to get the dependencies.

To activate the venv: `. ./env/Scripts/activate`

if you're using the "run code" button, **make sure you run the activate script in the terminal it opens**<br>
You'll know you aren't in the venv if you cant see the "(venv)"

Note: you won't be able to use venv with CMD.

We now require the Google API. In order to test the app, I (Adsu) will need to **add you as a test user on the API page**, otherwise it won't work.<br>
Assuming you're already a test user, you'll be prompted to consent to the scopes of the project on the first time run.<br>
This will generate a `token.json` file. Provided you have that file, you should be fine to continue as normal.
<br><br>
To begin the app, run:

`python src`

## Roadmap

### Major
- Add fancy visuals
- Actually show the correct data
- Add command to show unspent points
- Add a name dropdown (with a filter if possible)
  - could check if the users discord username matches a record in the db?

### Minor
- Allow Chasers to lookup their original usernames instead of their chaser titles
