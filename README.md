# LeetCode Pattern Notes

以 **演算法 pattern** 為單位整理的 LeetCode 筆記。重點放在 pattern 層級的觀察（什麼時候用、為什麼複雜度是這樣），題目本身只是 reference material。

## 結構

- `patterns/` — 每個 pattern 一個檔案或一個資料夾
  - 單一檔案：pattern 還沒分化出明顯變體
  - 資料夾：pattern 有 3+ 變體，或內容超過 ~300 行
- `templates/` — 獨立的 code skeleton（optional）

## 使用方式

解完一題後，告訴 Claude 題目與 pattern，會自動 append 到對應檔案；新增 pattern 或拆分變體前都會先確認。

<!-- INDEX START -->
## Patterns

### [Array](patterns/array/README.md)
操作 1D / 2D 陣列；常見 follow-up 是把 O(n) 輔助空間壓到 O(1)，靠陣列自身位置承載資訊。
- [In-place Marker](patterns/array/in-place-marker.md)

### [Backtracking](patterns/backtracking/README.md)
列舉解空間的樹狀搜尋，核心是「make choice → recurse → undo」。
- [Grid Backtracking](patterns/backtracking/grid-backtracking.md)

### [BFS](patterns/bfs/README.md)
按距離分層擴散的搜尋，邊權都相等時保證第一次到達即為最短。
- [Multi-source BFS](patterns/bfs/multi-source-bfs.md)

### [Linked List](patterns/linked-list/README.md)
操作 singly / doubly linked list；許多題能藉「改寫 node 指標欄位」達到 O(1) 額外空間。
- [Deep Copy](patterns/linked-list/deep-copy.md)
- [In-place Rewiring](patterns/linked-list/in-place-rewiring.md)
<!-- INDEX END -->
