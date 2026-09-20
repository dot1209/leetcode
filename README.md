# LeetCode Pattern Notes

以 **演算法 pattern** 為單位整理的 LeetCode 筆記。重點放在 pattern 層級的觀察（什麼時候用、為什麼複雜度是這樣），題目本身只是 reference material。

## 結構

- `patterns/` — 每個 pattern 一個檔案或一個資料夾，放 pattern 層級的觀察，以及每題的三行摘要（Trigger / Insight / Pitfall）
  - 單一檔案：pattern 還沒分化出明顯變體
  - 資料夾：題目真的能分成 2+ 種**不同的子類**（核心技巧 / 迴圈結構 / invariant 不同）才拆——看的是能不能分類，不是題數
- `problems/<pattern>/` — 每題一個獨立檔案，放完整 write-up（trigger、insight、複雜度、code、pitfalls），由 pattern 檔的摘要連過來

## 使用方式

解完一題後，告訴 Claude 題目與 pattern，會自動 append 到對應檔案；新增 pattern 或拆分變體前都會先確認。

筆記格式由 `.claude/skills/leetcode-notes/SKILL.md` 定義，可用 `python .claude/skills/leetcode-notes/check.py` 檢查整個 repo 有沒有壞連結、漏摘要、跑掉的 section 或 index。

<!-- INDEX START -->
## Patterns

### [Array](patterns/array/README.md)
操作 1D / 2D 陣列；常見 follow-up 是把 O(n) 輔助空間壓到 O(1)，靠陣列自身位置承載資訊。
- [In-place Marker](patterns/array/in-place-marker.md)
- [In-place Transform](patterns/array/in-place-transform.md)

### [Backtracking](patterns/backtracking/README.md)
列舉解空間的樹狀搜尋，核心是「make choice → recurse → undo」。
- [Grid Backtracking](patterns/backtracking/grid-backtracking.md)

### [BFS](patterns/bfs/README.md)
按距離分層擴散的搜尋，邊權都相等時保證第一次到達即為最短。
- [Multi-source BFS](patterns/bfs/multi-source-bfs.md)

### [Dynamic Programming](patterns/dp/README.md)
把重疊子問題用表記下來，避免重複計算；典型訊號是純 recursion 會 TLE。
- [0/1 Knapsack](patterns/dp/knapsack-01.md)
- [Unbounded Knapsack](patterns/dp/knapsack-unbounded.md)
- [String Partition](patterns/dp/string-partition.md)
- [Two-Sequence](patterns/dp/two-sequence.md)

### [Frequency Counting](patterns/frequency-counting.md)
先掃一遍把每個元素出現幾次記下來，再從計數表推答案；最常見形式是 bottleneck min——用一袋字元重複拼目標字，能拼幾組卡在最稀缺的字母上。

### [Greedy](patterns/greedy.md)
每步做當下最佳選擇、不回頭，靠 exchange argument 證明 local optimal → global optimal；最常見形式是 sort 後依序貪心取用。

### [Greedy + Stack](patterns/greedy-stack.md)
用 stack 暫存已讀元素，貪心決定何時吐出，建構字典序最佳的輸出；關鍵在 flush 條件——比較 top 與剩餘未讀部分的極值。

### [Heap / Priority Queue](patterns/heap.md)
動態取集合極值；當每個 step 後集合會變動又得再次取極值時，比 sort 更划算。

### [Linked List](patterns/linked-list/README.md)
操作 singly / doubly linked list；許多題能藉「改寫 node 指標欄位」達到 O(1) 額外空間。
- [Deep Copy](patterns/linked-list/deep-copy.md)
- [In-place Rewiring](patterns/linked-list/in-place-rewiring.md)

### [Monotonic Stack](patterns/monotonic-stack.md)
用單調的 stack 存住「還在等答案的元素」，pop 的那一刻就是答案定案的那一刻；用於 next greater / smaller 與「以某元素為極值能延伸多遠」類問題。

### [Sliding Window](patterns/sliding-window.md)
用左右指針框出連續區間並隨掃描滑動，把「枚舉所有 subarray/substring」壓成線性掃描；靠增量維護視窗狀態避免重算。

### [String](patterns/string/README.md)
字串為主要輸入、操作集中在字元層級而非 array random access；解析、模擬大數運算、模式比對等。
- [Pattern Matching (KMP)](patterns/string/pattern-matching.md)
- [Simulation](patterns/string/simulation.md)
<!-- INDEX END -->
