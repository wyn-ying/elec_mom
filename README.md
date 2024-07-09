# 各个服务
## 声音合成前端页面

text2speech.html 通过8124端口与声音合成服务进行交互

## 声音合成服务

text2speech.py 通过8124端口提供服务，调用 alitts.py 实现文本转mp3文件

## MP3文件服务

httpRandomMusic.py 通过8125端口提供服务

