# [78] Subsets
**Pattern:** [Backtracking → Subsets / Permutations](../../patterns/backtracking/subsets-permutations.md)
**Complexity:** Time O(n·2^n), Space O(n)（backtracking）/ O(1)（bitmask，皆不計 output）
**Link:** https://leetcode.com/problems/subsets/

## Trigger Signals
- 枚舉一個 array 的**所有子集**，順序無意義、每個元素最多用一次 → `start` index、遞迴傳 `i+1`（不可重複）
- 「所有 subset」而不是「湊到某個 target」→ 沒有 target 剪枝，每個節點/每個 leaf 直接就是一個解

## Core Insight
subsets 就是 combinations 的家族，跟 [Combination Sum](combination_sum.md) 差在「不可重複」（傳 `i+1` 不是 `i`）、且沒有 target 條件。真正值得記的是**同一題有兩種樹形，差別在「哪裡 push 結果」**：

- **for-loop 型（`start` index）**：recursion tree 的**每個節點都是一個合法 subset** → 一進 function body 就 `res.push_back(cur)`，不需要終止長度。
- **pick / not-pick 型（二元樹）**：每層決定「這個元素選或不選」，只有走到底（`idx == nums.size()`）的 **leaf 才是一個完整 subset** → 到底才 push。2^n 個 leaf 對應 2^n 個 subset。

把「for-loop 每節點推」的習慣帶到二元樹版、或反過來，是最容易搞混的地方。

## Complexity Analysis
- **Time O(n·2^n)**：一共 2^n 個 subset，每個 `push_back(cur)` 要 copy 目前路徑、花 O(n)。兩種 backtracking 樹形節點數不同（for-loop 版 2^n 個節點全推；二元樹版 2^(n+1)−1 個節點但只有 2^n 個 leaf 推），總 copy 成本都是 O(n·2^n)。bitmask 版外層 2^n × 內層 n 也是 O(n·2^n)。
- **Space O(n)（backtracking，auxiliary）**：遞迴深度 ≤ n，加上 `cur` 最多裝 n 個元素——都被 n 界住。**注意**：這裡的 O(n) 是「不含 output」的額外空間；連 output 一起算是 O(n·2^n)。「每個元素出現或不出現」解釋的是**為什麼有 2^n 個 subset**（時間/數量），不是空間 O(n) 的來源。
- **Space O(1)（bitmask，auxiliary）**：沒有遞迴 stack、沒有 `cur` buffer，直接對每個 bitmask 寫進 `res`，額外空間 O(1)（一樣不計 output）。
- 時間下界：光把答案寫出來就是 Θ(n·2^n)，所以 O(n·2^n) 已是最佳，三種寫法時間同階。

## Solution Code

### 寫法 1：for-loop（`start` index，每個節點都是解）
```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        // i = 0 [], [1]
        // i = 1 [], [2], [1, 2], [1]
        // i = 2 [], [3], [2], [1], [1, 2, 3], [1, 2], [2, 3], [1, 3]
        vector<vector<int>> res;
        vector<int> cur;
        solve(nums, 0, cur, res);
        return res;
    }
private:
    void solve(const vector<int>& nums, int idx, vector<int>& cur, vector<vector<int>>& res) {
        res.push_back(cur);
        
        for (int i = idx; i < nums.size(); i++) {
            // pick
            cur.push_back(nums[i]);
            solve(nums, i+1, cur, res);
            // not to pick
            cur.pop_back();
        }
        return ;
    }
};
```

### 寫法 2：pick / not-pick（二元樹，leaf 才是解）
```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        // i = 0 [], [1]
        // i = 1 [], [2], [1, 2], [1]
        // i = 2 [], [3], [2], [1], [1, 2, 3], [1, 2], [2, 3], [1, 3]
        vector<vector<int>> res;
        vector<int> cur;
        solve(nums, 0, cur, res);
        return res;
    }
private:
    void solve(const vector<int>& nums, int idx, vector<int>& cur, vector<vector<int>>& res) {
        if (idx == nums.size()) {
            res.push_back(cur);
            return ;
        }
        // pick
        cur.push_back(nums[idx]);
        solve(nums, idx+1, cur, res);
        // not to pick
        cur.pop_back();
        solve(nums, idx+1, cur, res);
        return ;
    }
};
```

### 寫法 3：bitmask 枚舉（O(1) 額外空間，非 backtracking）
```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        int n = nums.size();
        int p = 1 << n;
        vector<vector<int>> res(p);
        for (int i = 0; i < p; i++) {
            for (int j = 0; j < n; j++) {
                // continas jth element
                if ((i >> j) & 1) {
                    res[i].push_back(nums[j]);
                }
            }
        }
        return res;
    }
};
```
先開好 `2^n` 個位子，第 `i` 個 subset 由整數 `i` 的 binary 決定：第 `j` 個 bit 為 1 就放 `nums[j]`。用「整數本身」當作「選/不選」的狀態，省掉遞迴 stack。

## Pitfalls
- **push 的位置跟樹形綁定**：for-loop 版每個節點都推（一進 body 就 `push_back`）；二元樹版只有 `idx==nums.size()` 的 leaf 才推。搞混會推出一堆重複/不完整的中間狀態，或整組漏掉。
- **for-loop 版必須傳 `i+1`**：傳 `i` 會變「可重複選」（那是 [Combination Sum](combination_sum.md) 的方向）。subsets 不可重複，一定 `i+1`。
- **空間複雜度的「理由」別套錯**：O(n) 是遞迴深度 + `cur` 長度，不是「每個元素出現或不出現」——後者是 2^n 個解的來源（時間/數量）。
- bitmask 版能用的前提是 `n` 不大（`1 << n` 會爆），LC78 的 `n ≤ 10` 沒問題。

## Follow-ups
- **[90] Subsets II** — `nums` **含重複值**，要求子集不重複。改動：先 `sort`，for-loop 版在同一層跳過重複值 `if (i > idx && nums[i] == nums[i-1]) continue;`（同層不重挑同值，避免產生重複子集）。這正是 subsets 加上「重複值去重」那一招，和 Combination Sum II 的去重手法同一套。

## Related Problems
- [90] Subsets II — 同款，多了「重複值去重」
- [[39] Combination Sum](combination_sum.md) — 同 `start`-index 家族，把「不可重複」換成「可重複 + 湊 target」（傳 `i` 而非 `i+1`）
- [77] Combinations — subsets 限定「剛好選 k 個」，多一個長度剪枝
- [[46] Permutations](permutations.md) — 同 pattern 但順序有意義、用 `used[]` 而非 `start` index
- [784] Letter Case Permutation — 一模一樣的「每個字元選大寫或小寫」二元樹，pick/not-pick 樹形的另一個化身
