# [1590] Make Sum Divisible by P
**Pattern:** [Prefix Sum](../../patterns/prefix-sum.md)
**Complexity:** Time O(n) expected, Space O(n)
**Link:** https://leetcode.com/problems/make-sum-divisible-by-p/

## Trigger Signals
- 移除最短的連續區間，使剩餘總和可被 `p` 整除。令 `target = total % p`，移除的區間總和必須與 `target` 同餘。
- 例如 `[7,4,6]`、`p=5`，`target=2`。移除 `[7]` 後剩下 10，因為 `7 % 5 == 2`。

## Core Insight
令 `prefix[i]` 為前 `i` 個元素總和對 `p` 的餘數。刪除半開區間 `[L,R)` 要滿足 `prefix[R] - prefix[L] ≡ target (mod p)`。固定 `R` 後，查 `prefix[L] ≡ prefix[R] - target (mod p)`。

同一個餘數只留**最新的位置**。固定 `R` 時，最大的 `L` 讓 `R-L` 最短。每輪先查目標餘數，再寫入 `mp[prefix[R]] = R`。

## Why It's Correct
查詢前，Hash Map 記錄每種餘數在 `R` 左側最後出現的位置。若有符合條件的 `L`，正規化到同一餘數範圍後會找到它對應的 key，並取得該 key 下最大的 `L`。因此每個右端點都會檢查它的最短候選，遍歷全部右端點後取最小值即為答案。

`res` 從 `n` 開始，整段候選的長度恰為 `n`，不會降低 `res`。若最後仍為 `n`，代表沒有長度小於 `n` 的合法刪法，回傳 `-1`。原總和已整除時直接回傳 `0`。

## Complexity Analysis
- **期望時間 O(n)**。兩次線性掃描，每次 Hash Map 查詢或更新平均 O(1)。
- **額外空間 O(n)**。Prefix 陣列存 n+1 個餘數，Hash Map 最多有 min(n+1, p) 個 key。

## Solution Code

```cpp
class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        int n = nums.size();
        vector<int> prefix(n + 1, 0);
        // remainder, index
        unordered_map<int, int> mp;
        mp[0] = 0;
        for (int i = 1; i <= n; i++) {
            prefix[i] = prefix[i - 1] + nums[i - 1];
            prefix[i] %= p;
        }
        if (prefix[n] == 0) {
            return 0;
        }
        // cannot remove all elements
        int res = n;
        int target = prefix[n];
        // target % p = prefix[r+1] % p - prefix[l] % p;
        // prefix[l] % p = prefix[r+1] % p - target % p;
        for (int i = 1; i <= n; i++) {
            int goal = prefix[i] - target >= 0 ? prefix[i] - target
                                               : prefix[i] - target + p;
            auto it = mp.find(goal);
            if (it != mp.end()) {
                res = min(res, i - it->second);
            }
            mp[prefix[i]] = i;
        }
        return res == n ? -1 : res;
    }
};
```

## Alternatives / Optimization
第一遍算總餘數，第二遍用 rolling remainder 即可省掉 Prefix 陣列。Hash Map 的最壞額外空間仍為 O(n)。

## Pitfalls
- **C++ 負餘數。** `[3,1,4,2]`、`p=6`，掃到 4 時 `cur=2`、`target=4`，C++ 的 `(2-4)%6` 是 `-2`，要找的 key 是 `4`。兩個餘數均在 `[0,p-1]`，所以差為負時加一次 `p` 就夠。
- **整段不可刪。** `[1]`、`p=2` 唯一候選長度是 `n`，`res` 維持 `n`，最後回傳 `-1`。
- **公式與 code 逐項對照。** 早期註解已推到右 prefix 減 target，code 卻寫成 `target - prefix[i]`。註解中的等式用同餘符號表達更精確。
- **空 prefix 與整數範圍。** `mp[0] = 0` 讓區間能從開頭刪除。這版逐步取餘數，每次加法最多為 `(p-1) + 10^9`，在題目限制下用 `int` 安全。

## Related Problems
- [[525] Contiguous Array](contiguous_array.md) — 兩題都用 `R-L` 算長度。1590 求最短，用 `mp[key] = i` 保留最新位置。525 求最長，用 `try_emplace` 保留最早位置。
