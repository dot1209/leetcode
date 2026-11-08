# [862] Shortest Subarray with Sum at Least K
**Pattern:** [Sliding Window](../../patterns/sliding-window.md)（Prefix Sum + Monotonic Deque）
**Complexity:** Time O(n), Space O(n)
**Link:** https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

## Trigger Signals
- 求 Sum ≥ k 的**最短非空連續 Subarray**，而 `nums` 可能有負數；普通 Sliding Window 的區間 Sum 不再隨左右端點移動而單調變化。
- 要在 O(n) 或 O(n log n) 內處理多個可能左端點；暴力枚舉所有 Subarray 是 O(n²)。
- 把區間 Sum 轉成 Prefix Sum 的差，並設法只保存未被支配的候選左界。

## Core Insight
定義 `prefix_sum[i] = sum(nums[0:i))`，因此 `prefix_sum[0] = 0`，區間 `[l, r)` 的 Sum 為 `prefix_sum[r] - prefix_sum[l]`。當固定 `r`，要從滿足 `prefix_sum[l] <= prefix_sum[r]-k` 的候選裡找**最大的 `l`**，因為 `r-l` 才會最短。

使用 `deque<int>` 保存 Prefix **Index**：Deque 裡的 Index 由小到大，而對應的 Prefix Sum 必須**嚴格遞增**。沿 Prefix Index `r=0..n` 掃描：

1. **`pop_back()` — Dominance：** 若 `prefix_sum[r] <= prefix_sum[dq.back()]`，新的 `r` 較晚且 Prefix Sum 較小或相等，比舊候選更有利。重複移除 Back，直到嚴格遞增，再 `push_back(r)`。
2. **`pop_front()` — Finalization：** 當 `prefix_sum[r] - prefix_sum[dq.front()] >= k`，先更新 `res = min(res, r-dq.front())`，再移除 Front。已結算的左端點未來只會形成更長的 Subarray。

兩種 Pop 的依據不同：**Back 是被新候選支配；Front 是這個候選已經得到最早的合法右界。**

## Why It's Correct
### Back：被支配的左界不用留
假設舊左界 `i < j`，新左界 `j` 滿足 `prefix_sum[j] <= prefix_sum[i]`。若未來 `t > j` 使舊左界合法，即 `prefix_sum[t]-prefix_sum[i] >= k`，則 `prefix_sum[t]-prefix_sum[j] >= prefix_sum[t]-prefix_sum[i] >= k`，而 `t-j < t-i`。所以新左界的合法性與長度都不比舊左界差。

本人的程式先 `pop_back()`、`push_back(r)`，才檢查目前右界 `r` 的合法區間；這樣仍安全，因為被 `r` 支配的舊左界 `i` 有 `prefix_sum[r]-prefix_sum[i] <= 0 < k`（`k > 0`），無法與目前 `r` 組成合法區間。

### Front：已結算的左界不用留
一旦對左界 `l` 找到合法右界 `r`，就把長度 `r-l` 納入答案。對任何更晚的右界 `t>r`，`t-l > r-l`，不會得到更短的區間，因此 `l` 可以永久淘汰。

### 為什麼只從 Front 檢查？
Deque 對應的 Prefix Sum 嚴格遞增。若某個後方候選在當前 `r` 已合法，排在它前面的 Prefix Sum 更小，必定也合法。因此可以持續從 Front 結算；當 Front 不合法，後面的候選也都不合法。搭配 Back 的 Dominance 淘汰，不會漏掉最佳解。

## Complexity Analysis
- **Time O(n)：** 建 Prefix Sum 是 O(n)。每個 Prefix Index 最多 Push 進 Deque 一次，而且只會從 Back 或 Front **其中一端 Pop 一次**。雖然有兩個內層 `while`，所有 Pop 合計至多 n+1 次，所以是 Amortized O(n)，不是 O(n²)。
- **Space O(n)：** `prefix_sum` 長度為 n+1，`deque` 最壞也可能儲存 O(n) 個 Index。

## Solution Code
以下保留自己的原始 AC Code；其中一行 Prefix Sum 註解寫錯，但程式運算本身正確，詳見 Pitfalls。

```cpp
class Solution {
public:
    int shortestSubarray(vector<int>& nums, int k) {
        deque<int> dq;
        int res = INT_MAX;

        // cal prefix sum
        // define prefix_sum[i]: sum[0:i)
        // sum[i:j] = prefix_sum[j-1] - prefix_sum[i];
        vector<long long> prefix_sum(nums.size()+1, 0);
        for (int i = 1; i <= nums.size(); i++) {
            prefix_sum[i] = prefix_sum[i-1] + nums[i-1];
        }

        for (int r = 0; r <= nums.size(); r++) {
            while (!dq.empty() && prefix_sum[r] <= prefix_sum[dq.back()]) {
                dq.pop_back();
            }
            dq.push_back(r);

            while (!dq.empty() && prefix_sum[r] - prefix_sum[dq.front()] >= k) {
                res = min(res, r-dq.front());
                dq.pop_front();
            }
        }

        return res == INT_MAX ? -1 : res;
    }
};
```

## Pitfalls
- **Prefix Sum 註解 Off-by-one：** 原稿 `sum[i:j] = prefix_sum[j-1] - prefix_sum[i]` 有誤；對半開區間 `[i,j)` 應是 `prefix_sum[j] - prefix_sum[i]`。為保留 AC 原稿，程式碼內未直接修改。
- **`pop_back()` 比較方向：** 應在 `prefix_sum[r] <= prefix_sum[dq.back()]` 時淘汰舊值，不能寫成 `>`；等值也必須 Pop，因為新 Index 較大、可形成更短區間。
- **別漏 `prefix_sum[0]=0`：** 要用 `n+1` 長度，才能處理從 `nums[0]` 開始的合法區間，例如 `[2,-1,2]`、`k=3`。
- **半開區間長度是 `r-l`，不是 `r-l+1`：** `prefix_sum[r]-prefix_sum[l]` 代表 `nums[l:r)`。
- **累加要使用 `long long`：** Prefix Sum 可能超過 32-bit `int` 的範圍。
- **Deque 內存 Index，不是 Value：** 比較 Prefix 時要取 `prefix_sum[dq.front()]` / `prefix_sum[dq.back()]`。
- **有負數就不能直接套一般縮窗：** Sum 變動不單調，不能在當前區間不合法時任意捨棄左端點。

## Related Problems
- [[239] Sliding Window Maximum](sliding_window_maximum.md) — 一樣用 Monotonic Deque 存 Index；239 的 Front 因視窗過期移除，862 的 Front 因區間已結算移除。
- [209] Minimum Size Subarray Sum — 當元素皆為正數時，合法性具單調性，可直接使用一般 Sliding Window。
- [560] Subarray Sum Equals K — 也利用 Prefix Sum 差；計數類問題常搭配 Hash Map 記錄 Prefix Frequency。
