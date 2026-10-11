# [57] Insert Interval
**Pattern:** [Intervals](../../patterns/intervals.md)
**Complexity:** Time O(n), Space O(1) auxiliary / O(n) output
**Link:** https://leetcode.com/problems/insert-interval/

## Trigger Signals
- 原本的 intervals 已依 `start` 排序，而且彼此不重疊。
- 只需要插入一個 `newInterval`，它可能不重疊，也可能一次跨過多個 intervals。
- 題目給的 sorted + non-overlapping guarantees 很強，應優先利用，而不是先退化成一般 Merge Intervals。

## Core Insight
把整個掃描分成三段：先輸出所有完全在 `newInterval` 左邊的 intervals；接著把所有重疊區間持續 merge 進 `newInterval`；最後輸出 merge 完的 `newInterval` 與剩下所有右側 intervals。

這比「每個新東西都跟 `res.back()` 比」更貼合本題，因為原 intervals 本身已經互不重疊，唯一會改變結構的就是 `newInterval`。

## Why It's Correct
### 為什麼三個 phase 足夠
Intervals 已依 start 排序且彼此不重疊，所以相對於目前正在擴張的 `newInterval`，掃描只可能依序經過：

1. `interval.end < new.start`：current 完全在左邊，之後不可能再與它合併，直接輸出。
2. `interval.start <= new.end`：current 與 new overlap，把左右界擴成兩者 union。
3. overlap 結束後：因為後續 intervals 的 start 只會更大，剩下全部都在 merged new interval 右邊。

因此每個 interval 恰好被放進左側、合併區、或右側其中一類，不會漏掉也不會重複。

### 為什麼第二個 while 可以少檢查一半 overlap condition
一般 overlap 條件是 `new.start <= interval.end && new.end >= interval.start`。但第一個 while 已經把所有滿足 `interval.end < new.start` 的區間吃掉，所以進入第二段時，`new.start <= interval.end` 已經由 phase invariant 保證，只需要繼續檢查 `new.end >= interval.start`。

## Complexity Analysis
- **Time O(n)**：三個 while 共用同一個 index `i`，而 `i` 只會從 0 單調增加到 n；不是三次各掃 n 個元素。
- **Space O(1) auxiliary**：除了 result 外只用固定數量變數，並直接擴張 `newInterval`。
- **Output Space O(n)**：最壞情況沒有任何 merge，答案仍包含原本所有 intervals 加上 new interval。

## Solution Code
```cpp
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals,
                               vector<int>& newInterval) {
        int i = 0;
        vector<vector<int>> res;
        int n = intervals.size();

        // 1. append intervals which are at the left-hand side of newInterval
        while (i < n && newInterval[0] > intervals[i][1]) {
            res.emplace_back(intervals[i]);
            i++;
        }
        
        // 2. merge overlapping
        while (i < n && newInterval[0] <= intervals[i][1] &&
               newInterval[1] >= intervals[i][0]) {
            newInterval[0] = min(newInterval[0], intervals[i][0]);
            newInterval[1] = max(newInterval[1], intervals[i][1]);
            i++;
        }
        // 3. append newInterval
        res.emplace_back(newInterval);

        // 4. append intervals which are at the right-hand side of newInterval
        while (i < n && newInterval[1] < intervals[i][0]) {
            res.emplace_back(intervals[i]);
            i++;
        }

        return res;
    }
};
```

## Alternatives / Optimization
### 跟 res.back() 合併
可以先把 `newInterval` 正確插入 sorted stream，再像 LC 56 一樣讓每個 current interval 與 `res.back()` 比較。這個做法成立，但本題原 intervals 已 sorted + non-overlapping，因此需要額外處理「newInterval 應該在何時進 stream」；三段式通常更直接。

### 最後一段可直接 while (i < n)
第二段 overlap 結束後，因為 intervals 已排序，剩下的 intervals 必然都在 merged `newInterval` 右邊。因此最後一段的 `newInterval[1] < intervals[i][0]` 是正確但 redundant 的防守條件，可以簡化成單純把剩餘元素全部 append。保留目前 AC 寫法即可。

## Pitfalls
- **Overlap 條件只寫 `new.start <= interval.end`**：缺少另一側，會把完全位於 current 左邊的 interval 誤判成重疊。
- **把不重疊誤寫成 `c > a && d > b`**：這仍可能重疊，例如 `[1,5]` 與 `[3,8]`。
- **一開始套 `res.back()` abstraction**：不是錯，但容易因此多出插入位置與 state 管理；這題的 guarantees 讓三段式更乾淨。
- **左右註解寫反**：`new.start > interval.end` 代表 current interval 在 new interval 的左邊，不是右邊。

## Side Notes
這題很適合用來提醒自己：當 code 開始需要很多 special cases 時，先重新看題目 guarantees。這次最重要的 reset 是「sorted + non-overlapping 能不能讓流程直接分 phase？」答案就是 left → overlap → right。

## Related Problems
- [56] Merge Intervals — 所有 intervals 都可能彼此重疊；sort 後一直跟 `res.back()` 比是更自然的 abstraction
- [435] Non-overlapping Intervals — 同樣以 interval ordering 為核心，但目標改成刪除最少區間，常用 greedy
- [452] Minimum Number of Arrows to Burst Balloons — interval overlap 的 greedy 版本，重點是依 endpoint 做選擇
