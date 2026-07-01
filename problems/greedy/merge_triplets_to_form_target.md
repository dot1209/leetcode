# [1899] Merge Triplets to Form Target Triplet
**Pattern:** [Greedy](../../patterns/greedy.md)
**Complexity:** Time O(N), Space O(1)
**Link:** https://leetcode.com/problems/merge-triplets-to-form-target-triplet/

## Trigger Signals
- 給一堆 triplet，操作是「挑兩個取 element-wise max」可做**任意多次**，問能不能拼出 `target` → 不是最佳化，是**可行性判定（yes/no）**。
- 操作有兩個關鍵性質：**monotone**（max 只增不減）+ **per-coordinate**（三軸各自獨立取 max）。這兩個性質就是解題鑰匙。
- 訊號：「apply operation any number of times」+「能否得到某目標」→ 別模擬過程，改想「所有可達結果構成的集合」。

## Core Insight
關鍵轉念：merge 是 element-wise max，所以**任何可達的結果，都是某個 triplet 子集的 element-wise max**。問題不是「模擬一連串操作」，而是「**存不存在一個 subset，它的 element-wise max 剛好 = target**」。

這樣看之後，兩步就解完：
1. **Filter（丟 poison）**：任一軸 `> target` 的 triplet 一律不能用——merge 進來那軸就超過 target，而 max 只增不減，**永遠回不去**。
2. **Cover（檢查覆蓋）**：在剩下的 valid triplet 裡，三個軸**各自**都有人剛好 `== target[k]`（可以是三個不同的 triplet）就能拼出 target；否則不行。

### 為什麼這兩個條件是充要的（必要 + 充分）
- **必要（沒這兩條就不可能）**：
  - overshoot 的 triplet 不能用——merge 進來該軸 `> target`，max 只增不減、回不去 → 只能用「每軸都 `≤ target`」的 valid triplet。
  - 結果某軸要剛好 `== target[k]`，就一定要有某個被選的 triplet 在該軸達標（大家都 `≤ target[k]`，要 max 打到剛好 `target[k]` 得有人 ==）→ 三軸各要有人 hit。
- **充分（有這兩條就一定行）**：
  - 三軸都有 valid triplet 達標的話，把**所有** valid triplet 全 merge 起來：每軸都 `≤ target`（都 valid）、又該軸有人 `== target` → element-wise max 在每軸剛好 = target → 拼出 target。

→ `x && y && z`（三軸都被覆蓋）正好是充要條件。

## Complexity Analysis
- **Time O(N)**：單趟掃 N 個 triplet，每個 O(1) 比較。下界也是 Ω(N)——任何一個 triplet 都可能是「唯一」達標某軸的那個（例如只有最後一個 triplet 的第一軸 `== target[0]`），漏看就可能誤判，所以一定要全看過 → O(N) 已是最佳。
- **Space O(1)**：只有 `x`、`y`、`z` 三個 bool，與 N 無關。

## Solution Code
```cpp
class Solution {
public:
    bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
        bool x = false, y = false, z = false;
        for (int i = 0; i < triplets.size(); i++) {
            // skip: overshoots target on some axis. Merging it would push that
            // axis above target permanently (max only increases) -> unreachable
            if (triplets[i][0] > target[0] || triplets[i][1] > target[1] ||
                triplets[i][2] > target[2]) {
                continue;
            }
            x |= (triplets[i][0] == target[0]);
            y |= (triplets[i][1] == target[1]);
            z |= (triplets[i][2] == target[2]);
        }
        return x & y & z;
    }
};
```

## 程式碼小優化（非 bug，原碼照留）
- `return x & y & z;` 用 bitwise `&`：對 `bool`（值只會是 0/1）結果正確，但慣例上邏輯判斷用 `&&`（較清楚、有 short-circuit）。這裡沒 side effect 所以沒差。
- `i < triplets.size()` 是 `int` vs `size_t` 的 signed/unsigned 比較（`-Wsign-compare`）；可改成 range-based for `for (auto& t : triplets)`，連 index 雜訊一起省掉。

## Pitfalls
記一下我一開始卡住的點（很有代表性）：

- **第一版想「模擬」整個 merge 過程**：sort 之後 `cur = triplets[0]`，再一路把後面的 triplet 依序 merge 進 `cur`，加上一些臨時的 skip 條件。這條路會死，原因有二：
  - **沒 filter 掉 overshoot 的 triplet**：sort 後 `cur = triplets[0]` 可能本身就超標（例如 `[3,6,6]`，而 target 中間軸 `< 6`），從第一步就被污染，而 max 只增不減 → 永遠救不回來。
  - **skip 條件太窄**：只在 `cur[k] == target[k]` 時才 skip；當 `cur[k]` 還沒到 target 時，一個 overshoot 的 poison triplet 會直接被 merge 進來，把該軸頂爆。
- **真正的修法是換 model**：別維護一個「always valid 的 running merge」，而是認清「可達 = 某 subset 的 max」，於是只要 filter + 檢查覆蓋。**sort 在這題完全沒用**（答案與順序無關）。
- 教訓：操作**可任意次 + monotone** 時，先想**可達集合**，別模擬流程。這個 reframe 比這題本身更值得記。

## Follow-ups
- **推廣到 k 維**：target / triplet 從 3 維變 k 維，邏輯一字不改——filter 掉任一軸 overshoot 的，再檢查 k 個軸每個都有人達標。Time O(N·k)、Space O(k)。「3」完全不特別。
- **從可行性升級成「構造 / 最少操作次數」**：
  - **構造一組解**：把所有 valid triplet 全 merge 起來就會得到 target（前提三軸都覆蓋），所以不只回 yes，還給得出做法。
  - **最少 merge 次數**：merge `m` 個 triplet 需 `m−1` 次操作 → 找「覆蓋三軸的最小 triplet 子集」。因為只有 3 軸，是超小的 set cover：先看有沒有單一 triplet 已 `== target`（1 個、0 次操作），再看 2 個能否覆蓋三軸，最後才 3 個 → 上限 3 個 triplet / 2 次操作。骨架不變，只是判定變最佳化。

## Related Problems
- [55] Jump Game — 同樣是 greedy 的**可行性判定**（能不能到終點），yes/no 而非最佳化；只是它維護「最遠可達 index」，本題用 filter + 覆蓋。
- [45] Jump Game II — 上一題的最佳化版（最少跳幾次到終點），正好對應本題 follow-up 的「最少 merge 次數」——feasibility 升級成 optimization 的經典一對。
- [780] Reaching Points — monotone 操作（座標只增）下的 reachability，解法是「往回推、描述可達集合」而非正向模擬，跟本題「別模擬流程、認清可達 = 某 subset 的 max」是同一個教訓。
- （筆記內對照）[1833] Maximum Ice Cream Bars、[1877] Minimize Maximum Pair Sum — Greedy 的 sort-and-take／配對型，跟本題的 filter-覆蓋型是不同操作型態。
