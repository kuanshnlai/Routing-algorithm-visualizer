# 測試資料

---
<!-- TOC -->

- [測試資料](#測試資料)
- [Graph operation + Pop up window 測試](#graph-operation--pop-up-window-測試)
  - [Add Node Window `Mode : Node`](#add-node-window-mode--node)
  - [Add Node Window `Mode : Edge`](#add-node-window-mode--edge)
  - [Del Node Window `Mode : Node`](#del-node-window-mode--node)
  - [Del Node Window `Mode : Edge`](#del-node-window-mode--edge)
  - [Graph operation 測試](#graph-operation-測試)
  - [File 功能測試](#file-功能測試)

<!-- /TOC -->

Graph operation + Pop up window 測試
======
Operation 縮寫說明
   + DN P   : Delete node P
   + DE P Q : Delete edge (P,Q)
   + AN P X Y : Add node P at pos(X,Y)
   + AE W S D : Add edge (S,D) with weight W 

POP UP Window Message 縮寫說明
   `X is variable`
   `M means message`
   * M XAE  : X already exist     
   * M XCE  : X cannot be empty
   * M XOR  : X out of range
   * M XNE  : X not exist
   * M XMI  : X must be integer
   * M XYMD : X and Y must be different
   ```
      M NAE: Name already exist
      M NCE: Name cannot be empty
      M XCE: X cannot be empty
      M YCE: Y cannot be empty
      M XMR: X must in range
      M YMR: Y must in range
      M XMI: X must be int
      M YMI: Y must be int
      M WCE: Weight cannot be empty
      M WMI: Weight must be integer
   ```

input output 格式
   ```
   + Input
    ```
      some instructions
    ```
   + Output:
    ```
      some messenger or description of output
    ```
   ```

## Add Node Window `Mode : Node`




1. Testdata1      
   + Input
    ```
    AN 0 100 200
    AN 0 200 300
    ```
   + Output:
    ```
    M NAE
    ```

2. Testdata2      `測試節點ID為空`
   + Input
    ```
    AN '' 100 200
    ```
   + Output
    ```
    M NCE 
    ```
3. Testdata3      `測試節點X為空`
   + Input
    ```
    AN 0 '' 200
    ```
   + Output
    ```
    M XCE 
    ```
4. Testdata4      `測試節點Y為空`
   + Input
    ```
    AN 0 100 ''
    ```
   + Output
    ```
    M YCE 
    ```
5. Testdata5      `測試節點ID X Y 為空`
   + Input
    ```
    AN '' '' ''
    ```
   + Output
    ```
    M NCE 
    M XCE
    M YCE
    ```

6. Testdata6      `測試節點 X 不為 int (1)`
   + Input
    ```
    AN 0 'x' 100
    ```
   + Output
    ```
    M XMI
    ```
7. Testdata7      `測試節點 Y 不為 int (1)`
   + Input
    ```
    AN 0 100 'Y'
    ```
   + Output
    ```
    M YMI
    ```

8. Testdata8       `測試節點 X 不為 int (2)`
   + Input
    ```
    AN 0 1.23 100
    ```
   + Output
    ```
    M XMI
    ```
9. Testdata9       `測試節點 Y 不為 int (2)`
   + Input
    ```
    AN 0 100 1.23
    ```
   + Output
    ```
    M YMI
    ```
10. Testdata10       `測試X大於圖寬度`
    + Input
    ```
    AN 0 1000 200
    ```
    + Output
    ```
    M XOR
    ```
11. Testdata11      `測試Y大於圖高度`
    + Input
    ```
    AN 0 100 2000
    ```
    + Output
    ```
    M YOR
    ```
12. Testdata12      `測試X小於0`
    + Input
    ```
    AN 0 -10 200
    ```
    + Output
    ```
    M XOR
    ```
13. Testdata13      `測試Y小於0`
    + Input
    ```
    AN 0 100 -200
    ```
    + Output
    ```
    M YOR
    ```

## Add Node Window `Mode : Edge`


1. Testdata1        `測試Weight 為空`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE '' 0 1
    ```
   + Output
    ```
    M WCE
    ```
2. Testdata2        `測試Weight不為int(1)`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 's' 0 1
    ```
   + Output
    ```
    M WMI
    ```
3. Testdata3        `測試Weight不為int(2)`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 1.23 0 1
    ```
   + Output
    ```
    M WMI
    ```   
4. Testdata4        `測試Start為空`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 1 "Default" 1
    ```
   + Output
    ```
    M SCE
    ```   
5. Testdata5        `測試Destination為空`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 1 0 "Default"
    ```
   + Output
    ```
    M DCE
    ```      
6. Testdata6        `測試Start Destination 相同`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 1 0 0
    ```
   + Output
    ```
    M SDMD
    ```         
7. Testdata7        `測試邊已存在(1)`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 1 0 1
    AE 1 0 1
    ```
   + Output
    ```
    M EAE
    ```    
8. Testdata8         `測試邊已存在(2)`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    AE 1 0 1
    AE 1 1 0
    ```
   + Output
    ```
    M EAE
    ```
      
## Del Node Window `Mode : Node`


1. Testdata1 `節點ID不存在`
   + Input
    ```
    AN 0 100 200
    DN 1
    ```
   + Output
    ```
    M NNE
    ```
2. Testdata2 `節點ID為空`
   + Input
    ```
    AN 0 100 200
    DN ''
    ```
   + Output
    ```
    M NCE
    ```

## Del Node Window `Mode : Edge`

1. Testdata1 `邊不存在`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    DE 0 1
    ```
   + Output
    ```
    M ENE
    ```
2. Testdata2 `Start為空`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    DE '' 1
    ```
   + Output
    ```
    M SCE
    ```
3. Testdata3 `Destination為空`
   + Input
    ```
    AN 0 100 200
    AN 1 200 300
    DE 0 ''
    ```
   + Output
    ```
    M DCE
    ```

## Graph operation 測試



1. Testdata1 `新增多個節點`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
    ```
   + Output:
    ```
      畫面上出現三個節點
      節點資訊如下:
         0 : (100,200)
         1 : (400,300)
         2 : (300,200) 
    ```
2. Testdata2 `新增多個邊`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,1) :   1 
         (0,2) :   1
         (1,2) :   1
    ```
3. Testdata3 `刪除邊 [0,1]`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DE 0 1
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,2) :   1
         (1,2) :   1
    ```
4. Testdata4 `刪除邊 [1,0]`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DE 1 0
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,2) :   1
         (1,2) :   1
    ```
5. Testdata5 `刪除邊 [0,1] 後新增相同邊[0,1]`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DE 0 1
      AE 1 0 1 
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,1) :   1 
         (0,2) :   1
         (1,2) :   1
    ```
6. Testdata6 `刪除邊 [0,1] 後新增相同邊[1,0]`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DE 0 1
      AE 1 1 0
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,1) :   1 
         (0,2) :   1
         (1,2) :   1
    ```
7. Testdata7 `刪除邊 [1,0] 後新增相同邊[0,1]`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DE 1 0
      AE 1 0 1
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,1) :   1 
         (0,2) :   1
         (1,2) :   1
    ```
8. Testdata8 `刪除邊 [1,0] 後新增相同邊[1,0]`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DE 1 0
      AE 1 1 0
    ```
   + Output:
    ```
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,1) :   1 
         (0,2) :   1
         (1,2) :   1
    ```
9.  Testdata9 `刪除節點 X 後刪除跟 X 有關的邊`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DN 0
      DE (0,1)
    ```
   + Output:
    ```
      執行DE指令時會跳出錯誤
      M ENE
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (1,2) :   1
    ```
10. Testdata10 `刪除節點 X 後重新新增節點 X 並新增原本跟 X 有關的邊`
   + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DN 0
      AN 0 100 200
      AE 1 0 1
    ```
   + Output:
    ```
      執行DE指令時會跳出錯誤
      M ENE
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         1   : (400,300)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,1) :   1
         (1,2) :   1
    ```
11. Testdata11 `複合情況`
    + Input
    ```
      AN 0 100 200
      AN 1 400 300
      AN 2 300 200
      AE 1 0 1
      AE 1 0 2
      AE 1 1 2
      DN 0
      AN 0 100 200
      AE 1 0 1
      AE 1 2 0
      DN 1
    ```
   + Output:
    ```
      執行DE指令時會跳出錯誤
      M ENE
      畫面上出現三個節點及三個邊
      節點資訊如下:
         ID  :   Pos
         0   : (100,200)
         2   : (300,200)
      邊的資訊如下:
         Edge  : Weight
         (0,2) :   1 
    ```

## File 功能測試

1. Testdata1 `Load 正確格式檔案`
   + Input
    ```
      格式正確的correct.json
      Load "C:\....\correct.json"
    ```
   + Output:
    ```
      畫面會用load的檔案的圖的資訊來覆蓋原本的圖
    ```
2. Testdata2 `Load 錯誤格式檔案`
   + Input
    ```
      格式正確的incorrect.json
      Load "C:\....\incorrect.json"
    ```
   + Output:
    ```
      跳出錯誤提示訊息
      畫面會不變
    ```