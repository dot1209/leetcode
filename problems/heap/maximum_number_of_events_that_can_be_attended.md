# [1353] Maximum Number of Events That Can Be Attended
**Pattern:** [Heap / Priority Queue](../../patterns/heap.md)
**Complexity:** Time O(N log N), Space O(N)
**Link:** https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/

## Trigger Signals
- `[startDay, endDay]` 是可選的日期範圍，兩端都包含。每個活動只需選其中一天，每天最多參加一個，每個活動最多參加一次。
- 區間重疊仍可安排在不同天。例如三個 `[1,3]` 可以分別安排在第 1、2、3 天。看到 interval 時，先確認活動占用整段時間，還是只占區間內一格。
- 每天都有新的活動開始，舊活動也可能過期。要反覆從「今天還能參加的活動」取出最早結束的一個，適合用 min-heap 維護動態候選。

## Core Insight
「依 `startDay` 排序，把 `endDay` 丟進 priority queue」是兩個不同的決策：**開始日決定何時加入候選，結束日決定今天先選誰。** 在今天已開始、尚未過期且尚未參加的活動中，優先選最早到期的活動。

`i` 指向下一筆尚未加入 heap 的活動。一天的流程是：

1. 把今天開始的活動全部放入 heap。
2. 持續移除 `endDay < day` 的過期活動。`endDay == day` 仍可參加。
3. 若 heap 還有活動，取出最小的 `endDay`，參加一次並累加答案。
4. 若 heap 已空且還有未加入的活動，跳到下一筆的 `startDay`；否則前進一天。

清掉過期活動後，heap 恰好包含今天可以參加的未選活動。`i == N` 只代表所有活動都已加入，仍要處理 heap 裡剩下的活動。heap 空時，下一筆活動的開始日前沒有候選，因此可以跳過這段空檔。

### 用原本卡住的測資走一次

`[[1,4],[4,4],[2,2],[3,4],[1,1]]` 排序後是 `[[1,1],[1,4],[2,2],[3,4],[4,4]]`。所有活動都只能在第 1～4 天參加，答案最多是 4。

| 日期 | 清掉過期活動後的候選結束日 | 動作 | 累計 |
|---|---|---|---|
| 1 | `1, 4` | 參加結束日為 1 的活動 | 1 |
| 2 | `2, 4` | 參加結束日為 2 的活動 | 2 |
| 3 | `4, 4` | 參加其中一個 | 3 |
| 4 | `4, 4` | 參加其中一個 | 4 |
| 5 | 無 | 移除剩下的過期活動 | 4 |

## Why It's Correct
### Exchange Argument：選最早到期的候選

假設有一個最佳排程，已經和貪心在今天 `d` 之前的決策一致。貪心今天選 A。若最佳排程也選 A，就可直接保留。其他情況如下：

- **最佳排程今天選 B，且沒安排 A：** 把今天的 B 替換成 A，其他日期不用改，參加總數相同。
- **最佳排程在第 `d` 天參加 B，在較晚的第 `t` 天參加 A。** 交換兩個活動的日期：A 本來就是第 `d` 天的候選，所以可以提前到 `d`。B 原本能在 `d` 參加，因此到 `t` 時早已開始（`startB <= d < t`）。又因為 A 原本能在 `t` 參加，且貪心選的是今天最早到期的候選，所以 `t <= endA <= endB`，B 到 `t` 時也還沒過期。交換後，兩個活動都能參加，總數不變。
- **最佳排程今天沒安排活動：** 若 A 在之後某天，將它移到今天即可；若 A 沒被安排，今天可多參加一個，和最佳排程的假設矛盾。

每一步都能得到一個與貪心前綴一致的最佳排程，因此今天選 A 不會降低最後的總數。`endA == endB` 也能交換：相同的是最後期限，交換的是兩個不同的參加日期。

## Complexity Analysis
- **Time O(N log N)：** 排序 O(N log N)。每個活動最多進 heap 一次、離開一次，所有 heap 操作合計 O(N log N)。
- **跳日的作用：** 外層每輪至少取出一筆活動，可能是參加一個有效活動，也可能只清掉過期活動。heap 空且還有活動時直接跳到下一個開始日，下一輪必有活動加入並取出。因此外層輪數由活動數 `N` 限制。若改成逐天掃到最大結束日 `D`，則要另外算 O(D)，總時間為 O(N log N + D)。
- **Auxiliary Space O(N)：** 同一天可能有 N 個活動開始，heap 最多容納 N 筆結束日。

## Solution Code
### 寫法 1 — 使用者的 AC 版本（原樣保留）

掃描日期、用 min-heap 選最早到期的活動。heap 空時跳日，時間不依賴日期值域。

```cpp
class Solution {
public:
    int maxEvents(vector<vector<int>>& events) {
        sort(events.begin(), events.end(),
             [](const vector<int>& a, const vector<int>& b) {
                 if (a[0] == b[0]) {
                     return a[1] < b[1];
                 }
                 return a[0] < b[0];
             });
        priority_queue<int, vector<int>, greater<int>> pq;
        int day = events[0][0];
        int i = 0;
        int res = 0;
        // [[1,1], [1,4], [2,2], [3,4], [4,4]]
        while (i < events.size() || pq.size()) {
            while (i < events.size() && day == events[i][0]) {
                pq.push(events[i][1]);
                i++;
            }
            // pop outdated events
            while (pq.size() && pq.top() < day) {
                pq.pop();
            }
            if (pq.size()) {
                pq.pop();
                res++;
            }
            // jump to next start event
            if (pq.empty() && i < events.size()) {
                day = events[i][0];
            }
            else {
                day++;
            }
        }
        return res;
    }
};
```

### 寫法 2 — 補充：依 endDay 排序 + ordered set

沿用「每個活動找最早未使用日」的原始想法。`set::lower_bound` 直接找第一個不早於 `startDay` 的空日，代價是要儲存日期值域。

```cpp
class Solution {
public:
    int maxEvents(vector<vector<int>>& events) {
        sort(events.begin(), events.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });
        const int lastDay = events.back()[1];

        set<int> freeDays;
        for (int day = 1; day <= lastDay; ++day) {
            freeDays.emplace_hint(freeDays.end(), day);
        }

        int res = 0;
        for (const auto& event : events) {
            auto it = freeDays.lower_bound(event[0]);
            if (it != freeDays.end() && *it <= event[1]) {
                freeDays.erase(it);
                ++res;
            }
        }
        return res;
    }
};
```

### 寫法 3 — 補充：依 endDay 排序 + Fenwick Tree + 二分

保留日期陣列的概念，用可更新的區間空日數把查詢變成單調判斷。適合練習從「單點狀態」改成「前綴是否已存在答案」。

```cpp
class Solution {
public:
    int maxEvents(vector<vector<int>>& events) {
        sort(events.begin(), events.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });
        const int lastDay = events.back()[1];

        // Every day starts free. Each bucket contains lowbit(day) ones.
        vector<int> bit(lastDay + 1);
        for (int day = 1; day <= lastDay; ++day) {
            bit[day] = day & -day;
        }

        auto prefixFree = [&](int day) {
            int count = 0;
            for (; day > 0; day -= day & -day) {
                count += bit[day];
            }
            return count;
        };

        int res = 0;
        for (const auto& event : events) {
            const int before = prefixFree(event[0] - 1);
            if (prefixFree(event[1]) == before) {
                continue;
            }

            int left = event[0], right = event[1];
            while (left < right) {
                const int mid = left + (right - left) / 2;
                if (prefixFree(mid) > before) {
                    right = mid;
                } else {
                    left = mid + 1;
                }
            }

            for (int day = left; day <= lastDay; day += day & -day) {
                --bit[day];
            }
            ++res;
        }
        return res;
    }
};
```

## Alternatives / Optimization
### Heap 版的可讀性

`vector<int>` 的字典序會先比較 `startDay`，相同再比較 `endDay`，所以可以直接用 `sort(events.begin(), events.end())`。用 `!pq.empty()` 表達非空也比把 `pq.size()` 當布林值直觀。

可以將「heap 空就跳到下一個 `startDay`」移到迴圈開頭，然後依序加入候選、清過期、參加活動。此時若進入外層且 heap 空，`i < N || !pq.empty()` 可推出 `i < N`，所以讀取 `events[i]` 安全。只有成功參加才遞增 `day`；若清完過期活動後沒有候選，下一輪會跳日或結束。這些整理不改變複雜度。

### 為什麼依結束日處理也成立

固定已處理活動的安排，處理下一個最早到期的 E。令 `d` 是 E 範圍內最早空日。如果最佳排程原本把 E 放在 `t`，則 `d <= t`。若另一個未處理活動 F 原本占用 `d`，可以把 E 放在 `d`，F 移到 `t`：F 在 `d` 已開始，且 `t <= endE <= endF`。如果最佳排程未選 E，則用 E 替換 `d` 的活動，總數不變；若 `d` 也是空的，就能多排一個，和最佳性矛盾。找不到空日則可跳過 E，因為固定的安排已占滿 E 的範圍。

這個策略允許分配的日期往回。例如先處理 `[2,2]`，再處理兩個 `[1,3]`，會依序選日期 2、1、3。`set` 保留前面空下來的第 1 天。排序成本 O(N log N)，每個活動的查找與移除至多 O(log D)。程式按升序使用 `emplace_hint(end(), ...)`，新元素都插在提示位置前方，初始化為 O(D)。總時間為 O(N log N + D + N log D)，日期集合空間 O(D)，另有排序的堆疊空間。

### 二分的關鍵是單調判斷

`used[mid]` 只回答單一天。改問 `prefixFree(mid) - prefixFree(startDay - 1) > 0`，也就是 `[startDay, mid]` 是否有空日。擴大 `mid` 不會讓區間內的空日變少，所以答案只會從 `false` 變成 `true`。先檢查整個活動區間是否有空日，再找第一個成立的位置。

每次選用一天都需要更新空日狀態，Fenwick Tree 的單點更新與前綴計數各為 O(log D)。外層二分需要 O(log D) 次查詢，每筆活動花 O(log² D)，總時間 O(N log N + D + N log² D)。Fenwick Tree 使用 O(D) 空間，另有排序的堆疊空間。若只是要找下一個可用日期，`set::lower_bound` 的實作較短。

## Pitfalls
- **誤讀成選最多個互不重疊的區間。** 活動只占一天，不能用 `total - overlapped`。原練習範例中五個活動都在第 1～4 天，正確答案是 4。
- **依結束日排序後只用一個遞增的 `day`。** `[2,2]`、`[1,3]`、`[1,3]` 若排完第 2 天就往後走，會漏掉第 1 天。日期有洞，需要查詢空日的結構；若每次從 `startDay` 重掃，N 個 `[1,N]` 要檢查 `1 + 2 + ... + N` 次，為 O(N²)。
- **直接二分 `used` 陣列。** 若第 1～3 天為 `false, true, false`，從第 2 天看到 `true` 就往右，會跳過第 1 天。占用狀態本身沒有單調性。
- **把一輪當成一個活動，而非一天。** `if` 只加入一個活動，接著跳到同一開始日，會在一天內計數兩次。要用 `while` 先加入當天全部活動，再選一個。
- **只用 `i < N` 結束迴圈。** 兩個 `[1,2]` 在第 1 天就全入 heap，但第二個仍可在第 2 天參加。外層要用 `i < N || !pq.empty()`。
- **越界或讀取空 heap。** 早期 runtime error 是跳日讀 `events[i][0]` 前漏掉 `i < N`。用短路順序保護存取，例如 `i < N && events[i][0] == day`、`!pq.empty() && pq.top() < day`。題目保證至少有一個活動，所以原 AC 版的 `events[0]` 安全。
- **清除過期與參加混在一起。** 第 2 天的 heap 若有結束日 `1, 1, 3`，要在同一天清掉兩個 `1`，再參加 `3`。清過期不消耗一天，也不增加答案。
- **把 `<= day` 當成加入活動的必要條件。** `<=` 表達已開始，`==` 表達今天開始。這個流程每天加入全部同日起始活動，跳日時只跳到下一筆未加入的開始日，所以不會漏掉開始日，`==` 已足夠。

## Side Notes
### 怎麼決定 sort on start day 或 end day

先問「我要按什麼順序看到候選？」再問「在候選裡要優先取誰？」排序鍵、取用的優先順序可以不同。

| 問題 | 排序方式 | 排序的用途 |
|---|---|---|
| LC 56 合併區間 | start | 讓下個區間的起點依序出現，判斷能否接到目前的合併區間 |
| 選最多個互不重疊的完整區間 | end | 先完成早結束的區間，留下更多後續時間 |
| LC 1353 每天選活動 | start + min-heap of end | 依開始日加入候選，在候選中挑最早到期的 |
| LC 1353 每個活動選日期 | end + 空日集合 | 先處理較早到期的活動，再找區間內最早空日 |
| LC 1235 有權重的區間排程 | end + DP | 將相容的前置活動整理成可二分的前綴，由 DP 比較取與不取 |

### C++ priority_queue

`priority_queue<int>` 預設是 max-heap；`priority_queue<int, vector<int>, greater<int>>` 是 min-heap。`top()` 取極值，`pop()` 移除極值且不回傳數值。若活動的選擇與後續判斷只用到 `endDay`，heap 裡存一個 `int` 就夠了。

## Follow-ups
- [1751] Maximum Number of Events That Can Be Attended II — 題名相近，但活動要占用整段日期，並有價值與最多參加 `k` 個的限制。改用區間相容性、二分搜尋與 DP，比較跳過或選取活動；不能沿用每天選最早到期活動的交換論證。

## Related Problems
- [[621] Task Scheduler](task_scheduler.md) — 另一種動態候選排程，heap 的優先順序改為剩餘次數，並受冷卻時間限制。
- [1834] Single-Threaded CPU — 依開始可執行的時間加入候選，再用另一個優先順序取工作；沒有候選時同樣可以跳時間。
- [1851] Minimum Interval to Include Each Query — 依起點加入區間，查詢時從 heap 排除過期候選，取長度最短的有效區間。
- [[1235] Maximum Profit in Job Scheduling](../dp/maximum_profit_in_job_scheduling.md) — 比較整段時間占用、有權重的排程，理解排序後的相容性查詢何時要搭配 DP。
