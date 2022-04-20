from os import name
from flask import Blueprint, redirect, render_template, url_for

from app.authentication.helpers.forms import LoginForm

blueprint = Blueprint('simple_pages', __name__)

@blueprint.route('/')
def index():
    return redirect(url_for('authentication.login'))
    
