# 介绍
<!-- ImageWeb是一个旨在将桌面端的图像处理软件[ImagePy](https://github.com/Image-Py/imagepy)迁移到web上的项目，使得用户无需配置复杂的环境、仅需一个浏览器即可进行复杂的图像处理操作。
如下是硬币分割的一个案例录像： -->
![mov](docs/imageweb_small.gif)
# 启动后端
进入`backend`文件夹：
```python
uvicorn main:app --port 5000
```

# 启动前端
进入`frontend`文件夹：
```js
cd frontend
```
## 安装依赖
```js
npm install
```

## 启动
```js
npm run serve
```

# 登录页面
浏览器中输入：
```html
http://localhost:8080/
```
<!-- # 启动主程序
进入`app`文件夹：
```python
python -m http.server 7788
``` -->
<!-- # 登录页面
浏览器中输入：
```html
http://0.0.0.0:7788
```
 -->
