from flask import Blueprint, render_template

blueprint = Blueprint(
    'client',
    __name__,
    url_prefix='',
    static_url_path='static',
    static_folder='static',
    template_folder='templates',
)


@blueprint.route('/')
def index():
    return render_template('index.html')
