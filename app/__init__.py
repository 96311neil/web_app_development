from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    # 讀取環境變數中的 SECRET_KEY，開發階段使用預設值
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 註冊 Blueprints
    from app.routes.recipe import recipe_bp
    app.register_blueprint(recipe_bp)
    
    return app
