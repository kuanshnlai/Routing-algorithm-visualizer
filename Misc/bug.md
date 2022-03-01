Bug 記錄
========
---
Bug 紀錄格式
-------
* [ ] 問題描述:
    + 問題所在:
    + 解決方法:
File
-------


* [X] 問題描述 : Load File 後會產生重複的節點(即一個節點會重複被新增到圖內兩次且不會報錯)   `Done 2/18`
    + 問題所在 : graph class 內有兩個存取所有node的方法
        - graph.nodes `networkX內原始存取方法`
        - graph.nodesInfo `自定義dict來存取node資訊的方法`
        ```
        這兩種方法存取結果不知為何有不同，照預期來說兩者應該要一樣的
        但卻呈現下面結果
        graph.nodes:
        node          type
        0       : <class 'int'>
        1       : <class 'int'>
        2       : <class 'int'>
        0       : <class 'str'>
        1       : <class 'str'>
        2       : <class 'str'>

        graph.nodesInfo: (預期情況)
        node          type
        0       : <class 'str'>
        1       : <class 'str'>
        2       : <class 'str'>
        ```
    + 解決方法 : 將grpah內add_node的參數一律調成str

* [ ] 問題描述 : Load File 後Del Node 後無法刪除跟被刪除的Node相關的邊
    + 問題所在 : 估計在graph刪除節點後無法刪除相關的邊 需要再測試
    + 解決方法 : 尚未
* [X] 問題描述 : Add edge [0,1]後無法用[1,0]來刪除
    + 問題所在 : del edge部分條件寫錯
    + 解決方法 : 把del edge條件改成正確的版本
