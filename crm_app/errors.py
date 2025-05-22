from flask import render_template

def register_error_handlers(app):
    """Register error handlers with the Flask application"""
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403
    
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400