# [239] Sliding Window Maximum
**Pattern:** [Sliding Window](../../patterns/sliding-window.md)
**Complexity:** Time O(N), Space O(K)
**Link:** https://leetcode.com/problems/sliding-window-maximum/

## Trigger Signals
- 固定大小 `k` 的視窗，要回報**每個位置的視窗最大值** → fixed window，但視窗狀態不是「計數」而是「極值」。
- 暴力是對每個視窗重掃一遍取 max（O(N·K)），相鄰視窗只差頭尾一兩個元素，明顯有可增量維護的空間。
- 一看到「視窗 / 區間的 max / min」就該想到 **monotonic deque**，而不是 heap（heap 是 O(N log K)，且刪除過期元素麻煩）。

## Core Insight
維護一個**單調遞減的 deque（存 index，不存值）**，讓 `dq.front()` 永遠是當前視窗的最大值的 index。

兩個關鍵動作：
1. **後端淘汰（push 端）**：新元素 `nums[r]` 進來前，把後端所有比它小的 pop 掉。理由——`nums[r]` 又新又大，那些較小的舊元素在未來任何視窗都不可能再當 max，是廢的，丟掉。pop 完再 push `r`，deque 維持遞減。
2. **前端過期（出窗端）**：當最大值的 index 滑出視窗左界時，從前端 pop 掉它。

這就是為什麼**普通 stack 不夠**：max 住在「底部 / 前端」，而 stack 只看得到 top；而且過期元素也在前端，stack 無法從底部 pop。要同時操作兩端，必須用 deque。

## Complexity Analysis
**Time: O(N)** — 內層 `while (... pop_back())` 看起來像每步 O(K)，但**每個 index 一生只被 push 一次、最多被 pop 一次**（後端淘汰或前端過期擇一），所有 pop 次數加總 ≤ N，是**攤還 O(1)/步 → 總 O(N)**，不是 O(N·K)。
**Space: O(K)** — deque 裡的 index 都落在當前視窗內，前端過期保證它最多裝一個視窗的量，所以被 K 封頂。輸出陣列 O(N−K+1) 是必要輸出，不算輔助空間。

## Solution Code
```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        int l = 0;
        vector<int> res;
        for (int r = 0; r < nums.size(); r++) {
            while (dq.size() && nums[r] > nums[dq.back()]) {
                dq.pop_back();
            }
            dq.push_back(r);
            if (r-l+1 == k) {
                // get max
                res.push_back(nums[dq.front()]);
                // update max
                if (l == dq.front()) {
                    dq.pop_front();
                }
                l++;
            }
        }
        return res;
    }
};
```

## Pitfalls
- **deque 一定存 index，不能存值**：要靠 index 判斷元素有沒有滑出視窗（和左界比較）。比較大小時再用 `nums[index]` 取值。
- **前端過期的時機**：這份寫法用左指針 `l` 當左界，視窗滿（`r-l+1 == k`）時先讀 `dq.front()`，再判斷 `if (l == dq.front())` ——若這次要離開視窗的最左元素正好是 max，就 pop 前端，然後 `l++`。等價於常見的 `if (dq.front() <= r - k) dq.pop_front();`。
- **`>` 還是 `>=` 做後端淘汰**：這裡用嚴格 `>`，相等的元素會被保留（重複值都留在 deque）。仍然正確，因為前端是靠 index 過期、不是靠值；用 `>=` 也對（會把舊的相等值提早丟掉，省一點空間）。
- **操作順序**：先後端淘汰 + push，再判斷視窗是否已滿、讀 max、前端過期。順序錯（例如還沒 push 就讀 front）會 off-by-one。

## Related Problems
- [862] Shortest Subarray with Sum at Least K — 前綴和 + monotonic deque，同樣維護單調性並從兩端操作。
- [1425] Constrained Subsequence Sum — DP 值套 monotonic deque 維護「視窗內最大 dp」。
- [155] Min Stack — 同精神的「維護極值」結構，但只需單端（stack）。
