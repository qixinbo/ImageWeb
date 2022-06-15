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

## 启动（开发阶段）
如果是开发阶段，则使用如下命令：
```js
npm run serve
```

然后在浏览器中输入地址：
```html
http://localhost:8080/
```

## 启动（生产阶段）
开发结束后，使用如下命令对前端代码进行打包压缩：
```js
npm run build
```
该命令会生成`dist`文件夹，里面放置了前端所需的`html`、`css`、`js`文件及图片等静态文件。
**得到该文件夹后，后续就无需再使用`nodejs`及`npm install`这一步。**
对于这些页面，需要启动一个服务器来托管它们。
简单地，可以使用python内置的一个测试服务器来查看效果。可以查看该[教程](https://developer.mozilla.org/zh-CN/docs/Learn/Common_questions/set_up_a_local_testing_server)。
进入`dist`文件夹，然后：
```python
python -m http.server 8081
```
或者更专业地，使用`nginx`反向代理服务器，可以查看该[教程](https://www.cnblogs.com/taiyonghai/p/9402734.html)。
对`nginx`配置文件修改`listen`端口号（假设为`8081`）和`location`（即`dist`文件夹所在位置）后，启动服务：
```js
start nginx
```
然后在浏览器中输入地址：
```html
http://localhost:8081/
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
