# flask-docker
Testing flask with Docker Dev env

It was copied from https://github.com/docker/awesome-compose, flask folder.

(I am not very familiar with Git. I tried to copy just that folder and i think i just forked the whole awesome-compose repor). Anyways, in this repo, i just created a new repor, copied the yaml files from the awesome-compose flask folder and i will use it to create docker dev enviromnet. Lets see how it goes.

Note1 (20-05-2023)<br/>
 I couldn't make it work for Gunicorn as shown on various online videos and tutorials. I do not want to change anything in my app.py file. I do not want to create a single main function which contians everything in app.py and pass its refernece to Gunicorn. In one tutorial, i saw a new file wsgi.py being created and it being passed to Gunicorn as wsgi:app. <br/>
It never worked in my case. In my wsgi.py, when i used <br/>
from app import app<br/>
it was just referring to app module and not the app vaiable. After playing around with lots of combinations and permutations, i got it right. So now in wsgi.py i am using the syntax<br/>
from app.app import app<br/>
This worked because 1: in wsgi.py if i put my mouse curson on app (import app), it is shown as a variable and 2: Gunicorn is working. The command used to run Gunicorn is <br/>
gunicorn --bind=0.0.0.0 --timeout 600 app.wsgi:app<br/>
EndNote<br/>