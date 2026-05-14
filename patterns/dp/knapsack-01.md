# DP — 0/1 Knapsack

## When to Use
每個物品**最多選一次**（pick or not pick），要求對某個總量（weight / sum / count）做：
- **Feasibility**：能否湊出 target？→ bool dp，`||`
- **Counting**：幾種方式湊出 target？→ int / long dp，`+`
- **Optimization**：最大/小 value？→ int dp，`max` / `min`

關鍵特徵：每個元素獨立選擇 → 對應「2^n 種子集合」 → 用 DP 把這 2^n 壓成 O(n × W)（pseudo-polynomial）。

與 unbounded knapsack 的差別：unbounded 允許重複選同個物品（內層 `w` 正向掃）；0/1 不允許（內層 `w` 必須**倒著掃**才不會重複使用同個物品）。

## Template Code

### 2D bool (feasibility) — 最直觀
```cpp
vector<vector<bool>> dp(n + 1, vector<bool>(W + 1, false));
dp[0][0] = true;                            // 空集合可湊出 0
for (int i = 1; i <= n; i++) {
    for (int w = 0; w <= W; w++) {
        dp[i][w] = dp[i-1][w];              // 不選 nums[i-1]
        if (w >= nums[i-1])
            dp[i][w] = dp[i][w] || dp[i-1][w - nums[i-1]];  // 選
    }
}
return dp[n][W];
```

### 1D rolling (O(W) space)
```cpp
vector<bool> dp(W + 1, false);
dp[0] = true;
for (int num : nums) {
    for (int w = W; w >= num; w--) {        // 倒著掃！
        dp[w] = dp[w] || dp[w - num];
    }
}
return dp[W];
```
**倒著掃**是 0/1 vs unbounded 的關鍵：正向掃會讓同一個 `num` 多次被計入。

### Bitset (極致加速)
```cpp
bitset<W_MAX + 1> dp;
dp[0] = 1;
for (int num : nums) dp |= dp << num;
return dp[W];
```
原理：bit `w` 代表「能否湊出 w」，`dp << num` 等於「所有可達 sum 都加 num」。一個指令處理 64 bits，常數加速約 64x。**只適用於 feasibility**，counting 用不了。

### Counting 變體（dp 是 int）
```cpp
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
dp[0][0] = 1;
for (int i = 1; i <= n; i++) {
    for (int w = 0; w <= W; w++) {
        dp[i][w] = dp[i-1][w];
        if (w >= nums[i-1])
            dp[i][w] += dp[i-1][w - nums[i-1]];
    }
}
return dp[n][W];
```
注意 overflow：方案數最壞 2^n，必要時用 `long long`。

## Pitfalls
- **狀態定義要寫死**：「`dp[i][w]` 是 bool 還是 int？意義是什麼？」一開始模糊，後面 transition 一定錯
- **0/1 vs unbounded 內層方向**：0/1 必須倒著掃 W、unbounded 正向掃
- **Feasibility 用 `bool` + `||`**：用 int + `+=` 看似通用，但有 overflow 風險、失去 bitset 加速、語意較弱（細節見 LC 416 entry）
- **Pseudo-polynomial 的限制**：runtime O(n × W) 對 W 是 polynomial，但對 input bit-length（log W）是 exponential。題目給的 `nums[i]` 上限若達 10^9 級別，DP 直接不可行
- **Base case 不要寫成 row 全 true / false**：應該是「空集合 dp[0][0]=true、dp[0][w>0]=false」這種 specific 設定，不是整列同值

---

## Problems

### [[416] Partition Equal Subset Sum](../../problems/dp/partition_equal_subset_sum.md)
**Complexity:** Time O(n·sum), Space O(n·sum) → 可壓 O(sum)
- **Trigger:** 把 array 分兩堆和相等 → 「能否湊出 sum/2 的子集合」→ 0/1 knapsack feasibility
- **Insight:** 先檢查 sum 奇偶（奇直接 false），再用 bool DP 判斷能否湊到 sum/2
- **Pitfall:** Base 必須是 `dp[0][0]=true` 其餘 false；切記不是 row 全 true
