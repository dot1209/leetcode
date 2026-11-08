# [300] Longest Increasing Subsequence
**Pattern:** [Greedy](../../patterns/greedy.md)
**Complexity:** Time O(n log n), Space O(n)
**Link:** https://leetcode.com/problems/longest-increasing-subsequence/

## Trigger Signals

- 給定一個陣列，求**嚴格遞增** Subsequence 的最長長度；元素可以跳過，但原始順序不可改變。
- 除了 O(n²) DP，也要找 O(n log n) 的解法。
- 對於**相同長度**的遞增子序列，結尾越小，越容易接上未來的元素。這是 Greedy 的關鍵 Dominance。

## Core Insight

先前的思考是：「盡量挑小的數字放在前面，才容易讓 LIS 延伸」。但只維護**一條**目前選中的 subsequence 不夠；遇到較小的新數字時，可能需要替換中間位置，而且替換後各位置不一定來自同一條真實的 subsequence。

改成維護各個長度的「最小結尾」：

> 掃描到目前位置時，`tails[k]` 是所有**長度恰好為 `k+1`** 的合法嚴格遞增子序列中，**最後一個元素的最小值**。

例如掃過 `[1, 4, 8, 10, 6]`：

| 長度 | `tails` 值 | 可以作為證據的合法 subsequence |
|---|---:|---|
| 1 | 1 | `[1]` |
| 2 | 4 | `[1,4]` |
| 3 | 6 | `[1,4,6]` |
| 4 | 10 | `[1,4,8,10]` |

所以 `tails = [1,4,6,10]` **本身不是**原陣列的合法 subsequence，因為 `10` 比 `6` 早出現；但它的每個位置都對應一條**實際存在的**合法 subsequence。

### 更新規則

對每個新數字 `x`：

1. 若 `tails` 為空，或 `x > tails.back()`：`push_back(x)`，可以形成更長的 subsequence。
2. 否則，找出**第一個 `tails[k] >= x`** 的位置，以 `x` 取代它：改善長度 `k+1` 的最小結尾，但長度不變。

`tails` 沿著 `k` **嚴格遞增**，因此可以用 `lower_bound` 找替換位置。

- **不同 `k` 之間：** `tails[0] < tails[1] < ...`。
- **同一個 `k` 隨時間：** `tails[k]` 只會維持不變或變小，**不會變大**。
- `tails.size()` 只會增加，不會減少。

例子：

| Incoming `x` | 更新後 `tails` | 行為 |
|---|---|---|
| 1 | `[1]` | 新增 |
| 4 | `[1,4]` | 新增 |
| 8 | `[1,4,8]` | 新增 |
| 10 | `[1,4,8,10]` | 新增 |
| 6 | `[1,4,6,10]` | 替換**中間**的 8 |
| 11 | `[1,4,6,10,11]` | 新增，長度 5 |

最後一列的 `tails` 仍不是合法的 subsequence，但 `[1,4,8,10,11]` 是合法長度 5 的 witness。

## Why It's Correct

### Invariant：每一個最小結尾，都有實際 subsequence 作為證據

掃描完任意前綴之後，`tails[k]` 恰好是該前綴中，所有長度為 `k+1` 的嚴格遞增子序列的最小結尾。這個 invariant 包含兩件事：**至少有一條真的存在**，且**沒有結尾更小的同長度候選**。

若 `lower_bound(x)` 回傳位置 `k`，則：

- `k == 0`：單一元素 `[x]` 本身就是長度 1 的合法 subsequence。
- `k > 0`：因為 `tails[k-1] < x`，先前必有一條長度為 `k`、結尾是 `tails[k-1]` 的合法 subsequence。`x` 在掃描順序上較晚出現，因此可以接上去，得到長度 `k+1` 的合法 subsequence。
- 若 `k == tails.size()`，則新增一個更長的可行長度；否則把該長度原本的結尾改善成 `x`，不會傷害其他長度的候選。

更新的位置是 `lower_bound` 的第一個 `>= x`，所以 `k` 之前的最小結尾都 `< x`；`k` 之後原本都 `> tails[k] >= x`。因此替換後仍嚴格遞增。

### 兩個方向證明 `tails.size() == LIS`

設真正的 LIS 長度為 `L`。

**① 不會高估：`tails.size() <= L`（Soundness）**

只要 `tails` 有長度 `r`，就一定有一條長度 `r` 的合法遞增子序列，因為新增與替換都維持前述 witness invariant。所以 `tails.size()` 不可能比真正的 LIS 更長。

**② 不會低估：`tails.size() >= L`（Completeness）**

取任意一條真正存在的 LIS：

\[
a_1 < a_2 < \dots < a_L
\]

按這些元素在原陣列中的出現順序歸納，處理完 `a_r` 時，都能保證：

\[
tails[r-1] \le a_r
\]

- **Base：** 處理 `a_1` 後，長度 1 一定可達成，且其最小結尾 `tails[0] <= a_1`。
- **Induction：** 處理 `a_r` 前，因為已看過 `a_{r-1}`，而同一格 `tails[r-2]` 只會變小，有 `tails[r-2] <= a_{r-1} < a_r`。因此 `a_r` 一定能接在某條長度 `r-1` 的合法 subsequence 後面，讓長度 `r` 可達成，且 `tails[r-1] <= a_r`。

所以處理完 `a_L`，至少能維護長度 `L` 的候選。

結合兩個方向：

\[
\boxed{tails.size()=LIS}
\]

**English interview explanation：**

> `tails[k]` stores the minimum possible ending value among all increasing subsequences of length `k+1` seen so far. A smaller tail dominates a larger one of the same length because it leaves at least as many options for future extension. Each tail is witnessed by a valid subsequence, so we never overestimate the LIS. Conversely, along any actual LIS, the minimum tail for each prefix length is no larger than that LIS element, so the algorithm can always reach its full length. The tails array is sorted, which lets us locate the first tail greater than or equal to the new value with binary search.

## Complexity Analysis

令 `n = nums.size()`，`u` 為不同數值的個數。

| 解法 | Time | Auxiliary Space |
|---|---|---|
| Sorting + LCS（2D DP） | O(n log n + n·u)，最壞 O(n²) | O(n·u + n)，最壞 O(n²) |
| Sorting + LCS（1D DP） | O(n log n + n·u)，最壞 O(n²) | O(n + u) = O(n) |
| Greedy + Binary Search | **O(n log n)** | **O(n)** |

Greedy 版本掃描每個元素一次，`tails` 最多有 `n` 個元素。每次 `lower_bound` 是 O(log n)，替換或 `push_back` 的攤銷成本是 O(1)，因此總時間 O(n log n)、額外空間 O(n)。

注意 LCS Rolling 版本雖然 DP 表只剩 O(u)，仍然需要複製並排序一份長度 n 的 `sorted`，所以**整體**空間是 O(n)。

## Solution Code

### 寫法 1 — Greedy + Binary Search（最終 AC，原始碼保留）

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tails;
        for (auto x: nums) {
            if (tails.empty() || x > tails.back()) {
                tails.push_back(x);
                continue;
            }
            auto it = lower_bound(tails.begin(), tails.end(), x);
            *it = x;
        }
        return tails.size();
    }
};
```

### 寫法 2 — Sort + Unique + LCS（2D DP，原始 AC 版本）

先將另一份輸入排序、去重，得到嚴格遞增的 `sorted`。LIS 必定是 `nums` 和 `sorted` 的 Common Subsequence；反過來，任何 Common Subsequence 都因為 `sorted` 嚴格遞增，而是一條合法 LIS 候選。所以 `LIS(nums) == LCS(nums, sorted_unique(nums))`。

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> sorted = nums;
        sort(sorted.begin(), sorted.end());
        sorted.erase(std::unique(sorted.begin(), sorted.end()), sorted.end());

        // compute LCS(nums, sorted)
        // [0, 1, 0, 3, 2, 3]
        // [0, 1, 2, 3]
        int m = nums.size();
        int n = sorted.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (nums[i - 1] == sorted[j - 1]) {
                    dp[i][j] = max(dp[i][j], dp[i - 1][j - 1]) + 1;
                }
                else {
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        return dp[m][n];
    }
};
```

### 寫法 3 — Sort + Unique + LCS（1D Rolling DP，原始 AC 版本）

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> sorted = nums;
        sort(sorted.begin(), sorted.end());
        sorted.erase(std::unique(sorted.begin(), sorted.end()), sorted.end());

        // compute LCS(nums, sorted)
        // [0, 1, 0, 3, 2, 3]
        // [0, 1, 2, 3]
        int m = nums.size();
        int n = sorted.size();
        // remove layer i
        vector<int> dp(n + 1, 0);
        for (int i = 1; i <= m; i++) {
            // init for dp[0][0]
            int diag = dp[0];
            for (int j = 1; j <= n; j++) {
                int old = dp[j];
                if (nums[i - 1] == sorted[j - 1]) {
                    dp[j] = dp[j-1] + 1;
                }
                else {
                    dp[j] = max(dp[j], dp[j-1]);
                }
                // old become new diag after j++
                diag = old;
            }
        }
        return dp[n];
    }
};
```

## Alternatives / Optimization

### 一般 LCS 的 Rolling Transition（修正觀念，非本人原碼）

你的 1D AC 版本在 match 時用了 `dp[j-1] + 1`，而 `diag` 實際上未參與計算。**這在此題可以 AC，是因為 `sorted` 已去重**：每一列 `nums[i-1]` 最多只會與 `sorted` 中的一個位置匹配，所以到達 match 之前，這一列的 `dp[j-1]` 恰好等於上一列的對角線值。

但這不能直接套在**一般 LCS**。例如 `A = [1]`、`B = [1,1]`，錯誤地用已更新的 `dp[j-1] + 1` 會得到 2，正確 LCS 是 1。

一般 LCS 應保留舊的左上對角值：

```cpp
vector<int> dp(n + 1, 0);
for (int i = 1; i <= m; ++i) {
    int diag = 0;  // Previous row, previous column.
    for (int j = 1; j <= n; ++j) {
        int old = dp[j];  // Previous row, same column.
        if (nums[i - 1] == sorted[j - 1]) {
            dp[j] = diag + 1;
        } else {
            dp[j] = max(dp[j], dp[j - 1]);
        }
        diag = old;  // Diagonal value needed by the next column.
    }
}
```

在每次更新前：

| 狀態 | 一維存放位置 |
|---|---|
| `dp[i-1][j]`（上方） | `dp[j]` 的舊值 |
| `dp[i][j-1]`（左方） | `dp[j-1]` 的新值 |
| `dp[i-1][j-1]`（左上） | `diag` |

必須由左往右更新，才能直接取得本列的 `dp[i][j-1]`；而舊對角值在被覆蓋前，要用一個變數接住。

## Pitfalls

- **`tails` 不一定是一條合法 LIS。** 例如 `[1,4,8,10,6]` 產生 `[1,4,6,10]`；`6` 在原陣列出現於 `10` 後面，兩者不能組成這個順序的 subsequence。正確的是每個 `tails[k]` **各自**有一條合法 witness。
- **嚴格遞增必須用 `lower_bound`，不是 `upper_bound`。** 要找第一個 `>= x` 的位置；同值應該替換，不能當作變長。例 `[2,2,2]` 的答案是 1，不是 3。
- **替換不限於尾端。** 例如 `tails = [1,4,8,10]`、`x = 6`，替換的是 index 2 的 `8`，不是 `10`。`tails` 是不同長度的最佳結尾，不是一條必須保持原位置順序的完整路徑。
- **不要把兩種單調性混淆。** `tails` 沿 index 嚴格增加，但同一個 `tails[k]` 隨掃描只會降低或維持不變。
- **一般 LCS match 必須讀舊對角線。** 一維 DP 中的 `dp[j-1]` 已更新成目前列，不能當作上一列左上的值；本題去重後才有特殊等價。
- **LCS 轉換必須先去重。** 若 `sorted = [1,1,2]` 保留重複值，LCS 可能選到重複元素而不符合 LIS 的 strict increasing。
- **Sorting + LCS 空間分析別漏掉 `sorted`。** 即使 DP 壓到一列，也還有長度 O(n) 的複製陣列。
- **`std::unique` 不會縮短 vector。** 它只把相鄰相同元素壓到前面，回傳有效前綴的 past-the-end iterator，再用 `erase(it, end())` 刪掉剩餘尾段。

## Side Notes

### `std::unique` 和半開 `erase`

```cpp
sort(sorted.begin(), sorted.end());
auto it = unique(sorted.begin(), sorted.end());
sorted.erase(it, sorted.end());
```

`it` 指向**保留下來的有效前綴之後的第一個位置**，不是最後一個唯一元素。`erase(it, end())` 刪除半開範圍 `[it, end())`。

### `lower_bound` 回傳的是 Iterator

`lower_bound(tails.begin(), tails.end(), x)` 回傳第一個滿足 `*it >= x` 的位置。如果所有元素都小於 `x`，回傳 `tails.end()`；你的程式已先以 `x > tails.back()` 分支處理這種情況，所以剩下的分支可以安全地 `*it = x`。

## Follow-ups

- **回傳 LIS 實際元素，而不只是長度：** `tails` 的內容不一定是合法 subsequence，因此不能直接回傳 `tails`。需要額外紀錄各長度結尾的原始 index，以及每個元素的 predecessor，再從最後一個 index 反向重建；仍可做到 O(n log n) 時間、O(n) 空間。
- **Longest Non-decreasing Subsequence：** 如果允許相等，延伸條件改成 `x >= tails.back()`，替換位置改為第一個 `> x`，也就是 `upper_bound`。

## Related Problems

- [1143] Longest Common Subsequence — 對照本題的 Sort + Unique + LCS 轉換，以及一般 LCS 的 Rolling Transition。
- [354] Russian Doll Envelopes — 排序一個維度後，對另一維做 LIS；須小心相同第一維的排序方向。
- [673] Number of Longest Increasing Subsequence — 不只問長度，還要計數；單純的 `tails` 不足以保存方案數。
- [1964] Find the Longest Valid Obstacle Course at Each Position — Non-decreasing 版本，改用 `upper_bound`。