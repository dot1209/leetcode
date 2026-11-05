# DFS

## When to Use
- 題目要求判斷兩個節點是否連通，或從起點沿著圖搜尋任一條可行路徑。
- 沿路需要攜帶狀態，例如累積權重、路徑資訊或目前答案。
- 可以先選一個鄰居深入探索，再回到上一層繼續處理其他鄰居；不要求依距離分層取得最短路。

## Typical Complexity
**Time:** O(V + E) — 單次完整搜尋中，每個節點最多展開一次，每條 adjacency entry 最多掃描一次；提前找到目標可以提早結束，但 worst case 不變。
**Space:** O(V) — visited 與最深遞迴 stack 各為 O(V)，不包含輸入圖；若自行建 adjacency list，圖另占 O(V + E)。

Hash-based graph 的操作假設為 expected O(1)，字串長度視為常數。若每筆 query 都重新搜尋，Q 筆查詢的時間為 O(Q(V + E))；查詢逐次執行，搜尋空間不用乘上 Q。

## Template Code
```cpp
bool dfs(int cur, int target, const vector<vector<int>>& adj,
         vector<bool>& visited) {
    if (cur == target) {
        return true;
    }

    visited[cur] = true;
    for (int next : adj[cur]) {
        if (visited[next]) {
            continue;
        }

        bool found = dfs(next, target, adj, visited);
        if (found) {
            return true;
        }
    }

    return false;
}
```

## Recursive Calls and Return Flow
每次呼叫都有自己的 cur、區域變數與 for 迴圈進度。呼叫下一層時，這一層暫停；下一層 return 後，這一層從呼叫後面的敘述繼續執行。

- 子搜尋成功，才把成功結果往上傳。
- 子搜尋失敗，繼續看其他鄰居；單一分支失敗不代表目前節點的搜尋失敗。
- 所有尚未拜訪的鄰居都探索完，才在迴圈外回傳失敗。

遇到已拜訪的鄰居，直接跳過該鄰居。只有抵達 target 才能回傳成功；繞圈回到舊節點不代表找到查詢終點。

## Accumulated State and Return Contracts
寫 DFS 前，先分清楚「往下傳的參數」與「往上回傳的結果」。以乘法權重為例，可採用兩種不同的 contract，但不能混用：

| 設計 | 參數或回傳值的意義 | 抵達 target | 子搜尋成功後 |
|---|---|---|---|
| 累積值往下傳 | cur_val 已包含起點到 cur 的權重乘積；回傳值是起點到 target 的完整答案 | 回傳 cur_val | 直接回傳 res |
| 剩餘結果往上組合 | 回傳值只代表 cur 到 target 的權重乘積 | 回傳乘法單位元 1 | 回傳 edge_weight * res |

第一種設計的 cur_val * edge_weight 只代表走到 next，後面的路徑由下一層繼續探索。下一層成功後，res 已經是完整答案，不能換回目前這一層的部分累積值。

## DFS Path State：Prefix Sum 與 Backtracking

當問題允許路徑從任意節點開始、只能沿 Parent → Child 往下延伸時，不一定要從每個節點重新 DFS。若題目要求 Path Sum 等於 Target 的**路徑數量**，可用 Root-to-Current Prefix Sum 搭配 Hash Map Frequency，把「列舉所有起點」轉換成「查詢有多少個 Past Prefix 使差值等於 Target」。

- **Prefix Identity：** `PathSum = CurrentPrefix - AnyPastPrefix`，因此查詢 `prefix_mp[currentPrefix - target]`。Map Value 是該 Prefix 的出現次數，不是布林值；不同 Ancestor 位置即使有相同 Sum，也對應不同起點。
- **Query Before Insert：** 先查目前 Ancestors 的 Prefix Frequency，再插入 Current Prefix 供 Children 使用。否則當 Target 為 0，`CurrentPrefix - CurrentPrefix` 會把沒有任何 Node 的 Empty Path 錯誤計數。
- **Empty Prefix：** `prefix_mp[0] = 1` 表示 Root 之前的虛擬起點，可以計算從 Root 開始、至少包含一個節點的路徑，和 Empty Path 不同。
- **DFS Lifecycle：** `Enter → Update Prefix → Query → Insert → DFS Children → Decrement → Return`。頻率大於 0 的 Prefix 必須只來自目前的 Ancestor Path。返回 Parent 前移除自己的那一次頻率，避免把 Sibling Branch 當成 Ancestor。
- **Traversal Order ≠ Backtracking：** Pre-order / Post-order 描述處理 Node 的時間；Backtracking 描述共用 State 的有效範圍。Prologue 建立 Context、Epilogue Restore，並不表示這題是純 Post-order DP。
- **Complexity：** Hash Map 操作平均 O(1)，DFS 一次走訪 V 個 Node，Time O(V) expected。若用 `operator[]` 查不存在的 Key、離開時也不 Erase 零次數 Key，Map 可能保留 O(V) 個 Key；改用 `find()` 並移除零頻率 Key，可把 Map Space 壓到 O(H)。

**Correctness：** 每條 Downward Path 有唯一終點；到達終點時，Hash Map 中每一個符合 `currentPrefix - target` 的 Past Prefix 位置，都對應唯一的合法起點。Backtracking 使這些位置只能來自目前的 Ancestor Chain，因此不會漏算、重複計數或跨左右分支。

**English：** The prefix-frequency map represents prefix sums along the current ancestor path. For each current node, every previous prefix equal to `currentPrefix - target` identifies a valid starting position. Query before inserting the current prefix, and decrement its frequency on return to prevent sibling branches from sharing path state.

## Pitfalls
- 把失敗 return 放在 for 裡面：第一個鄰居找不到就停止，其他分支完全沒被搜尋。
- 收到子搜尋的完整答案後，卻回傳目前只走一條邊的值，或再次累乘已經包含在答案中的前綴。
- 把 visited 當成找到終點的判斷。visited 是避免重複展開節點的工具，成功條件仍是 cur == target。
- 對每筆獨立查詢，必須重新建立 visited；判斷可達性時，同一筆搜尋內不必在回傳時移除 visited。列舉所有路徑的 backtracking 則需要不同的狀態生命週期。
- 若節點以名稱表示，先確認起終點存在，才處理同點查詢；否則未知節點也可能被當成合法起點。
- 非 void 函式的執行路徑若走到結尾卻沒有回傳值，會造成 undefined behavior。
- 遞迴深度最壞可達 O(V)；大圖可改用 explicit stack，並自行保存必要的搜尋狀態。
- 需要共用目前 Path 的 State 時，不要把 Pre-order / Post-order 與 Backtracking 混淆；由當前 DFS Call 負責建立、維護並恢復自己的 Context。
- Prefix Sum 計數要先查詢 Ancestors，再把當前 Prefix 加入 Map；插入後才查會把空路徑算成合法答案。

---

## Problems

### [[399] Evaluate Division](../problems/dfs/evaluate_division.md)
**Complexity:** Time O(E + Q(V + E)), Space O(V + E)
- **Trigger:** 已知變數間的比值，查詢是否能從 query[0] 沿等式關係走到 query[1]
- **Insight:** 建立互為倒數的雙向加權邊，以 1 初始化累積值，沿邊相乘；抵達目標後把完整結果逐層回傳
- **Pitfall:** 成功時應回傳 res，而非只到下一個節點的 cur_val * val；失敗必須等所有鄰居都試完才回傳

### [[437] Path Sum III](../problems/dfs/path_sum_iii.md)
**Complexity:** Time O(V) expected, Space O(V)
- **Trigger:** Binary Tree 中任意起終點的 Downward Path，要求計算 Sum 等於 Target 的路徑數量。
- **Insight:** 用 Root-to-Current Prefix Sum，查詢 `currentPrefix - target` 的歷史 Prefix Frequency；每節點先 Query 再 Insert，DFS 返回時 Decrement。
- **Pitfall:** 不能用 Maximum Path Sum 的負數剪枝；不要把 Current Prefix 算成自己的 Past Prefix，且必須 Backtrack 防止 Sibling Branch 污染。
