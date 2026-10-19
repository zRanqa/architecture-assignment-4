from flask import Flask, jsonify
from app.blueprints.farm import farm_bp
from app.blueprints.task import task_bp
from app.errors import NotFoundError, ValidationError, ForbiddenError

def create_app():
    app = Flask(__name__)
    app.register_blueprint(farm_bp)
    app.register_blueprint(task_bp)


    @app.errorhandler(ValidationError)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 400

    
    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    
    @app.errorhandler(ForbiddenError)
    def handle_forbidden(e):
        return jsonify({"error": str(e)}), 403
    
    return app