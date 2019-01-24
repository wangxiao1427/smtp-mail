---------------------------------------------------------------------
* 更新版本发布流程
1. 在setup.py更新版本号
2. 生成最新版本发布包 `python setup.py sdist`
3. 第一次时,安装上传组件 `pip install twine`
4. 上传指定发布包 `twine upload dist/smtp-mail-0.0.1.tar.gz`
