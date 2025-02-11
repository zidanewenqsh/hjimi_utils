# PyPI 配置指南

## .pypirc 文件说明

.pypirc 是一个用于存储 PyPI 仓库配置信息的文件，它通常位于用户的主目录下（例如：~/.pypirc 或 %HOME%/.pypirc）。这个文件包含了上传 Python 包时所需的认证信息和仓库配置。

## 配置文件位置

- Linux/Mac: `~/.pypirc`
- Windows: `C:\Users\YourUsername\.pypirc`

## 配置内容说明

配置文件主要包含以下几个部分：

1. **[distutils] 部分**
   - 用于指定默认的包索引服务器
   - 可以设置 index-servers 来列出可用的服务器

2. **[pypi] 部分**
   - 用于配置官方 PyPI 仓库
   - 包含用户名和密码信息
   - 建议使用 API token 而不是密码

3. **[testpypi] 部分**
   - 用于配置测试版 PyPI 仓库
   - 用于测试包的上传
   - 同样支持 token 认证

4. **[server-login] 部分**
   - 可以配置其他自定义的包索引服务器
   - 每个服务器需要单独的认证信息

## 安全建议

1. 文件权限设置为仅当前用户可读写（chmod 600）
2. 优先使用 API token 而不是密码
3. 不要将此文件加入版本控制系统
4. 定期更新 token
5. 不同项目使用不同的 token

## 使用场景

1. 上传包到官方 PyPI
2. 上传包到测试版 PyPI
3. 上传包到私有 PyPI 服务器
4. 配置多个不同的包索引服务器

## 注意事项

1. 确保文件格式正确（INI 格式）
2. 避免在配置文件中使用明文密码
3. 正确设置文件权限
4. 备份配置文件
5. 定期检查和更新配置

## 配置示例

### 1. 基本配置示例
使用用户名和密码的基础配置：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = your_username
password = your_password

[testpypi]
repository = https://test.pypi.org/legacy/
username = your_username
password = your_password
```

### 2. 使用 API Token 的配置（推荐）
使用更安全的 Token 认证方式：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-xxxxx...  # 你的 PyPI API token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxx...  # 你的 TestPyPI API token
```

### 3. 多仓库配置示例
包含私有仓库的配置：

```ini
[distutils]
index-servers =
    pypi
    testpypi
    private

[pypi]
username = __token__
password = pypi-xxxxx...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxx...

[private]
repository = https://private.company.com/pypi
username = internal_user
password = internal_password
```

## 使用方法

### 1. 上传到官方 PyPI

```bash
python -m twine upload dist/*
```

### 2. 上传到测试 PyPI

```bash
python -m twine upload --repository testpypi dist/*
```

### 3. 上传到私有仓库

```bash
python -m twine upload --repository private dist/*
```

### 4. 使用环境变量（替代配置文件）

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-token-here
python -m twine upload dist/*
```

## 常见问题解决

### 1. 权限问题
在 Linux/Mac 系统中设置正确的文件权限：

```bash
chmod 600 ~/.pypirc
```

### 2. Token 获取方法
获取 PyPI API Token：

```bash
# 1. 访问 https://pypi.org/manage/account/token/
# 2. 创建新 token
# 3. 复制并保存 token（只显示一次）
```

### 3. 配置验证
验证配置是否正确：

```bash
python -m twine check dist/*
```

## 最佳实践

1. Token 命名建议：
```ini
project-name-push-YYYYMMDD
```

2. 环境变量设置（Windows）：
```batch
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=your-token-here
```

3. 环境变量设置（Linux/Mac）：
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-token-here
```
