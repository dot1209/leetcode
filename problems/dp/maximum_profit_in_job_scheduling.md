# [1235] Maximum Profit in Job Scheduling
**Pattern:** [DP → Weighted Interval Scheduling](../../patterns/dp/weighted-interval-scheduling.md)
**Complexity:** Time O(n log n), Space O(n)
**Link:** https://leetcode.com/problems/maximum-profit-in-job-scheduling/

## Trigger Signals
- 每個工作都有開始時間、結束時間與報酬，要選出一組工作。
- 選到的工作不能重疊；在時間 `t` 結束的工作，可以立刻接上同樣在 `t` 開始的工作。
- `n <= 50000`，不能在每次轉移時掃過前面所有工作。時間最大可到 `10^9`，所以 DP 應以工作為索引，而不是替每個時間點建立狀態。

## Core Insight
定義 `dp[i]` 為「前 `i` 個 project（包含 `i` 在候選集合內）能得到的最大 profit」。這不代表一定要選第 `i` 個 project。整張表完成後，`dp[n]` 就是答案。

先依照 `endTime` 由小到大排序。處理工作 `i` 時，比較「不選 `i`」與「選 `i`」。如果要選 `i`，就往前找最後一個滿足 `endTime[j] <= startTime[i]` 的工作 `j`：

```cpp
dp[i] = max(dp[i-1], dp[j] + tasks[i].profit);
```

索引 `0` 放一個 profit 為零的 guard。沒有相容的真實工作時，`j = 0`。`upper_bound` 會找到第一個 end time 嚴格大於目前 start time 的位置，因此它的前一個位置就是最後一個相容工作。

### 最後的推導如何串起來
原本的思路會先檢查前一個工作是否重疊：

- 如果 `endTime[i-1] <= startTime[i]`，由於工作已依 end time 排序，更前面的工作也都已經結束，因此可以把 `profit[i]` 加到 `dp[i-1]`。
- 否則，往前找結束後能接上 `i` 的最後一個工作，並比較選 `i` 與保留 `dp[i-1]`。
- 依 end time 排序後，相容工作的分界具有單調性，因此可以用 binary search 取代 O(n) 掃描。

提交版本中的兩個 branch 是正確的，也可以統一寫成上面的 recurrence。

## Why It's Correct
排序不只保證工作 `j` 本身與 `i` 相容，還保證整個 prefix 都與 `i` 相容。對所有 `k <= j`：

```text
endTime[k] <= endTime[j] <= startTime[i].
```

因此，`dp[j]` 所代表的任何可行工作組合，後面都能接上工作 `i`。

前 `i` 個工作中的最佳排程只有兩種情況：

- 不選 `i`，最佳值是 `dp[i-1]`。
- 選 `i`，先前選到的工作都必須位於相容 prefix `1..j` 中，最佳值是 `dp[j] + profit[i]`。

兩種選擇都可實現，取最大值就得到最佳解。從 `dp[0] = 0` 開始，可以依序證明每個狀態都正確，因此 `dp[n]` 也是正確答案。

## Complexity Analysis
- **Time O(n log n)：** 建立 `n` 筆工作需要 O(n)，排序需要 O(n log n)，接著處理 `n` 個狀態，每個狀態最多做一次 O(log n) 的 predecessor search。原本的條件分支在前一個工作相容時可以省略 binary search。
- **Space O(n)：** jobs 與 DP table 都有 O(n) 個元素。`dp[j]` 可能離 `i` 很遠，所以這個 recurrence 不能只保留前一個 DP 值。
- 如果每個狀態都向前線性掃描 predecessor，整體會退化成 O(n^2)。
- 題目限制下，總 profit 最大為 `50000 * 10000 = 500000000`，`int` 足夠使用。

## Solution Code
### Accepted solution — 原樣保留
以下是通過的實作，保留原本的條件轉移、命名、索引與手推範例。

```cpp
class Solution {
public:
    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        vector<Task> tasks(n+1);
        tasks[0] = Task{0, 0, 0};
        for (int i = 1; i <= n; i++) {
            tasks[i] = Task{startTime[i-1], endTime[i-1], profit[i-1]};
        }
        sort(tasks.begin(), tasks.end(), [](Task& a, Task& b){
            return a.endTime < b.endTime;
        });

        // define dp[i]: max profit of first i tasks
        vector<int> dp(n+1, 0);
        for (int i = 1; i <= n; i++) {
            // overlapped
            if (tasks[i].startTime < tasks[i-1].endTime) {
                auto it = upper_bound(tasks.begin(), tasks.end(), tasks[i].startTime, [](int start, Task& a){
                    return start < a.endTime;
                });
                int j = distance(tasks.begin(), it)-1;
                dp[i] = max(dp[j] + tasks[i].profit, dp[i-1]);
            }
            else {
                dp[i] = dp[i-1] + tasks[i].profit;
            }
        }
        return dp[n];
    }
private:
    struct Task {
        int startTime;
        int endTime;
        int profit;
    };
};
/*
[0,1,2,4,6,3]
[0,3,5,6,9,10]
[0,20,20,70,60,100]
[0,20,20,90,150,150]
*/
```

## Alternatives / Optimization
### 統一 transition
這只是可讀性調整，時間仍是 O(n log n)，空間仍是 O(n)，不會取代上方原始 AC code。

保留原本的 guard 與 `Task` 結構，只把 DP loop 改成：

```cpp
for (int i = 1; i <= n; ++i) {
    auto it = upper_bound(
        tasks.begin(), tasks.begin() + i, tasks[i].startTime,
        [](int start, const Task& task) {
            return start < task.endTime;
        }
    );

    int j = static_cast<int>(it - tasks.begin()) - 1;
    dp[i] = max(dp[i-1], dp[j] + tasks[i].profit);
}
```

當工作 `i-1` 與 `i` 相容時，`j` 就是 `i-1`。由於 profit 都是正數，選取分支自然會得到 `dp[i-1] + profit[i]`，因此不需要另外判斷是否重疊。把搜尋範圍限制在 `[begin(), begin() + i)`，也能清楚表達只能依賴前面的工作。

原本搜尋整個 vector 仍然正確：工作 `i` 本身一定滿足 `endTime[i] > startTime[i]`，所以第一個大於 start time 的 end time 最晚出現在索引 `i`，因此 `j < i`。時間為零的 guard 則保證 iterator 一定在 `begin()` 之後。

sort comparator 可改用 `[](const Task& a, const Task& b)`，更清楚表達比較時不會修改工作。

### 依 start time 排序搭配 suffix DP
依 start time 排序也可以，但 state 與 transition 必須改成朝向剩餘工作：

| 排序方式 | State | 相容分界 | 填表順序 |
|---|---|---|---|
| end time 遞增 | `dp[i]`：工作 `1..i` 的最大 profit | 最後一個 `end[j] <= start[i]` 的 `j` | `i` 遞增 |
| start time 遞增 | `dp[i]`：工作 `i..n` 的最大 profit | 第一個 `start[j] >= end[i]` 的 `j` | `i` 遞減 |

suffix 寫法以 `endTime[i]` 為 target，在已依 start time 排序的欄位中使用 `lower_bound`：

```cpp
// Suffix DP with start-time ordering and one-based job indices.
dp[i] = max(dp[i+1], tasks[i].profit + dp[j]);
```

另外配置 `dp[n+1] = 0`；如果找不到下一個工作，就令 `j = n+1`。因為 start time 已排序，從 `j` 開始的每個工作都會在 `i` 結束後才開始。`i+1` 與 `j` 都大於 `i`，所以必須反向填表，最後回傳 `dp[1]`。

搜尋的 target 與排序使用的欄位是不同概念：這裡是拿目前工作的 end time，去已排序的 start time 欄位中搜尋。

## Pitfalls
### start time 排序卻使用 prefix DP
只找到一個相容工作，不代表整個 `dp[j]` prefix 都相容。

| 工作（依 start time 排序） | Start | End | Profit |
|---|---:|---:|---:|
| A | 1 | 10 | 100 |
| B | 2 | 3 | 10 |
| C | 4 | 5 | 20 |

處理 C 時，B 與 C 相容，但 `dp[2] = 100` 選到的是 A。若直接加上 C，會錯誤得到 `120`，但 A 與 C 其實重疊。依 end time 排序，才能讓相容範圍形成完整 prefix；另一種做法是保留 start time 排序，但改成 suffix DP。

### 使用錯誤工作的時間進行搜尋
一開始曾拿前一個工作的 end time 當搜尋值。threshold 應該來自目前工作：

- prefix DP：拿 `startTime[i]` 搜尋 end time。
- suffix DP：拿 `endTime[i]` 搜尋 start time。

前一個工作只適合用來快速判斷整個前綴是否都相容。

### 把候選集合誤解成強制選擇
「前 `i` 個 project（包含 `i`）」是在描述考慮哪些工作，不代表一定要選 `i`。如果 state 定義成一定選 `i`，recurrence 與最後取答案的方式都會不同。

### 找到第一個相容 predecessor，而不是最後一個
end times 為 `[2, 4, 4, 7]`，目前 start time 為 `4` 時，前三個工作都屬於相容 prefix。若只取第一個相容 index，會無謂排除後面的可行選擇。需要的是最大的 `j`，使 `endTime[j] <= startTime[i]`。

### 漏掉端點剛好相等的工作
相容條件是 `endTime[j] <= startTime[i]`。使用嚴格小於 `<` 會排除合法的前後相接工作。`lower_bound(start) - 1` 找到的是最後一個 end time 嚴格小於 start 的工作，會漏掉相等的端點；應使用 `upper_bound(start) - 1`。

### 直接反轉 comparator，卻沒有維持 partition
曾嘗試在 `lower_bound` 使用 `task.endTime > target`。對遞增的 end-time sequence 而言，結果會是先 false、後 true，違反 `lower_bound` 要求的「true prefix、false suffix」。只有符合 partition 前提時，「找到第一個 false」的描述才成立；不符合時，搜尋結果不可靠。

### 寫反 upper_bound 的參數型別
`upper_bound` 會呼叫 `comp(target, element)`。如果 lambda 寫成 `(Task&, int)`，對 integer target 與 `Task` element 來說參數順序錯誤，無法編譯。正確形式是 `(int, const Task&)`，並比較 `target < task.endTime`。

### predecessor index 計算錯誤
- `upper_bound` 回傳第一個不相容位置，因此要減一才是最後一個相容工作。
- `distance(it, tasks.begin())` 的方向相反。對 vector iterator 可能得到負數，拿來存取 DP 會變成無效 index；應使用 `distance(tasks.begin(), it)`。
- 一般 predecessor search 中，`it == end()` 代表搜尋範圍內所有元素都小於等於 target，因此最後一個元素其實是有效 predecessor；它不代表「沒有 predecessor」。
- 只有在 upper-bound iterator 位於搜尋範圍的 `begin()` 之後，才能往前減一。本實作使用 `{0, 0, 0}` guard，而真實 start time 都是正數，所以一定安全。

### 讓 prefix optimum 下降
第一次手推的最後一格曾寫成 `120`：

```text
[0, 20, 20, 90, 150, 120]
```

最後一個工作為 `[3, 10]`、profit 為 `100`。選它會得到 `dp[1] + 100 = 120`，但不選它能保留 `dp[4] = 150`。正確結果是：

```text
[0, 20, 20, 90, 150, 150]
```

因為永遠可以不選新工作，所以 `dp[i] >= dp[i-1]`。直接回傳 `dp[n]` 即可；使用 `max_element` 反而可能掩蓋錯誤下降的 transition。

## Side Notes
### lower_bound 與 upper_bound
對一個使用相符 strict-less comparator 且遞增排序的 range：

| Function | 預設分界 | 自訂 comparator 的呼叫方式 | 找到的位置 |
|---|---|---|---|
| `lower_bound` | 第一個 `>= target` 的元素 | `comp(element, target)` | 第一個 `false` |
| `upper_bound` | 第一個 `> target` 的元素 | `comp(target, element)` | 第一個 `true` |

兩者都回傳 iterator；如果分界位於所有元素之後，會回傳 `end()`，不能對 `end()` 解參考。

對 `[2, 4, 4, 7]` 與 target `4`，`lower_bound` 指向 index `1`，`upper_bound` 指向 index `3`。`lower_bound` 預設找的是第一個 `>=`，不是 `<=`。

```cpp
// tasks is sorted by increasing endTime.
auto lo = lower_bound(
    tasks.begin(), tasks.end(), target,
    [](const Task& task, int value) {
        return task.endTime < value;
    }
);

auto hi = upper_bound(
    tasks.begin(), tasks.end(), target,
    [](int value, const Task& task) {
        return value < task.endTime;
    }
);
```

兩個 lambda 都是在表達「左參數小於右參數」，差別是 library 傳入參數的順序不同。target 是明確傳入的第三個參數，不是等拿到 iterator 後再從 iterator 讀出的欄位。

按照上面的參數順序，lower-bound comparisons 會形成 true prefix、false suffix；upper-bound comparisons 會形成 false prefix、true suffix。comparator 是在描述排序關係，不是一個任意的「這個元素是不是答案」判斷式。

### Iterator arithmetic 與 distance
對 vector 來說，`it - tasks.begin()` 與 `distance(tasks.begin(), it)` 都是 O(1)。如果不是 random-access iterator，`distance` 可能需要線性時間。

一般的「找最後一個小於等於 target」操作，在移到前一個元素前必須先檢查 `it != begin()`。這份解法透過 job-specific guard 處理邊界。guard 可以簡化索引，但它的時間必須能排在所有真實工作之前。

### vector of struct
`vector<Task>` 很適合這題，因為每個工作的 start、end 與 profit 本來就屬於同一筆資料。排序時三個欄位會一起移動；具名 member 也讓 comparator 容易閱讀；vector 還能支援 sort、binary search 與 random access。

題目介面雖然給三個 vector，把它們合成 record 後，排序時仍能維持三個欄位的對應關係。

### Struct 初始化：大括號與小括號
提交版本的 `Task` 沒有自訂 constructor，因此是 aggregate：

```cpp
struct Task {
    int startTime;
    int endTime;
    int profit;
};

Task a{1, 3, 50};  // Aggregate initialization works in C++17.
Task b(1, 3, 50);  // Parenthesized aggregate initialization needs C++20.
```

如果明確定義三參數 constructor，C++17 也能使用小括號形式。大括號也可能呼叫 constructor，不是看到大括號就一定是 aggregate initialization。

大括號會拒絕 narrowing conversion；小括號的 aggregate initialization 則允許一般 conversion：

```cpp
Task a{1.5, 3, 50};  // Ill-formed: double-to-int narrowing.
Task b(1.5, 3, 50);  // C++20: startTime becomes 1.
```

### Sort comparator 的規則
sort 必須使用 strict comparison，例如 `a.endTime < b.endTime`。改成 `<=` 不是合法 comparator。參數使用 `const Task&`，可以清楚表示比較時只讀取資料。

### References
- [C++ working draft：lower_bound](https://eel.is/c++draft/lower.bound)
- [C++ working draft：upper_bound](https://eel.is/c++draft/upper.bound)
- [P0960R3：parenthesized aggregate initialization](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0960r3.html)

## Related Problems
- [435] Non-overlapping Intervals：移除最少區間；可用來對照沒有權重時的 greedy 與有 profit 時的 DP。
- [1751] Maximum Number of Events That Can Be Attended II：限制最多能選幾個 event，因此除了 interval compatibility，還需要多一個 DP dimension。
