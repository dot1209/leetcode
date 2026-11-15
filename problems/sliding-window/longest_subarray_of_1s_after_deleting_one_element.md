# [1493] Longest Subarray of 1's After Deleting One Element
**Pattern:** [Sliding Window](../../patterns/sliding-window.md)
**Complexity:** Time O(n), Space O(1)
**Link:** https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/

## Trigger Signals
- 給定只含 0 和 1 的陣列，**恰好刪除一個元素**，求剩下的陣列中最長連續 1 的長度。
- 「最長連續區段」加上「最多容忍一個異值」→ 可變長度的 Sliding Window，視窗內最多含一個 0。

## Core Insight
- **不變量**。縮窗完成後，閉區間 `[l, r]` 最多含一個 0，且 `l` 是目前右端 `r` 能用的最左起點。
- **縮窗條件**。加入 `nums[r]` 後，若 `zeros > 1`，逐步移動 `l` 並更新 `zeros`。任何已有兩個 0 的起點，往後延伸右端仍會包含至少兩個 0，因此可以略過。
- **計算答案**。視窗有一個 0 就刪掉它。視窗全是 1 就刪掉一個 1。兩種情況都能得到 `(r - l + 1) - 1 = r - l`。對固定的右端，最長合法視窗提供最大的候選值。

| 輸入 | 答案 | 原因 |
| --- | --- | --- |
| `[1, 1, 0, 1]` | 3 | 刪掉中間的 0 |
| `[1, 1, 1]` | 2 | 必須刪掉一個 1 |
| `[0, 0, 0]` | 0 | 每次縮窗後只剩一格，`r - l = 0` |

## Why It's Correct
如果某個最佳解刪掉的是全 1 區段外的元素，原陣列中那段全 1 仍是連續的。把區段往任一有鄰居的一側多納入一格，再刪掉那格，就能用同樣的視窗公式得到該長度。

## Complexity Analysis
- **Time O(n)：** 每個指標最多走 n 步。內層 `while` 只會讓 `l` 前進，全程合計至多 n 次，所以是 Amortized O(n)。
- **Space O(1)：** 只用 `l`、`res`、`zeros` 三個變數。

## Solution Code
```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums) {
        int l = 0;
        int res = 0;
        int zeros = 0;
        for (int r = 0; r < nums.size(); r++) {
            if (nums[r] == 0) zeros++;
            while (zeros > 1) {
                if (nums[l] == 0) zeros--;
                l++;
            }
            // our interval is represented as [l:r]
            res = max(res, r-l);
        }
        return res;
    }
};
```

## Pitfalls
- **全 1 時仍須刪一格**：答案為 `n - 1`，不是 `n`。用 `r - l` 更新答案就自動涵蓋這個情況。
- **答案是 `r - l`，不是 `r - l + 1`**：閉區間 `[l, r]` 的長度要再減去被刪掉的那一格。
- **全 0 時答案為 0**：每次縮窗後視窗只剩一格，`r - l = 0`。

## Follow-ups
### 任意整數，刪一個後最長全相同區段
保留滑窗和 `r - l`，將合法條件改為 **`windowLength - maxFrequency <= 1`**。例如 `[2, 3, 3]` 刪掉 2 即可，`[2, 3, 3, 2]` 則必須縮窗。寫法上可維護頻率表，將頻率歸零的值移除。合法視窗最多兩種值，加入右端後暫時最多三種，因此每次重新計算最高頻率仍為 O(1)，全程時間 O(n)、額外空間 O(1)。

## Related Problems
- [487] Max Consecutive Ones II — 同樣是視窗內最多一個 0，差別在翻轉而非刪除，答案是 `r - l + 1`。
- [1004] Max Consecutive Ones III — 把「最多一個 0」推廣成「最多 k 個 0」。
- [424] Longest Repeating Character Replacement — 合法條件同為 `windowLength - maxFrequency <= k`，對應上面的任意整數延伸題。
