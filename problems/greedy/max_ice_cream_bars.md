# [1833] Maximum Ice Cream Bars
**Pattern:** [Greedy](../../patterns/greedy.md)
**Complexity:** Time O(n + maxVal), Space O(maxVal)
**Link:** https://leetcode.com/problems/maximum-ice-cream-bars/

## Trigger Signals
- 有固定預算 `coins`，要買**最多數量**的 ice cream（不是最高總價值，每支價值都一樣＝1 支）。
- 買某一支不會影響其他支能不能買（彼此獨立）→ 典型 sort-then-greedy。
- 值域有限（`1 ≤ costs[i] ≤ 1e5`）→ 排序可用 **counting sort** 取代 comparison sort，去掉 log。

## Core Insight
要最大化「買的支數」，就**從最便宜的開始買**。Exchange argument：任何一種最優買法，如果它沒買最便宜的那支、卻買了較貴的某支，把那次消費換成最便宜的那支，總支數不變、花的錢只會更少（不會超支）——所以「便宜先買」至少跟任何最優解一樣好。

排序這一步，因為 cost 落在 `[1, 1e5]` 的固定值域，用 **counting sort**（值域陣列計數）就能 O(n + maxVal) 完成，不必 comparison sort 的 O(n log n)。

## Complexity Analysis
- **Time O(n + maxVal)** — 建頻率表掃 `costs` 一次 O(n)；接著的雙層迴圈，外層固定跑 `maxVal = 1e5` 次、內層加總 `Σ freq[i] = n` 次，合計 O(maxVal + n)。**沒有 log 因子**——這才是真正的 counting sort。
- **Space O(maxVal)** — `freq` 是固定大小 `1e5+1` 的陣列，與輸入 n 無關。
- 因為 `maxVal` 在本題是常數（1e5），相對於輸入規模 n 來說，時間實際上是**線性**、額外空間是**常數級**；但寫成 O(n + maxVal) / O(maxVal) 才精確點出「成本來自值域大小」這件事。

## Solution Code
```cpp
class Solution {
public:
    int maxIceCream(vector<int>& costs, int coins) {
        // counting sort on costs
        constexpr int N = 100000;
        // step 1: frequency
        int freq[N+1] = {0};
        for (auto cost: costs) {
            freq[cost]++;
        }
        // step 2: sort
        int count = 0;
        for (int i = 1; i <= N; i++) {
            for (int j = 0; j < freq[i]; j++) {
                if (coins - i >= 0) {
                    coins -= i;
                    count++;
                }
            }
        }
        return count;
    }
};
```

## Notes / 可改進處（不改你的 code，另記於此）
1. **可以早停。** 值域是 ascending 掃描，一旦最便宜的剩餘 `i` 都買不起（`coins < i`），後面更貴的必然也買不起，外層可直接 `break`/`return count;`，省掉後面整段空轉（不影響最壞複雜度，但實務上常常很早就停）。
2. **`int freq[100001]` 開在 stack 上約 ~391 KB。** LeetCode 跑得過，但在預設 stack 較小的環境（某些執行緒只有 1 MB）會逼近上限；若想保險可改 `static`、`vector<int>` 或放到 heap，記憶體就不佔 call stack。

## Pitfalls
- 別被「max」誤導成要最大化價值——這題每支價值相同，所以是最大化**數量**，貪心方向是「便宜先」。
- counting sort 的前提是**值域有限且不大**；若 cost 範圍是 1e9，就不能開這麼大的陣列，得退回 comparison sort 的 O(n log n)。
- 早停的合法性建立在「依值域遞增掃描」之上；亂序就不能因為一支買不起而停。

## Related Problems
- [455] Assign Cookies — 同樣 sort-then-greedy，把最小的餅乾配給胃口最小的小孩。
