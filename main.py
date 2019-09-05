''''
this script will used in a docker environment where it will have access to a root folder and from there be able
to do a git fetch and pull and specific repos

the trigger will be from webhooks from github and should be configurable. Any commits from a repo should do a git fetch and
pull.

Doing it from here will at least ensure that if the code fails, the updating can continue on for the next commit.

it will also need to know about how to restart the specific application (which is dockerised) by using a http GET command
which means the app needs to have a small webserver interface like tornado or flask or something.
'''
