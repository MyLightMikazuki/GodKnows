# GodKnows

神的語言漫畫下載程式，無須登入即可使用

## 需求

需要 Requests 模組，輸入下指令下載

    $ pip3 install requests

## 操作方法

依據車號直接下載（一次只能下載一個）

    $ python3 god_knows.py -i 381952

依據車號檔案直接下載（一次能下載多個）

    $ python3 god_knows.py -f data.txt

將下載檔案放到指定資料夾

    $ python3 god_knows.py -f data.txt -d myfile

翻譯車號對應書名

    $ python3 god_knows.py --translate

## 注意事項

下載完後會產生一個 nhentai_status.txt 的檔案，請不要刪除它，它會紀錄已經下載過的車號，避免重複下載浪費時間。

## TODO
* 依據 tag 下載
* 翻譯中文 tag
* 隨機下載
* 增進下載效率
* 增加車號以便老司機打包下載
