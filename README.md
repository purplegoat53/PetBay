# PetBay
3rd Year Project

## Quickstart
At the moment, this project only depends on Python 2.7, you can get that here:
> [Python 2.7 32bit](https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi)
(its probably easier if we all stick to 32bit)

Run the installer, and make sure to select `Add python.exe to Path` on the **Customize** setup page.

After installation, in the PetBay local directory, run `main.py` by just clicking on it. This will start a server locally, accessible at `http://localhost:8080` in the browser.

The directory structure of PetBay currently is as follows:

* **static/** - contains all the css, js, images and other resources
* **views/** - contains all the template files (which are just the html files with a `.tpl` extension)
* **waitress/** - not important, part of the server
* **bottle.py**, bottle.pyc - also not important, part of the server
* **main.py** - the server script, run to start server
