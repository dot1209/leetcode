# Greedy

Greedy 是「每一步都做當下看起來最好的選擇、做完不回頭」的策略。它能成立的關鍵不是直覺，而是要能證明 **local optimal → global optimal**——最常用的工具是 **exchange argument**：假設存在一個最優解沒有選貪心會選的那個元素，那就把它換成貪心選的，論證「換完之後答案不會變差」，於是貪心解至少跟最優解一樣好。它存在的價值是：當這個交換論證成立時，原本可能要 DP / 搜索的問題，可以壓成「sort 一次 + 線性掃過去逐一取」。

最常見的具體形式就是 **sort 後依序貪心取用**：先把元素照某個 key 排好（最便宜、最短、最早結束……），再線性掃，能取就取直到資源（budget / 次數）用盡。

## When to Use
- 要**最大化能取的數量**或**最小化成本／次數**，而「取某個元素」的決策**不影響其他元素能不能取**（彼此獨立、無後效性）
- 排序後有明顯且固定的取用順序：最便宜先買、最短先做、最早結束先排
- 能用 exchange argument 說服自己：先取最 X 的那個，不會比別的順序差
- 訊號詞：`maximum number of ...`、`in a budget`、`as many as possible`、`minimum number of ...`
- **反例（這時別用 greedy）**：選擇之間互相牽連——取了 A 就不能取 B、或取某元素會改變後面元素的權重 → 通常要 DP。最經典的反例是 **0/1 knapsack**：價值/重量不成單調比例時，貪心拿 CP 值最高的會錯，必須 DP。

## Typical Complexity
**Time:** O(n log n) — 由 **sort 主導**；排序後的線性掃描只是 O(n)。若值域有限（例如本題 `costs[i] ≤ 1e5`），可改用 **counting sort** 把排序降到 O(n + maxVal)，整題就變 O(n + maxVal)、沒有 log 因子。
**Space:** O(1) ~ O(n) — in-place sort 為 O(1)（遞迴版 quicksort 另計 O(log n) stack）；若改用額外容器（map / 計數陣列）承載排序，則為 O(n) 或 O(maxVal)。

關鍵理解：greedy 本身只是 O(n) 的掃描，複雜度幾乎都是花在「把順序準備好」這一步——所以想優化時間，優化的對象是**排序方式**（comparison sort 的 O(n log n) vs counting sort 的 O(n + maxVal)），不是貪心迴圈。

## General Template
```cpp
// Sort, then take greedily in order until the budget / constraint runs out.
sort(items.begin(), items.end());          // cheapest / smallest / earliest first
int count = 0;
for (int x : items) {
    if (budget < x) break;                  // cheapest remaining is unaffordable -> nothing later fits either
    budget -= x;
    count++;
}
return count;
```

## Pitfalls
- **先證明再貪心。** 看到「最多／最少」就 sort+greedy 很危險——一定要先確認 exchange argument 成立（決策彼此獨立）。否則就是該用 DP 的題目被當成 greedy 寫，會 WA。
- **sort 的 key / 方向要對。** 「買最多支」是 ascending（便宜先）；「在 deadline 內排最多工作」可能要 by deadline 或 by end-time，搞錯方向整題就錯。
- **早停的正確性靠「已排序」。** 因為是 ascending，當最便宜的剩餘元素都買不起時，後面更貴的必然也買不起 → 可以直接 `break`/`return`。沒排序就不能這樣早停。

---

## Problems

### [[1833] Maximum Ice Cream Bars](../problems/greedy/max_ice_cream_bars.md)
**Complexity:** Time O(n + maxVal), Space O(maxVal)
- **Trigger:** 固定 coins 想買「最多數量」的 ice cream，且買一支不影響其他支 → 便宜先買能買越多
- **Insight:** 從最便宜開始買；exchange argument——最優解若沒買最便宜的那支，換成最便宜的不會更差
- **Pitfall:** 值域有限（cost ≤ 1e5）才能用 counting sort 換掉排序的 log——代價是固定 O(maxVal) 空間；值域一大就得退回 O(n log n)

### [[1877] Minimize Maximum Pair Sum in Array](../problems/greedy/minimize_maximum_pair_sum.md)
**Complexity:** Time O(n log n), Space O(1)
- **Trigger:** 兩兩配對並「最小化最大配對和」(minimize the maximum) → sort 後頭尾相接
- **Insight:** 最小配最大；exchange argument——若最優解沒把 min 跟 max 配在一起，交換成 `(min,max)`+`(x,y)` 後兩個和都 ≤ 原本的 `max+y`，max 不增
- **Pitfall:** 別只憑直覺配頭尾就交卷，正確性要靠 exchange argument；回傳的是配對和的 max 不是總和
