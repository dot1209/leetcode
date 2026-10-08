# [410] Split Array Largest Sum

**Pattern:** [Binary Search on Answer](../../patterns/binary-search.md)
**Complexity:** Time O(n log(S - M + 2)), Space O(1)
**Link:** https://leetcode.com/problems/split-array-largest-sum/

## Trigger Signals

- 陣列切成剛好 `k` 個連續、非空的 subarrays，最小化其中最大的 sum。
- 元素非負，所以一組加入更多元素時，總和不會下降。
- 與其枚舉所有切法，先固定一個 cost，判斷能不能在這個限制下完成分組。
- 官方限制為 `1 <= n <= 1000`、`0 <= nums[i] <= 10^6`、`1 <= k <= min(50, n)`。

## Core Insight

我的想法是「用二分搜來搜可能的 cost」：每回合猜一個上限，當目前 `sum + nums[i]` 超過這個上限就先切一刀；如果組數不超過 k，就試試看更小的 cost。

比較的是 sum 與候選 cost m，不是 sum 與 k。k 是組數；剛好 k 組只需要 k 減一刀。

## Why It's Correct

### 固定 cap 時，greedy 得到最少組數

Greedy 的每一組都盡量往右延伸。第一組若已放到 index i，但加入下一個元素就超過 cap，任何合法解的第一刀都「不可能」切在更後面：非負數讓再延伸也無法降低總和。

更完整的論證是 greedy 的切點始終領先。假設 greedy 在前 g 減一組後的切點不早於任一合法切法：

- 若它已走到那個合法切法第 g 組的結尾，就已領先。
- 否則，它接下來要走到該結尾，只需涵蓋合法第 g 組的一段 suffix；非負數保證這段 suffix 的 sum 不大於整組，因此也不超過 cap。

所以 greedy 第 g 組的結尾仍不會更早。若有合法解用 q 組覆蓋全部元素，greedy 至多也用 q 組，因此它得到最少組數。

### 為什麼 groups 小於 k 也算可行

我的理解是：即使組數少於 k，依舊可以從有兩個以上 elements 的組裡面補切到 k 為止，拆開不會讓 cost 變大。

精確條件是 `groups < k <= n`，因此一定還有一組包含至少兩個元素，可以繼續拆。元素是非負數，不一定全是正數；拆開後每個部分的 sum 都不會大於原本，因此最大組 sum 不會增加。只需至少兩個元素，不必超過兩個。

所以 `groups <= k` 等價於可以切成剛好 k 個非空組；反過來，若 greedy 已需要超過 k 組，就不存在合法的 k 組方案。

### 為什麼 cost 可以二分搜尋

若某個切法在 cap 下可行，同一個切法在更大的 cap 下仍然可行；因此可行值形成一段連續的上方值域。搜尋第一個可行 cost，就是最小可能的最大組 sum。

### 下界、右界與半開區間的語意

令 `M = max(nums)`、`S = sum(nums)`。每個元素不可拆開，最大的元素一定屬於某一組，而該組 sum 至少是 M，所以任何小於 M 的 cost 都不可行。

S 可行：先把全部元素視為一組，再拆成剛好 k 組，非負數保證各組 sum 不超過 S。使用者選擇 `l = M`、`r = S + 1`，其中 r 同樣可行。

這份 `[l, r)` 模板維護的是：

- 所有小於 l 的 cost 都不可行。
- r 已知可行，是尚待搜尋區間外的邊界。
- `[l, r)` 的值仍待搜尋；真正答案可能等於 r，不能宣稱答案永遠位於這個半開區間內。

只有 check 通過時才把 r 更新成 m，所以「r 更新的值永遠是被 check 過的」是對的；初始 r 則由 S 的可行性直接保證。當 m 可行，更新 `r = m`；當 m 不可行，更新 `l = m + 1`。結束時 l 與 r 相同，該值可行，所有更小值都不可行，回傳任何一者都正確。

## Complexity Analysis

令 `W = S - M + 1`，就是初始 `[M, S + 1)` 的寬度。

- 初始化最大值與總和各掃描一次，共 O(n)。
- 每次 solve 最多掃過 n 個元素，耗時 O(n)。
- 每輪二分搜尋將寬度約減半，共 O(log(W + 1)) 輪；加一也涵蓋全部為零、寬度為一時仍需一次判定的情況。
- 所以時間是 O(n log(S - M + 2))，不是直接 O(n log n)：搜尋的是可能的 cost，不是 n 個陣列位置。
- 只有邊界、累加和與組數，沒有額外容器或遞迴，因此空間是 O(1)。

## Solution Code

### 使用者的最終版本

保留原始命名、型別、迴圈與註解；沒有加入後來建議的 early return。

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        long long l = *max_element(nums.begin(), nums.end());
        long long r = accumulate(nums.begin(), nums.end(), 0LL) + 1;
        while (l < r) {
            // search cost m
            int m = (r - l) / 2 + l;
            // Search unresolved values in [l, r).
            // Values below l are infeasible; r is feasible.
            if (solve(nums, k, m)) {
                r = m;
            } else {
                l = m + 1;
            }
        }
        return r;
    }

private:
    bool solve(vector<int>& nums, int k, int m) {
        int sum = 0;
        int groups = 1;
        for (int i = 0; i < nums.size(); i++) {
            // impossible result
            if (nums[i] > m) {
                return false;
            }
            if (sum + nums[i] <= m) {
                sum += nums[i];
            } else {
                groups++;
                sum = nums[i];
            }
        }
        return groups <= k;
    }
};
```

### 補充解法：DP 枚舉最後一刀

這是另一種值得學的建模方法，並非取代使用者的程式。`dp[i][g]` 表示前 i 個元素切成剛好 g 組時，最小可能的最大組 sum；枚舉最後一組從 j 開始：

`dp[i][g] = min over j { max(dp[j][g - 1], prefix[i] - prefix[j]) }`。

時間 O(k·n²)，空間 O(k·n)。它比較慢，但直接列舉所有最後一刀的位置，且仍適用於負數。`dp[0][0]` 用負無窮，讓第一組的 sum 可以是負值；若用零，會把全負陣列的答案錯誤夾成至少零。

```cpp
class DpSolution {
public:
    long long splitArray(const vector<int>& nums, int k) {
        int n = nums.size();
        vector<long long> prefix(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }

        const long long INF = numeric_limits<long long>::max() / 4;
        const long long NEG_INF = numeric_limits<long long>::lowest();
        vector<vector<long long>> dp(n + 1, vector<long long>(k + 1, INF));
        dp[0][0] = NEG_INF;

        for (int g = 1; g <= k; g++) {
            for (int i = g; i <= n; i++) {
                for (int j = g - 1; j < i; j++) {
                    if (dp[j][g - 1] == INF) {
                        continue;
                    }
                    long long lastSum = prefix[i] - prefix[j];
                    dp[i][g] = min(dp[i][g], max(dp[j][g - 1], lastSum));
                }
            }
        }

        return dp[n][k];
    }
};
```

## Alternatives / Optimization

### 組數超過 k 就提早結束

`groups > k` 時，後面繼續掃描只會維持或增加組數，因此可直接回傳 false。不加仍正確，這是減少不必要掃描的常數優化，最壞時間階不變。

### 更緊的下界

除了 M，也可以使用 `ceil(S / k)`：所有組的總和為 S，最大組總和不可能低於平均。初始化可設為 `max(M, (S + k - 1) / k)`。使用者目前的 M 下界已正確，這只是可選的收緊。

### DP 可以 rolling 壓縮

DP 只依賴上一個組數 g 的那一層，可以保留前後兩列，把額外空間從 O(k·n) 壓成 O(n)。完整表較容易搭配切點紀錄回傳實際切法。

## Pitfalls

- 起初 `groups = 0` 配上 `groups <= k`，會把切刀數當成組數；應從一組開始算。
- cap 小於某個元素時，切一刀後直接 `sum = nums[i]`，依舊是非法組。從零開始搜尋本身不會錯，錯的是判定沒有拒絕這種狀態。
- 下界要用 `max_element`，不是 `min_element`。兩邊保護都可以保留：正確下界避開不可能的候選，`num > cap` 讓判定函式單獨使用時也正確。
- 加入下一個元素前比較 `sum + nums[i] > cap`，不是跟組數 k 比較。
- r 是可行右界，不代表已是最小可行值；「答案永遠在 `[l, r)`」不正確，因為 `r = m` 可以正好保留最佳答案。
- 題目保證輸入非空；要檢查單元素、全零、`k = 1`、`k = n` 與最大總和。`k = n` 時也仍須符合官方的 k 上限。

## Side Notes

### int 與 long long

官方限制使 S 最多為 `10^9`，因此原始程式的 `int m`、`int sum` 與 int 回傳值都安全。初始右界是 S 加一，而 m 一定小於 r；暫時累加的元素也只是整個陣列的一部分，不會超過 S。

`accumulate(..., 0LL)` 讓累加型別是 long long；若將來放寬題目限制，還必須一起檢查 m、判定中的 sum 與回傳型別，不能只放大二分邊界。統一使用 long long 是更泛用的選擇，不是這題原始碼必須修正的 correctness bug。

### 初始右界不必一律加一

使用者採用 S 加一作為 sentinel。這個更新模板也能從已知可行的 `r = S` 開始；`[l, r)` 描述的是尚待搜尋值，右界自身已保留為可行候選，所以沒有「半開區間一律必須加一」的規則。

## Follow-ups

### 回傳實際切法

先求最佳 cap，再以相同 greedy 記錄各組區間，會得到不超過 k 組。若需要剛好 k 組，就繼續拆開任一個至少有兩個元素的組；非負數保證不會增加 cost。

回傳切點或區間邊界需要 O(k) 輸出空間；若直接複製所有 subarrays，還需 O(n) 輸出空間。一次建構時也可以保留足夠元素給剩餘組，但必須明確定義目前組與尚未分配的元素，避免強制切割條件 off by one。

### 若允許負數

例如 `[10, -9, 10, -9]`、`k = 2`、`cap = 1`，可以切成兩個 `[10, -9]`，每組 sum 都是一。但目前 greedy 會因單一元素 10 大於 cap 而拒絕；負數也可能使暫時超標的 sum 稍後下降，不能超過就立刻切。

有三個前提一起失效：

- 單一最大元素不再是答案下界，因為可以被同組的負數抵銷。
- 拆開不保證 cost 不增加，因此「最少組數不超過 k」不再等價於「剛好 k 組可行」。
- 全部放成一組的總和不一定能當成剛好 k 組的可行上界。

對「是否存在剛好 k 組、各組 sum 不超過 cap」的判定，隨 cap 放寬的單調性依然成立；壞掉的是目前的 greedy 與邊界推導。前述 exact-k DP 可以直接處理這個延伸。

### 改成最大化最小組 sum

可改成「每組至少有多少」的判定：非負數情況下累加到下限就切出一組，檢查能否湊足目標組數。多出的組可以合併，仍不會低於下限。可行值會從小到大由真轉假，所以要找最後一個可行下限；不能照抄最小容量的更新方向。

## Related Problems

- [1011] [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) — 按原順序運貨，搜尋最小容量；greedy 判定所需天數，核心與本題相同。
- [1231] [Divide Chocolate](https://leetcode.com/problems/divide-chocolate/) — 連續分組但改成最大化最小 sum，對照可行性的方向與切割時機。
- [875] [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) — 搜尋最小可行速度，判定改成累加每堆需要的時間。
