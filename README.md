# UIUC Sports Analytics Society Project

- Source code for our sports prediction web app
- View the project at [URL]

### Git Setup:
---
 `git clone [url]` *Reach out if you don't know how to find the URL*

 `cd uiuc_sas/frontend`

 `npm install`

### Git Workflow:
---
`git switch main`

`git pull origin main`

`git switch -c [branch name]`

`git branch` *You should see an asterisk next to your new branch name*

*Make your changes*

`git add .`

`git commit -m "Commit message here"`

`git push origin [branch name]`

*Then we review the changes that were made, and merge the branches*

### Frontend Setup:
---
- React (https://react.dev/)

`npm install` 
- Only needs to be run once, to install your React dependencies
`npm run dev`
- Hosts the project on `localhost:5173`

### Backend Setup:
---
- NoSQL style database hosted on Amazon DynamoDB
- Flask for setting up an API (https://flask.palletsprojects.com/en/stable/)

`python3 app.py` *Make sure you are in backend directory*
- Runs backend on the URL found in console
- Note that different URL extensions result in different data shown