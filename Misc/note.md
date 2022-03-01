筆記用
=======


刪除邊
```

    def remove_relative_edge(self, edge):
        finish = False
        while not finish:
            finish = True
            for e in self.edgesInfo:
                if not(e in self.edges or (e[0], e[1]) in self.edges):
                    self.edgesInfo.pop(e)
                    finish = False
```


Pop up window design
------
### method
#### 新增元件類別

```
text      : 按鈕上呈現的文字
posx      : 按鈕左上角位置的x值
posy      : 按鈕左上角位置的y值
width     : 按鈕寬度
height    : 按鈕高度
parent    : 按鈕父元件
object_id : 元件ID
container : 包含元件的容器 預設為Root

add_button(text,posx,posy,width,height,parent,object_id,container) 新增按鈕

add_panel(posx,posy,width,height,parent,object_id,container) 新增panel

add_label(text,posx,posy,width,height,parent,object_id,container) 新增label

add_dropdown_menu(posx,posy,width,height,parent,option_list,starting_option,container) 新增menu

add_entryline(posx,posy,width,height,parent,object_id,container) 新增輸入框

```
#### 其他

### Set window
#### 元件

* Label:
   + Start
   + Destination
   + Radius
   + MinSize
* Button:
   + Confirm
   + Cancel
* EntryLine:
   + Radius
   + MinSize
* Dropdown menu:
   + Start
   + Destination


```
#################
Label
-------     :   t          x    y    w    h     
Start       :   start     50   50   90   20 
Destination :   dest..    50   80   90   20
Radius      :   rad..     50   110  90   20
MinSize     :   min..     50   140  90   20
#################
Button
-------         x       y       w       h
Confirm     :   100     280     70      50
Cancel      :   220     280     70      50
#################
EntryLine
-------         x       y       w       h
Radius      :   140     110     60      20
MinSize     :   140     140     60      20
#################
DropdownMenu    x       y       w       h
-------
Start       :   140     50      90      20
Destination :   140     80      90      20   

```




error message
```
start 為空
destination 為空
Radius 非整數
Radius 為空
Radius 超出範圍(0,min(width,height))
MinSize 為空
MinSize 非整數
MinSize 超出範圍
```

## 動畫功能設計

開兩個thread，一個監控按鈕組態(主程式)，一個負責跑動畫(Animation)，

主程式分兩種模式:

1. 未跑動畫模式 
   + 負責切換版面
   + 圖的操作
2. 動畫模式
   + 負責根據mediaState來切換按鈕組態(disable/enable)
   + 監控mediaState的切換

## Media Sate 
Media State = [mainState,subState]
mainState,subState 是兩個字串，代表多媒體按鈕主狀態和副狀態
用一個全域的常數來存這些字串
* InitState
   + 組態說明 : 初始狀態
   + Media State = [INITSTATE,DEFAULT]
* GraphNotCompileState
   + 組態說明 : 有圖但未編譯
   + Media State = [NOTCOMPILESTATE,DEFAULT]
* GraphComipileState
   + 組態說明 : 圖編譯完成但未按下播放(創建Animation實體)
   + Media State = [COMPILESTATE,DEFAULT]
* PlayOnlyFrameState
   + 組態說明 : 播放只有一張圖的動畫
   + Media State = [PLAYSTATE,ONLY]
* PlayFirstFrameState
   + 組態說明 : 動畫播放第一張圖
   + Media State = [PLAYSTATE,FIRST]
* PlayIntermediaState
   + 組態說明 : 動畫播放非第一也非最後一張圖
   + Media State = [PLAYSTATE,INTERMIDIATE]
* PlayLastFrame
   + 組態說明 : 動畫播放最後一張圖
   + Media State = [PLAYSTATE,LAST]
* PauseOnlyFrameState
   + 組態說明 : 播放只有一張圖的動畫
   + Meida State = [PAUSESTATE,ONLY]
* PauseFirstFrameState
   + 組態說明 : 動畫播放第一張圖
   + Media State = [PAUSESTATE,FIRST]
* PauseIntermediaState
   + 組態說明 : 動畫播放非第一也非最後一張圖
   + Media State = [PAUSESTATE,INTERMIDIATE]
* PauseLastFrame
   + 組態說明 : 動畫播放最後一張圖
   + Media State = [PAUSESTATE,LAST]

### Media State各按鈕狀態
|MediaState|Play|Pause|Build|Next|Previous|Load|Store|Speed+|Speed-|Add|Del|Set|
|:---------|:---|:----|:----|:---|:-------|:---|:----|:-----|:-----|:--|:--|:--|
|

Reference
------
1. icon下載網站
   https://icons8.com/icons/set/play
