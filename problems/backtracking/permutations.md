# [46] Permutations
**Pattern:** [Backtracking → Subsets / Permutations](../../patterns/backtracking/subsets-permutations.md)
**Complexity:** Time O(n·n!), Space O(n)
**Link:** https://leetcode.com/problems/permutations/

## Trigger Signals
- 給一個**無重複值**的 array，要求列出**所有排列**
- 順序有意義（`[1,2]` 與 `[2,1]` 算不同解），要枚舉具體的解而非計數 → backtracking
- 決策點是「還沒被用掉的元素，這一層選哪一個」，沒有座標或圖結構 → 用 `used[]` 驅動

## Core Insight
每一層從「還沒放進目前排列的位置」中挑一個，靠一個 `used[]` 陣列標記哪些位置已經在目前的部分排列裡；走到 `cur.size() == nums.size()` 就收下一個完整排列。經典三步驟：**標記-處理-退回（make choice → recurse → undo）**。

當初重寫時忘了 `used[]`——沒有它，recursion body 每層都會把所有元素再選一次，變成 n^n 條分支而非合法排列。`used[]` 就是「這個位置已經在目前排列裡，別再選」的守門員。

## Complexity Analysis
- **Time O(n·n!)**：合法排列共有 n! 個（葉節點數），每產生一個排列還要花 O(n) 把 `cur` 複製進 `res`，故 n × n!。遞迴樹內部節點的總數也被這個階主導。（單寫 O(n!) 抓主導項也可，帶上 n 更嚴謹。）
- **Space O(n)**：遞迴深度最深 n，加上 `used`（n）與 `cur`（n）都是 O(n)。輸出 `res` 本身 O(n·n!) 不計入額外空間。

## Solution Code
```cpp
class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> res;
        vector<int> cur;
        // mark positions already taken in the current permutation,
        // so the loop skips them instead of re-picking
        vector<uint8_t> used(nums.size(), 0);
        solve(nums, used, cur, res);
        return res;
    }

private:
    void solve(const vector<int>& nums, vector<uint8_t>& used, vector<int>& cur,
               vector<vector<int>>& res) {
        if (cur.size() == nums.size()) {
            res.push_back(cur);
            return;
        }
        for (int i = 0; i < nums.size(); i++) {
            if (used[i]) {
                continue;
            }
            used[i] = 1;
            cur.push_back(nums[i]);
            solve(nums, used, cur, res);
            cur.pop_back();
            used[i] = 0;
        }
        return;
    }
};
```

> 只改了那段註解（原本寫 "skip the duplicated elements" 語意會誤導成「去重」，換成 "skip positions already taken"），其餘 code 原樣。

## Pitfalls
- **`used[]` 不是去重工具**。這題 nums 保證無重複值，`used[]` 只防「同一個位置在一條排列裡被選兩次」。若把 nums 換成含重複值（如 `[1,1,2]`），這份 code 會產生重複排列——那是 LC47 的範圍，要另外排序 + `!used[i-1]` 剪枝。
- 忘記 `used[]`（當初就是這裡卡住）：沒有它，每層都能重選所有元素，得到的是長度 n 的所有 n^n 組合而非排列。
- `undo` 兩行（`cur.pop_back()` 與 `used[i]=0`）必須成對還原，漏一行就污染後續分支。

## Follow-ups
- **[47] Permutations II（nums 含重複值）**：目標從「所有排列」變成「所有*不重複*排列」。`used[]` 不足以去重，需先 `sort(nums)`，再在迴圈加 `if (i>0 && nums[i]==nums[i-1] && !used[i-1]) continue;`——同一層裡，值相同且前一個相同值尚未被選時就跳過，避免同一組值以相同順序被枚舉多次。破的假設正是「元素兩兩相異」。

## Related Problems
- [47] Permutations II — 同模板，nums 含重複值，需排序 + 同層剪枝去重
- [[78] Subsets](subsets.md) — 順序無意義，改用 `start` index、每個節點都收一個解，而非等 `cur` 滿
- [77] Combinations — 從 n 選 k，一樣 `start` index 驅動，終止條件是 `cur.size()==k`
- [[39] Combination Sum](combination_sum.md) — `start` index + 元素可重複選（遞迴傳 `i` 而非 `i+1`）
