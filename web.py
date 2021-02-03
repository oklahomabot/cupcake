import random, string
from flask import Flask, render_template, request
from threading import Thread
import datetime
'''
app = Flask('')

@app.route('/')
def home():
    now = datetime.datetime.now()
    return (f'webserver accessed @ {now.strftime("%H:%M %m/%d/%Y")}')
'''





app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

@app.route('/')  # What happens when the user visits the site
def base_page(message = 'Just Started'):

	random_num = random.randint(1, 100000)  # Sets the random number
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
		random_number=random_num,  # Sets the variable random_number in the template
	  last_command = message)


def run():
  app.run(host='0.0.0.0',port=8080)

def start_web(message = 'Just Started'):
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=8080)  # Randomly select the port the machine hosts on.





'''
import random, string
from flask import Flask, render_template, request

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits





@app.route('/2')
def page_2():
	rand_ammnt = random.randint(10, 100)
	random_str = ''.join(random.choice(ok_chars) for a in range(rand_ammnt))
	return render_template('site_2.html', random_str=random_str)


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
'''