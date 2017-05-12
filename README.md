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
Server and client are written in Python 2 and depend on multiple packages, which need to be installed before running the game. All required packages are annotated inside the requirements.txt file, which can be run through pip to install all requirements.
```
pip install -r requirements.txt
```
The only thing which is left now is to install wxPython. For Windows it might be the best idea to download the binary package from [the wxPython download page](https://wxpython.org/download.php).
For other operating systems, please follow the official [wxPython installation notes](https://wiki.wxpython.org/How%20to%20install%20wxPython).
# accessibility notes
## Screen Reader support
We provide accessibility by supporting several screen readers, including the following:
* JAWS
* NVDA
* Speechd (Linux)
* Supernova
* System Access
* Virgo
* VoiceOver (OS X)
* Window Eyes

Of course we'll try to support as many platforms as possible, so if you encounter any accessibility problems with any platform/screen reader, don't hesitate to contact us, or at least open an issue.

## Keystrokes
Keep in mind that the accessibility features are only enabled if using the client-accessible launcher. If only using the client launcher, the accessibility features will be disabled. That's just to prevent sighted people into stumbling into a world of stuttering speech which would disgust them that much that they'll throw this game away immediately.
When using the client-accessible launcher, you'll immediately hear some stuff. Remember to navigate using the tab key, using helpers like JAWS cursor or object navigator in NVDA won't help you here. All controls will tell you their name and their function immediately. Of course you can type text into input fields and press buttons by using the return key. Input fields can be navigated using the cursor keys and als the home and end keys as usual. When placing text into input fields, you'll hear the typed letters immediately. To make it easier to listen to the whole input again without using tab and shift+tab to navigate back into this window, you can just press the left ctrl key to repeat the current control. This will of course work on all controls, not just the input fields. If you want some key stroke added to improve the accessibility, just write us or open an issue.