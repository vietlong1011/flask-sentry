#Chạy ứng dụng
#!/usr/bin/env python3
#!/flask/py3.10.12/bin python3
from app import app

if __name__ == "__main__":
  app.run(host='172.21.21.12', port=5000, debug=True)