''''
this script will used in a docker environment where it will have access to a root folder and from there be able
to do a git fetch and pull and specific repos

the trigger will be from webhooks from github and should be configurable. Any commits from a repo should do a git fetch and
pull.

Doing it from here will at least ensure that if the code fails, the updating can continue on for the next commit.

it will also need to know about how to restart the specific application (which is dockerised) by using a http GET command
which means the app needs to have a small webserver interface like tornado or flask or something.
'''
import tornado.web
import tornado.ioloop
from WebHook import AbstractWebHook, WebHookInjector
import git
from git import Repo
import json
import os
import logging
from logging import info
from config import Configuration
logging.basicConfig(level=logging.INFO)

config = Configuration()
PORT = 8087


class WebHook(AbstractWebHook):

    def on_push(self, payload):
        print("on_push")

class AutoPullHook(AbstractWebHook):
    def __init__(self):
        super().__init__()

    def on_push(self, payload):
        info("Repo push hook.")
        repoInfo = json.loads(payload)
        name = str(repoInfo["repository"]["name"]).lower()
        if name in config.repos:
            try:
                path = config.repos[name].path
                if not os.path.exists(path):
                    os.mkdir(path)
                repo = git.Repo(config.repos[name].path)
                repo.git.refresh('--hard', 'origin/master')
                # g = git.Git(config.repos[name].path)
                #
                # g.pull('origin', 'master')
            except git.InvalidGitRepositoryError:
                if len(os.listdir(config.repos[name].path)) is not 0:
                    info("Repo:{} is not under git. Cannot clone before the folder is empty").format(config.repos[name].path)
                else:
                    bPath = True
                    if not os.path.exists(config.repos[name].path):
                        info("Creating path:{}".format(config.repos[name].path))
                        bPath = os.mkdir(config.repos[name].path)

                    if bPath:
                        url = repoInfo["repository"]["url"]
                        info("Cloning from url:{}".format(url))
                        Repo.clone_from(url, config.repos[name].path)
# /usr/src/app
if __name__ == '__main__':
    info("Started server on port:{}".format(PORT))
    info("version 1.0")
    app = tornado.web.Application()

    WebHookInjector.inject("/webhooks", app, AutoPullHook, u'{}'.format(config.settings.secret))
    try:
        app.listen(PORT)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        info("Exiting codeupdater")