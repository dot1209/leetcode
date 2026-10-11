# Intervals

## When to Use
- 輸入由 `[start, end]` 組成，而且題目保證或允許先依 `start` 排序。
- 問題核心是判斷區間是否相交、合併重疊區間，或把一個新區間插入已排序且互不重疊的區間序列。
- 最常用的基本關係是：兩區間 `[a,b]`、`[c,d]` 不重疊 iff `b < c || d < a`；反過來，重疊 iff `c <= b && d >= a`。

## Typical Complexity
**Time:** O(n) — 當 intervals 已依 `start` 排序且只需線性掃描時，每個 interval 最多被處理一次。若題目未排序而需要先 sort，通常會變成 O(n log n)。
**Space:** O(1) auxiliary space；若答案需要建立新的 result array，output space 為 O(n)。

## Template Code
```cpp
vector<vector<int>> res;
int i = 0;

// Phase 1: intervals completely before the target interval
while (i < n && intervals[i][1] < target[0]) {
    res.push_back(intervals[i++]);
}

// Phase 2: merge every overlapping interval into target
while (i < n && target[1] >= intervals[i][0]) {
    target[0] = min(target[0], intervals[i][0]);
    target[1] = max(target[1], intervals[i][1]);
    i++;
}

res.push_back(target);

// Phase 3: intervals completely after the merged target
while (i < n) {
    res.push_back(intervals[i++]);
}
```

## 三段式思考：Left → Overlap → Right
當輸入已排序且彼此不重疊時，插入一個新 interval 後，整個序列只會經過三個 phase：

1. 完全在 new interval 左邊的區間，直接輸出。
2. 與 new interval 重疊的區間，持續擴張 new interval。
3. 一旦重疊區段結束，剩下所有區間一定都在右邊，可以直接輸出。

這個 phase ordering 本身就是 invariant。第一段結束後已知目前 interval 不可能完全在 new interval 左邊，因此第二段判斷 overlap 時，只需要看 `newEnd >= currentStart`；另一半條件已由前一個 phase 保證。

## 什麼時候適合一直跟 res.back() 比
若所有待處理 intervals 都在同一個 sorted stream 裡，而且「過去」可以被最後一個 merged interval 完整代表，就很適合用 `res.back()`。LC 56 Merge Intervals 就是典型例子：current interval 若連 `res.back()` 都接不上，更不可能跟更早的區間重疊。

LC 57 不一定要這樣做，因為原 intervals 已經 sorted + non-overlapping，直接利用 left / overlap / right 三段結構更自然。

## Pitfalls
- **只看某個 start 是否落在另一段內**：會漏掉「一個 interval 完全包住另一個」的情況。
- **把不重疊寫成 start 對 start、end 對 end**：真正要看的是一段的 start 是否已經超過另一段的 end。
- **忽略 input guarantees**：已 sorted + non-overlapping 時，不需要重新 sort，也不需要把問題退化成一般 Merge Intervals。
- **phase 註解左右寫反**：`interval.end < new.start` 代表 current interval 在 new interval 的左邊；剩下未處理的才在右邊。

---

## Problems

### [[57] Insert Interval](../problems/intervals/insert_interval.md)
**Complexity:** Time O(n), Space O(1) auxiliary / O(n) output
- **Trigger:** 原 intervals 已 sorted 且互不重疊，只插入一個可能跨越多段的 new interval
- **Insight:** 把掃描拆成 left → overlap → right；前一 phase 的 invariant 讓下一 phase 不必重做完整 overlap 判斷
- **Pitfall:** 不要一開始硬套一般 Merge Intervals 的 `res.back()` 模型，否則會多出插入位置與 special cases
