# Heap / Priority Queue

Heap 是一個只保證「**根節點為集合極值**」的 partial-ordered 樹（C++ STL `priority_queue` 預設為 max-heap）。它的存在價值是：當集合會被反覆 insert / extract，而每一步都要再次取極值時，sort 一次 O(n log n) 沒辦法跟著動，於是改用 heap 把每次取極值的代價壓到 O(log n)。

## When to Use
- 每個 step 都需要當下集合的最大／最小值，且集合會在過程中變動（push 新元素、pop 舊元素）
- 訊號詞：「每次取頻率最高的」「合併最小的兩個」「Top K」「scheduling with priority」
- 反例：靜態取極值 → sort 或 `nth_element` 就夠了，不需要 heap

STL 對應：
- `priority_queue<int>` — 預設 max-heap
- `priority_queue<int, vector<int>, greater<int>>` — min-heap

## Typical Complexity
**Time:** push / pop 各 O(log n)，peek O(1)。整題常見 O(n log n) 或 O(n log k)（k 為 heap 大小上限）。
**Space:** O(n) 或 O(k) — heap 自身佔用。

當題目只關心 top-k 時，限制 heap 大小到 k 可以把 time 從 O(n log n) 降到 O(n log k)，space 從 O(n) 降到 O(k)。這是「靜態 sort 全部 vs 動態維護一個 k-size heap」的關鍵差異。

## Template Code
```cpp
priority_queue<int> pq;             // max-heap
// priority_queue<int, vector<int>, greater<int>> pq;  // min-heap

for (int x : nums) pq.push(x);

while (!pq.empty()) {
    int top = pq.top();
    pq.pop();
    // process top; possibly push something derived back
    // (e.g. top - 1, or merged value)
}
```

## 候選的加入順序與取用順序
排程或區間查詢可以依 `start` 排序，用指標把已開始的項目加入 heap。排序決定「何時能選」，heap key 決定「能選的項目裡先選誰」，兩者可以不同。例如活動從 `startDay` 開始可選，但取用時優先考慮最早的 `endDay`。

取 heap top 前先清除不再合法的候選。當 heap 空且下一個項目尚未開始時，可跳到下一個開始時刻；指標走到尾端只代表已沒有新候選，heap 裡的項目仍須處理。

## Dijkstra：累積距離、Relaxation 與最終確定

Dijkstra 使用 Min-Heap 依照**從 Source 到節點的累積成本（Tentative Distance）**決定探索順序，而不是依照單條 Edge Weight。前者求 Single-Source Shortest Path；後者則像 Prim's MST 的選邊準則。

- `dist[v]` 可以在 Relaxation 時更新：它是目前找到的最佳候選值，不代表已定案。
- 當 `(cost, v)` 以 `cost == dist[v]` 從 Min-Heap Pop 出來時，在**非負權重**前提下，`dist[v]` 才確定是最短距離。
- Lazy Heap 不必刪掉舊 Entry。如果 `cost > dist[v]`，這筆 Stale Entry 已被更低成本支配，直接跳過。
- 只有 `newCost < dist[v]` 才更新並 Push。若對每條 Edge 都無條件 Push，Cycle 可能讓 Queue 永遠不清空。
- 需要所有節點距離時，讓 Heap 清空，再檢查不可達節點；只求單一終點時，可以在該終點以最新 Entry 被 Pop 時提早結束。

**Correctness：** 反證若 Pop 出 `u` 的成本 `d` 還不是最短，取更短路徑上第一個尚未確定距離的節點 `x`。其前驅已處理過，且權重非負，故 `x` 應已有小於 `d` 的候選距離，應先於 `u` Pop，矛盾。

**Complexity：** Lazy PQ 在 E 條邊上最多有 E 次成功 Relaxation，加起點共至多 E + 1 次 Push，Heap 操作為 O(log(E + 1))。整體 Time O(V + E log(E + 1))、Space O(V + E)。

**English：** Dijkstra pops the node with the smallest tentative distance. Because all edge weights are non-negative, a cheaper path through any unsettled node would have caused that node to be popped first. Therefore, a non-stale node's shortest distance is finalized when it is popped.

## Pitfalls
- **同輪內不能立刻 push 回去**：若一輪要從 heap 取多個不同元素，pop 出來後要先暫存，整輪結束再 push 回，否則同一個元素可能在同輪被取兩次
- **`priority_queue` 預設是 max-heap**，跟很多語言（Python `heapq` 是 min-heap）相反，min-heap 要明寫 `greater<>`
- **`auto [_, v] : mp` 的 `_` 不是 wildcard**，只是普通變數名，編譯器只把它當一個叫 `_` 的變數
- **Dijkstra 的 Min-Heap Key 寫成單條 Edge Weight**：必須放從 Source 到節點的累積 Cost，否則混淆成 Prim。
- **Relaxation 時只 Push 不更新 dist，或無條件 Push**：會造成重複展開，Cycle 還可能無限延伸；更新 `dist` 與 PQ Entry 必須成對進行。

---

## Problems

### [[621] Task Scheduler](../problems/heap/task_scheduler.md)
**Complexity:** Time O(n log k), Space O(k) — n 為 tasks 總數，k 為 unique 任務數（≤ 26）
- **Trigger:** 每一輪都要挑「當下頻率最高的任務」→ 動態取極值
- **Insight:** 每 `n+1` 個 slot 為一輪，整輪先從 heap pop 出最多 `n+1` 個不同任務各執行一次，剩餘頻率 > 0 的等該輪結束再 push 回；避免同任務在同輪被取兩次
- **Pitfall:** 最後一輪不必補 idle — pq 空了就只算實際執行的任務數，不是固定 `n+1`

### [[1353] Maximum Number of Events That Can Be Attended](../problems/heap/maximum_number_of_events_that_can_be_attended.md)
**Complexity:** Time O(N log N), Space O(N)
- **Trigger:** 每個活動只占可用區間內一天；每天從已開始且未過期的候選中選一個。
- **Insight:** 依 `startDay` 排序加入活動，min-heap 依 `endDay` 選最早到期者；無候選時跳到下一個開始日。
- **Pitfall:** 同一天先加入全部新活動並清過期，再選一個；輸入掃完後仍要處理 heap 裡的候選。

### [[743] Network Delay Time](../problems/heap/network_delay_time.md)
**Complexity:** Time O(V + E log(E + 1)), Space O(V + E)
- **Trigger:** 單一起點訊號傳遍所有節點，邊權非負，求所有節點最短距離的最大值。
- **Insight:** 以 `(累積成本, node)` 做 Min-Heap Key；每次成本改善時同步更新 `dist` 並 Push，非最新的 Entry Pop 時跳過。
- **Pitfall:** 不能用單條 Edge Weight 排序，也不能無條件 Push 鄰居；只有成功 Relaxation 才能產生新 Entry。
