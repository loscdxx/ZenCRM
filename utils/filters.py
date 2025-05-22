from markupsafe import Markup
import re

def nl2br(value):
    """Convert newlines to <br> tags."""
    if not value:
        return ""
    return Markup(re.sub(r'\r\n|\r|\n', '<br>', value))

def register_filters(app):
    """Register custom Jinja2 filters."""
    app.jinja_env.filters['nl2br'] = nl2br