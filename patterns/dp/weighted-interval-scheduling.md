# DP — Weighted Interval Scheduling

## When to Use
- 要從 intervals 中選出總價值最大的 non-overlapping subset，每個 interval 最多使用一次。
- 每個 interval 的價值不同，因此單純 greedy 選最早結束者不一定能最大化總價值。
- 排序後，相容的 predecessors 或 successors 能形成連續範圍，因此可以在 DP transition 中使用 binary search。

## Typical Complexity
**Time:** O(n log n) — 先排序，再替每個 state 做一次 O(log n) 的相容邊界搜尋。
**Space:** O(n) — 儲存 intervals，以及 prefix 或 suffix DP table。

## State Definition and Sort Order
DP state 描述的是一整個候選集合。transition 加入某個 interval 時，必須保證引用的整個 subproblem 都與它相容，不能只檢查邊界上的一個 interval。

| State | 排序方式 | 相容分界 | 填表順序 |
|---|---|---|---|
| 前 `i` 個 intervals 的最佳值 | end time 遞增 | 最後一個 `end[j] <= start[i]` 的 `j` | 向前 |
| intervals `i..n` 的最佳值 | start time 遞增 | 第一個 `start[j] >= end[i]` 的 `j` | 向後 |

prefix DP 中，依 end time 排序能保證每個 `k <= j` 都滿足 `end[k] <= end[j] <= start[i]`。suffix DP 中，依 start time 排序能保證每個 `k >= j` 都滿足 `start[k] >= start[j] >= end[i]`。因此整個 subproblem 都能安全地與 interval `i` 組合。

先定義 candidate set，再推導 dependencies，最後決定 computation order。「前 `i` 個 intervals」不代表一定要選 interval `i`。

## Template Code
以下 prefix template 把真實 jobs 放在索引 `1..n`，索引 `0` 則放時間早於所有真實工作的零值 guard。

```cpp
sort(jobs.begin() + 1, jobs.end(),
     [](const Job& a, const Job& b) {
         return a.end < b.end;
     });

vector<int> dp(n + 1, 0);
for (int i = 1; i <= n; ++i) {
    auto it = upper_bound(
        jobs.begin() + 1, jobs.begin() + i, jobs[i].start,
        [](int start, const Job& job) {
            return start < job.end;
        }
    );

    int j = static_cast<int>(it - jobs.begin()) - 1;
    dp[i] = max(dp[i-1], dp[j] + jobs[i].profit);
}
return dp[n];
```

不選 `i` 時，保留前一個 prefix optimum；選 `i` 時，把它的 value 加到最佳相容 prefix。尋找最後一個 eligible index，才能保留所有可能的相容 predecessors，包括 end time 相同的工作。

## Pitfalls
- 把 start-time sorting 與 prefix state 混用，可能讓 `dp[j]` 選到一個較早開始、但尚未結束的長工作，即使工作 `j` 本身與目前工作相容。
- 找到第一個 eligible predecessor 會排除後續仍合法的選擇。應找最後一個 end time 小於等於目前 start time 的工作。
- 端點相等是否相容由題目定義。若允許前後相接，predecessor 條件是 `end <= start`，可使用 `upper_bound(start) - 1`。
- 目前 interval 只是候選，不是必選。因為永遠能略過它，prefix optimum 不會下降。
- `upper_bound` 回傳第一個 end time 嚴格大於 target 的位置，也就是相容 prefix 的下一格。
- 自訂 comparator 的參數順序不同：`lower_bound` 使用 `comp(element, target)`；`upper_bound` 使用 `comp(target, element)`。
- sentinel 只有在排序後確實位於所有真實 intervals 前面時，才能安全簡化 index；沒有 sentinel 時，必須明確處理空的相容 prefix。
- 每個 interval 都掃描所有 predecessors 會是 O(n^2)；binary search 能成立，是因為排序後的 compatibility boundary 具有單調性。

---

## Problems

### [[1235] Maximum Profit in Job Scheduling](../../problems/dp/maximum_profit_in_job_scheduling.md)
**Complexity:** Time O(n log n), Space O(n)
- **Trigger:** 從最多 50000 個 jobs 中選出 profit 最大的 non-overlapping subset。
- **Insight:** 依 end time 排序，比較略過目前工作與把它接在最佳相容 prefix 後方。
- **Pitfall:** 只有一個 predecessor 相容還不夠；必須保證 DP 的整個 candidate prefix 都相容，因此要找 end time 小於等於 start time 的最後一個工作。
