# cards-against-humanity
An open-source implementation of the popular Cards Against Humanity game.
If you don't know what this actually is, look at the corresponding [website](https://cardsagainsthumanity.com/).
# Development
Development of this project will occur during the summer semester 2017 by students of the Anhalt University of Applied Sciences.
We aim to provide the following features:
* packaging support to make it possible to run server and/or client even without any further installations (possibly with cx_Freeze)
* accessibility improvements so blind and visually impaired players can play this game too
* one database per server support, meaning that different servers can provide different card databases
* database editing utility so users can edit their database to add new and unique cards (black as well as white ones)
* multi-platform support (Windows Linux, OS X, maybe mobile devices like Android too)
# Dependencies
Server and client are written in Python 2 and depend on multiple packages, which need to be installed before running the game. All required packages are annotated inside the requirements.txt file, which can be run through pip to install all requirements. Since pip itself requires some packages before it's able to execute the package installation successfully, you'll need to execute the following commands in the right order to setup the development environment properly:
```
pip install Mercurial
pip install -r requirements.txt
```
The only thing which is left now is to install wxPython. For Windows it might be the best idea to download the binary package from [the wxPython download page](https://wxpython.org/download.php).
For other operating systems, try installing it via pip:
```
pip install wx
```
If this doesn't help, please consider looking into the [wxPython installation notes](https://wiki.wxpython.org/How%20to%20install%20wxPython).