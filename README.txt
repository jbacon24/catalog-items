To run this final project

# Clone
1. `git clone https://github.com/jbacon24/catalog-items.git` into terminal

# Vagrant
1. Open terminal
2. Run `vagrant up` in terminal
3. Run `vagrant ssh` in terminal
4. Next `cd /vagrant`

# Inside the vagrant environment
1. `cd catalog-items`
2. run `python database_setup.py` to create the database
3. run `python alltheitems.py` to populate the database
4. run `python finalflask.py` and navigate to localhost:5000 in your browser
