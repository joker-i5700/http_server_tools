# -*- coding: utf-8 -*-
"""
!/usr/bin/python3
@CreateDate   : 2019-06-24
@Author      : jet
@Filename : app.py
@Software : pycharm

The app module, containing the app factory function.
"""
import logging
import sys

from flask import Flask, render_template
from flask_restful import Api

from flask_server_user.api import TodoList, Todo, TaskList
from flask_server_user import commands, public, user
from flask_server_user.extensions import (
    bcrypt,
    cache,
    csrf_protect,  # 防跨站脚本攻击扩展功能
    db,
    debug_toolbar,  # 激活flask debug tool bar功能
    login_manager,
    migrate,
    # webpack,
)


def create_app(config_object="flask_server_user.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    api_demo(app)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app


def api_demo(app):
    """create restful api"""
    api = Api(app)
    ##
    # Actually setup the Api resource routing here
    ##
    api.add_resource(TodoList, '/todos')
    api.add_resource(Todo, '/todos/<todo_id>')
    api.add_resource(TaskList, '/tasks')

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)

def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)    # 对外发布前，注释掉此段代码，则不显示主页的flask debug右则信息
    migrate.init_app(app, db)
    # webpack.init_app(app)
    return None
