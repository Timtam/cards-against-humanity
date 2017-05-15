from pygame import USEREVENT

# EVENT_VIEWCHANGE needs to have keyword argument 'view'
# 'view' needs to be the name of the view to be set
EVENT_VIEWCHANGE = USEREVENT + 1
# this event will cause the function 'function' to be called with the unpacked
# arguments from argument args and
# keyword arguments from 'kwargs' argument
EVENT_FUNCALL = USEREVENT + 2
