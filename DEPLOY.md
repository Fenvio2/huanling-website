# Render 后端部署配置

## 一、在 Render.com 免费部署后端

### 步骤 1：注册 Render 账号
访问 https://render.com ，用 GitHub 账号登录。

### 步骤 2：创建 Web Service
1. 点击 **New +** → **Web Service**
2. 选择仓库 `Fenvio2/huanling-website`
3. 配置：
   - **Name**: `huanling-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Free Plan**: 选 Free
4. 点击 **Deploy Web Service**

### 步骤 3：获取后端地址
部署完成后，Render 会给你一个地址，类似：
```
https://huanling-api.onrender.com
```

### 步骤 4：更新前端 API 地址
在前端所有页面的 `API_BASE` 变量中，将生产环境地址替换为你的 Render 地址：

```javascript
var API_BASE = (function() {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:5000';
  }
  return 'https://huanling-api.onrender.com';  // 替换为你的 Render 地址
})();
```

---

## 二、GitHub Pages 静态前端（已完成）

前端地址：https://fenvio2.github.io/huanling-website/

---

## 三、Render 免费版注意

- 免费版 15 分钟无访问会自动休眠
- 首次访问需要 30-60 秒唤醒
- 每月 750 小时免费运行时间
