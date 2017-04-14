__author__ = "Joseph Mullen"

from personal_web.personalWebsite import app

'''Code protected by if__name__ which means it will only run
immediately when this file is executed as a script,not when it is loaded as a module'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


