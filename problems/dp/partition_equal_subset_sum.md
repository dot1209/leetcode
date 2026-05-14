# [416] Partition Equal Subset Sum
**Pattern:** [DP → 0/1 Knapsack](../../patterns/dp/knapsack-01.md)
**Complexity:** Time O(n · sum), Space O(n · sum) → 可壓到 O(sum) 或 bitset O(sum / 64)
**Link:** https://leetcode.com/problems/partition-equal-subset-sum/

## Trigger Signals
- 把 `nums` 切成兩個子集合，要求兩堆和相等
- 等價問題：「**能否從 `nums` 中挑一個子集合，和為 `sum/2`**」 → 經典 0/1 knapsack feasibility
- 每個元素只能用一次 → 0/1（不是 unbounded）

## Core Insight
1. **奇偶過濾**：若 `sum` 為奇數，不可能平分 → 直接 false
2. **轉化**：問題變成「能否用部分 `nums` 湊出 `goal = sum/2`」
3. **DP feasibility**：`dp[i][w]` = 用前 i 個元素能否湊出和 w；轉移就是「選或不選 `nums[i-1]`」

## Complexity Analysis
- **Time O(n · sum)**：表的大小是 `(n+1) × (goal+1)`，每格 O(1) 轉移
- **Space O(n · sum)**：完整 2D table；若用 rolling 1D 可壓到 O(sum)
- **Pseudo-polynomial**：對 `sum` 是 polynomial，但 `sum` 在 input 編碼裡只佔 `log(sum)` bits，所以對 input bit-length 是 exponential。LC 416 限制 `nums[i] ≤ 100, n ≤ 200` → goal ≤ 10⁴ 跑得動

## Solution Code
```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int n = nums.size();
        int sum = accumulate(nums.begin(), nums.end(), 0);
        if (sum & 1) {
            return false;
        }
        int goal = sum / 2;
        // check whether we can make sum of elements equal to goal
        // define dp[i][w] := consider index 0~i can form the sum w;
        vector<vector<bool>> dp(n+1, vector<bool>(goal+1, false));
        
        // no element form zero sum
        dp[0][0] = true;
        // init: use no element
        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= goal; w++) {
                dp[i][w] = dp[i-1][w]; // not pick 
                if (w >= nums[i-1]) {
                    dp[i][w] = dp[i][w] || dp[i-1][w-nums[i-1]]; // pick
                }
            }
        }
        return dp[n][goal];
    }
};
```

## Pitfalls

### Base case 容易寫錯成「整列同值」
正確 base：`dp[0][0] = true`，**只有這一格**；`dp[0][w > 0]` 全是 false（用 0 個元素湊不出正和）。

常見錯誤是把 `dp[0][0..goal]` 全初始化成 `true` 或某個非零 int（後者更糟，會讓整張表都 truthy，永遠回傳 true）。**「用 0 個元素能湊出 0」是個 specific fact，不是普遍狀態**。

### Feasibility 用 `bool` + `||`，不要用 `int` + `+=`
看似 `+=` 更通用（多了「方案數」資訊），但對 416 這題：
- **Overflow**：subset 數量最壞 `2^n`，n = 200 時遠超 long long
- **失去 bitset 加速**：bitset 那招只能 bool
- **語意較弱**：debug 時看到 `dp[i][w] = 42` 要多想一層

選對工具：問什麼用什麼。問 feasibility 就用 bool。

### 內層 w 的方向（1D 版才要在意）
2D 版本兩個方向都可以（因為讀的是 `dp[i-1][...]`，跟當前 row 無關）。
**1D rolling 版必須倒著掃**（`for w = goal; w >= num; w--`），否則同個 `num` 會被重複使用，變成 unbounded knapsack。

### Pseudo-polynomial 不是真的 polynomial
LC 限制 `nums[i] ≤ 100` 才讓 DP work。如果題目給 `nums[i] ≤ 10^9`，DP 直接 OOM 不可行。要警覺這條線，不要看到 subset sum 就無腦上 DP。

## Optimization: 1D Rolling
```cpp
vector<bool> dp(goal + 1, false);
dp[0] = true;
for (int num : nums) {
    for (int w = goal; w >= num; w--) {     // 倒著掃
        dp[w] = dp[w] || dp[w - num];
    }
}
return dp[goal];
```
Space 從 O(n · goal) → O(goal)。

## Optimization: Bitset (最快)
```cpp
bitset<10001> dp;                           // goal ≤ sum/2 ≤ 10000
dp[0] = 1;
for (int num : nums) dp |= dp << num;
return dp[goal];
```
`dp[w] = 1` 代表「能湊出 w」。`dp << num` 是「全部可達 sum 都加 num」，`dp |= ...` 把「pick / not pick」兩條 path 聯集。CPU 一次處理 64 bits，常數比 1D bool 快約 30-50 倍。

## Related Problems
- [494] Target Sum — 0/1 knapsack **counting**（用 int + `+=`，正解就是 int 版），可轉化為 subset sum
- [474] Ones and Zeroes — 2D 0/1 knapsack（兩個 weight 維度）
- [322] Coin Change — **unbounded** knapsack min count（內層正向掃）
- [518] Coin Change II — unbounded knapsack counting
