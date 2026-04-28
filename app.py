from app import create_app
from app.models.db import init_db

app = create_app()

if __name__ == '__main__':
    # 在啟動伺服器前自動確保資料庫已經初始化建表
    init_db()
    app.run(debug=True)
