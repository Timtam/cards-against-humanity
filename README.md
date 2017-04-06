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
Server and client are written in Python 2 and depend on multiple packages, which need to be installed before running the game. You can use the following command to do so while you're in the project directory:
pip install -r requirements.txt
