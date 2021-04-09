# 进击的巨人漫画爬虫

进击的巨人漫画爬虫，爬取漫画中的每一页，下载存储到本地。

## 漫画爬取

在项目目录下执行：
```bash
python main.py
```

图片会按照章节整理，被下载到`attack-on-titan`目录下

### 参数配置

在`main.py`中，根据个人需求调整下面的参数。（可能对部分较早的章节存在问题。）

```py
start_chepter_num = 126 # 起始章节
end_chepter_num = 138 # 终止章节
base_folder = './attack-on-titan' # 本地存储的目录文件夹
```