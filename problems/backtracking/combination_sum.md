# [39] Combination Sum
**Pattern:** [Backtracking → Subsets / Permutations](../../patterns/backtracking/subsets-permutations.md)
**Complexity:** Time O(N^(target/M)), Space O(target/M)
**Link:** https://leetcode.com/problems/combination-sum/

## Trigger Signals
- 從一個 array 枚舉「所有加起來等於 target 的組合」，順序無意義 → combination（用 `start`/`idx` index，不是 `used[]`）
- **同一個數字可以重複選任意次** → 這是這題的招牌 twist

## Core Insight
就是一般 combinations，只差**一行**：遞迴時傳 `i` 而不是 `i+1`。

- 傳 `i`：下一層還能從 `i` 開始 → 同一個數字可以再被選 → **可重複選**
- 傳 `i+1`：下一層只能從 `i` 之後開始 → 每個數字最多用一次（那是 LC40 的方向）

決策點是「這一層從剩下的候選裡，選哪一個開始往下加」，而不是「這個元素選或不選」——兩種框架是同一棵樹的不同編碼，這份 code 走的是 for-loop「選哪一個」那一版。

## Complexity Analysis
- **Time O(N^(target/M))**：每一層最多 N 個分支（N = 候選個數），遞迴深度最多 `target/M`，因為每選一個數 target 至少減掉最小元素 M，所以最多選 `target/M` 層就到底。指數的底是分支數、指數是深度。
- **Space O(target/M)**：遞迴堆疊深度 + `cur` 路徑長度，都被同一個 `target/M` 界住。（不計 `res` 輸出本身。）

剪枝（sort + break）只砍掉大量無效分支、改善常數，不改變最壞情況的階。

## Solution Code
```cpp
class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> res;
        vector<int> cur;
        sort(candidates.begin(), candidates.end());
        solve(candidates, 0, target, cur, res);
        return res;
    }

private:
    void solve(const vector<int>& nums, int idx, int target, vector<int>& cur,
               vector<vector<int>>& res) {
        if (target == 0) {
            res.push_back(cur);
            return ;
        }

        for (int i = idx; i < nums.size(); i++) {
            // pruning
            if (target-nums[i] < 0) {
                break;
            }
            cur.push_back(nums[i]);
            solve(nums, i, target-nums[i], cur, res);
            cur.pop_back();
        }

        return;
    }
};
```

## Pitfalls
- **結束條件是 `target == 0` 就 push，不是 `idx == nums.size() && target == 0`**。一開始寫成後者會**漏解**——合法組合常常在用盡 index 之前就湊到 0 了，硬要走到底反而找不到。
- **傳 `i` vs `i+1`**：`i` = 可重複，`i+1` = 每個數只用一次。這一字之差決定整題語意。
- **sort 之後剪枝要用 `break` 不是 `continue`**：sort 過後 `nums` 遞增，一旦 `target - nums[i] < 0`，後面更大的一定也不行，直接 `break` 收掉整段；不 sort 的話只能用 `continue`（後面可能有更小的還湊得出來），或靠 `target < 0` 在 recurse 進去後才擋，效率差很多。
- 別忘了 undo（`cur.pop_back()`），否則污染其他分支的部分解。

## Follow-ups
- **[40] Combination Sum II** — 每個數字**只能用一次**，且 `candidates` 含**重複值**。改動：遞迴傳 `i+1`（只用一次），再加同層去重 `if (i > idx && nums[i] == nums[i-1]) continue;`（同一層不重複挑同值，避免重複組合）。
- **[377] Combination Sum IV** — 問的是**組合「個數」**且**順序有意義**（其實是 permutation 計數）。因為只要數量、不還原路徑，最佳解是 **DP** 而非 backtracking——正好對應 pattern README 裡「DP 算個數、backtracking 列具體解」那條界線。

## Related Problems
- [40] Combination Sum II — 同族，把「可重複」換成「每個一次 + 去重」
- [216] Combination Sum III — 限定「剛好 k 個數」且候選固定為 1~9，多一個長度限制的剪枝
- [77] Combinations — 最純的 `start`-index combination（傳 `i+1`），本題把它加上「可重複 + 湊 target」
- [[78] Subsets](subsets.md) — 同樣 `start`-index，但每個節點都是解、沒有 target 條件
