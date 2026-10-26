# Backtracking — Subsets / Permutations

## When to Use
- 從一個給定集合（array）**枚舉所有排列 / 組合 / 子集**，而不是在格子或圖上走路徑
- 沒有空間座標，決策點是「還沒被用掉的元素，這一步選哪一個」
- 題目敘述出現：all permutations、all subsets、all combinations、enumerate、生成所有…
- 與 grid backtracking 的差別：那邊靠 board 座標移動、in-place mark 格子；這邊靠一個 `used[]` 或 `start` index 追蹤「哪些元素還能選」

這一類的核心不是「走到哪」，而是**「在每一層決定拿掉哪一個候選」**，遞迴深度等於最終解的長度。兩種驅動方式：

- **`used[]` 陣列（permutations）**：順序有意義，每一層都能從所有「還沒被拿」的元素裡挑，`[1,2]` 和 `[2,1]` 是不同解。
- **`start` index（subsets / combinations）**：順序無意義，下一層只從 `start` 之後挑，避免同一組合以不同順序重複出現。

## Template Code
```cpp
// Permutations flavor — used[] tracks which positions are already
// in the current partial answer; order matters.
void solve(const vector<int>& nums, vector<uint8_t>& used,
           vector<int>& cur, vector<vector<int>>& res) {
    if (cur.size() == nums.size()) {   // a full arrangement is done
        res.push_back(cur);
        return;
    }
    for (int i = 0; i < nums.size(); i++) {
        if (used[i]) continue;         // skip positions already taken
        used[i] = 1;                   // make choice
        cur.push_back(nums[i]);
        solve(nums, used, cur, res);   // recurse
        cur.pop_back();                // undo
        used[i] = 0;
    }
}
```

三步驟一如 backtracking 通則：**make choice（`used[i]=1` + push）→ recurse → undo（pop + `used[i]=0`）**。

## Pitfalls
- **`used[]` ≠ 去重**：在 nums 無重複值的前提下，`used[]` 只是防止「同一個位置在一條排列裡被選兩次」。它跟「重複的值」無關。若 nums 本身含重複值（LC47），這份 code 會吐出重複排列——去重要另外排序 + `if (i>0 && nums[i]==nums[i-1] && !used[i-1]) continue;`。
- 忘了 undo（`pop_back` 或 `used[i]=0` 其一漏掉），會污染其他分支的部分解。
- permutations 用 `used[]`（每層看全體）；subsets/combinations 用 `start` index（每層只看後面），兩者別混用，否則排列會被當組合、或組合會漏。
- 終止條件對象要對：permutations 是 `cur.size()==nums.size()`；subsets 是「每個節點都是一個解」，沒有單一終止長度。
- **subsets 有兩種樹形，「push 的位置」跟著變**：for-loop（`start` index）版每個遞迴節點都是合法解 → 一進 function body 就 `push_back`；pick / not-pick 二元樹版只有走到底的 leaf（`idx==nums.size()`）才是完整解 → 到底才 push。別把「每節點都推」的習慣帶到二元樹版，或反過來漏推。permutations 也是「leaf 才是解」的那一類。

---

## Problems

### [[46] Permutations](../../problems/backtracking/permutations.md)
**Complexity:** Time O(n·n!), Space O(n)
- **Trigger:** 無重複值的 array，枚舉所有排列、順序有意義
- **Insight:** `used[]` 標記已在目前排列中的位置，每層從沒用過的元素挑；make-recurse-undo
- **Pitfall:** `used[]` 是防「同位置重選」不是「去重」；含重複值的 nums 會產生重複排列

### [[39] Combination Sum](../../problems/backtracking/combination_sum.md)
**Complexity:** Time O(N^(target/M)), Space O(target/M)（M = 最小元素）
- **Trigger:** 枚舉所有加起來等於 target 的組合、順序無意義，且**同一數字可重複選**
- **Insight:** 就是 `start`-index combination，唯一差別是遞迴傳 `i` 而非 `i+1`（留在原地 → 可重複）；sort 後用 `break` 剪枝
- **Pitfall:** 結束條件 `target==0` 就 push（別加 `idx==n`，會漏解）；傳 `i` vs `i+1` 決定「可重複／只用一次」

### [[78] Subsets](../../problems/backtracking/subsets.md)
**Complexity:** Time O(n·2^n), Space O(n)（backtracking）/ O(1)（bitmask，皆不計 output）
- **Trigger:** 枚舉所有子集、順序無意義、每個元素最多一次；沒有 target 剪枝
- **Insight:** 兩種樹形——for-loop（`start` index）每節點都是解 → 進 body 就 push；pick/not-pick 二元樹只有 leaf 是解 → `idx==n` 才 push。另有 bitmask 枚舉把 O(n) stack 砍成 O(1)
- **Pitfall:** push 位置要跟樹形對上；for-loop 版傳 `i+1`（傳 `i` 就變可重複）；O(n) 空間是遞迴深度+cur，不是「元素出現與否」
