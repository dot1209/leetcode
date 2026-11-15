# Google L4 — Coverage & Mastery

此表是**依現有證據的追蹤表**，不是看過題目就視為掌握。只把「陌生變形無關鍵提示，能獨立推導＋正確 Code＋複雜度／正確性說明」視為已驗證；歷史筆記本身不足以證明獨立通過。

| 領域 | 已有練習證據 | 目前判定 | 下一個驗證方向 |
|---|---|---|---|
| Array / Hash / Prefix Sum | 525、437 有筆記；1590 回報 AC | Guided AC（1590），獨立性待驗證 | 相同 Prefix 狀態在最短、最長、計數的不同題上決定 Map 的保存策略。 |
| Sliding Window / Monotonic | 239、862 有筆記；1493 二元版回報 AC；907 曾需 Major Hint | Guided（907）；其他獨立性待驗證 | 不揭露 Pattern 的陌生 Stack／Deque 變形；驗證 Stack Invariant 與相同值歸屬。另以 1493 任意整數版驗證頻率維護與縮窗條件。 |
| Graph BFS / DFS | 133、1293、743、934 等已有練習 | 有覆蓋，獨立性待驗證 | Complete Transition：Discover → Mark/Create → Enqueue/Push → Process；陌生 Graph 變形。 |
| Union-Find | 827 使用者提供 AC Code | Independent AC 證據（單題） | 在不同型態的連通性問題重新驗證 Root／Size Invariant。 |
| Binary Search | 410 有完整筆記 | 變形不足 | 標準邊界、Answer Space 可行性證明與新題獨立實作。 |
| Trees / BST / Tree DP | 124 已練；310 提過 Brute Force | 證據不足 | LCA、BST、Tree DP／Rerooting 類陌生題。 |
| Dynamic Programming | 1235、115、416、2328 型的筆記／練習 | 有覆蓋，進階 State Modeling 待驗證 | 新 DP 問題的 State、Transition、初始化、最終讀取。 |
| Trie | 無獨立題目筆記 | Unverified | Trie 建構、查詢及延伸變形。 |
| Two Pointers / Sorting | 部分 Array 題有關聯 | Unverified（作為獨立 Pattern） | 陌生雙指針與排序後決策問題。 |
| Divide & Conquer | 無獨立題目筆記 | Unverified | 需要明確分治思路的題目。 |
| Greedy / Heap / Intervals | 1353、743、57、1899 等筆記 | 有覆蓋，證明需抽驗 | 交換論證、最小／最大候選更新、排序依據。 |
| Backtracking | 39、46、78、79 等筆記 | 有覆蓋，進階剪枝未驗證 | 陌生約束與剪枝方案。 |
| Graph MST / Advanced Shortest Path | Dijkstra 有筆記；MST 缺獨立題 | MST Unverified | MST、含限制條件的最短路。 |
| Bit Manipulation / Bitmask | XOR State DP 有紀錄 | 獨立 Bitmask 題型 Unverified | 基本 Bitmask 狀態與合法性驗證。 |
| Segment Tree / Fenwick Tree | 無獨立題目筆記 | Unverified（次優先） | Range Query／Update 動態問題。 |
| Math / Counting / Combinatorics | 部分題使用計數技巧 | 未系統驗證 | Count-by-Contribution、組合計數及模運算。 |

## 優先追蹤的弱點

- **907：** Contribution Counting、Left Previous ≤／Right Next < 的相異比較規則、Stack 計算時機、Duplicate Tie-breaking。之後用不同題先測，再按 7 天規則考慮重訪 907。
- **133 Clone Graph：** 曾漏掉新節點被 Discover 後的 Enqueue，屬於 Implementation Slip；不同 Graph Traversal 題需抽驗完整轉移鏈。
- **1590：** Prefix Modulo 關係需區分求最短時的 Latest Index，與 525 求最長時的 Earliest Index。用陌生變形驗證能否獨立推導同餘條件、選擇 Map 記錄策略，並正確處理空 Prefix、負餘數與區間長度限制。

**覆蓋狀態更新規則：** 不只加題目數；每個領域累積獨立陌生變形才提高成熟度，並保留首次完成是否接受 Hint 的證據。
