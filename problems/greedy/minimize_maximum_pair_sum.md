# [1877] Minimize Maximum Pair Sum in Array
**Pattern:** [Greedy](../../patterns/greedy.md)
**Complexity:** Time O(n log n), Space O(1)
**Link:** https://leetcode.com/problems/minimize-maximum-pair-sum-in-array/

## Trigger Signals
- 要把元素**兩兩配對**，並**最小化「所有配對和的最大值」**（minimize the maximum）→ 典型的 minimax 配對，sort 後頭尾相接。
- 配對決策彼此**獨立**（一個配對不影響其他配對能怎麼配）→ 可以用 exchange argument 證明貪心成立。
- 訊號詞：`pair up`、`minimize the maximum ...`。

## Core Insight
sort 之後，把**最小的配最大的**（`nums[i]` 配 `nums[n-1-i]`），答案就是所有配對和的 max。直覺是要「平衡」——把大的拉去跟小的配，避免兩個大的湊在一起把 max 撐高。

### Greedy property 的證明（exchange argument）
設陣列已排序，最小元素為 `a`、最大元素為 `d`。假設某個**最優配對沒有把 `a` 跟 `d` 配在一起**，那它必然包含兩個配對 `(a, x)` 與 `(d, y)`，其中 `a` 是全域最小、`d` 是全域最大，所以 `a ≤ y` 且 `x ≤ d`。現在把它們換成 `(a, d)` 與 `(x, y)`：

- `a + d ≤ d + y`（因為 `a ≤ y`）
- `x + y ≤ d + y`（因為 `x ≤ d`）

兩個新配對和都 `≤ d + y`，而 `d + y` 本來就出現在舊配對裡、已被算進舊的 max。所以這次交換**不會讓最大配對和變大**。對「最小配最大」反覆套用這個交換，就能把任何最優解逐步搬成頭尾相接的配對，而 max 不增 → 頭尾配對至少跟最優解一樣好。

另一個 lower-bound 直覺：最大元素 `d` 一定落在某個配對裡，跟它配的東西 `≥ a`，所以**任何**配對方式都有 max `≥ a + d`。頭尾配對對這個極端元素剛好打平這個下界，同時讓中間的配對盡量平衡。

## Complexity Analysis
- **Time O(n log n)** — 由 **sort 主導**；排序後只掃 `n/2` 次做配對與取 max，是 O(n)。
- **Space O(1)** — in-place sort，沒有用到與輸入等長的額外空間。（嚴格講 `std::sort` 是 introsort，遞迴會用 O(log n) stack；慣例上仍記為 O(1)，因為沒有 array 級別的額外空間。）

## Solution Code
```cpp
class Solution {
public:
    int minPairSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int res = 0;
        for (int i = 0; i < n/2; i++) {
            res = max(res, nums[i]+nums[n-1-i]);
        }
        return res;
    }
};
```

## Pitfalls
- **別只「想當然」配頭尾就交卷**——greedy 的正確性靠上面的 exchange argument，要先說服自己「最小配最大、max 不增」才算真懂這題。
- 配對索引是 `nums[i]` 與 `nums[n-1-i]`，迴圈只跑到 `n/2`；跑滿 `n` 會把每個配對算兩次（雖然 max 不變，但邏輯上重複）。
- 回傳的是配對和的 **max**，不是 min、也不是總和——題目要的是「最小化的那個最大值」。

## Related Problems
- [1833] Maximum Ice Cream Bars — 同屬 Greedy，但是「sort 後依預算逐一取用」的形式，跟本題「sort 後頭尾配對」是不同操作型態。
