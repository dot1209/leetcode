# [2357] Make Array Zero by Subtracting Equal Amounts
**Pattern:** [Frequency Counting](../../patterns/frequency-counting.md)
**Complexity:** Time O(n), Space O(1) — bitset 解（值域固定 1..100）；原本的 sort 解是 O(n log n) time，hash set 版是 O(n) time / O(n) space
**Link:** https://leetcode.com/problems/make-array-zero-by-subtracting-equal-amounts/

## Trigger Signals
- 問「最少幾次操作把陣列歸零」，但每次操作是「對所有正元素減同一個量」→ 真正決定答案的不是數值大小，而是**有幾種不同的非零值**。
- 只在乎「有哪些相異值」、完全不在乎順序或位置 → 順序資訊可以丟掉，把問題壓成 **count distinct**，正是 frequency / presence table 的味道。

## Core Insight
**答案 = 相異非零值的個數，因為每次操作剛好消掉「一種」最小的非零值。**

最佳策略永遠是每次都減掉當前最小的非零元素：這一步會把所有等於該最小值的元素一起歸零。每一種不同的非零數值，剛好對應一次操作，所以答案就是相異非零值的個數。程式用 `bitset<101>` 當 presence table：值域固定在 1..100，把每個出現過的正值 `set` 起來，最後 `count()` 就是相異非零值的種數。

## Why It's Correct
### 為什麼「每次最多消掉一種值」（lower bound + 可達）
- 每次操作對**所有正元素減同一個 x**，本質是一次「平移」：兩個不同的正值減掉同樣的量後仍然不同 → 相異正值不會因為操作而合併，除非剛好歸零。
- 只有**等於 x** 的值會歸零，而題目限制 `x ≤ 最小非零值`，所以一次最多只能讓「最小的那一種」值歸零 → 相異非零值的種數每次最多減 1 → **至少**需要 k 次。
- 反過來，每次取 `x = 當前最小值`，剛好每次減 1 種 → k 次就**做得到**。上下界夾出答案 = k = distinct non-zero count。

## Complexity Analysis
- **Time O(n)** — 只掃一遍 `nums` 設定對應的 bit；最後的 `count()` 是對固定 101 bits 做 popcount，與 n 無關（視為 O(1)）。沒有排序，所以整體是線性。
- **Space O(1)** — `bitset<101>` 固定 101 bits，大小由**值域**（0..100）決定，與輸入長度 n 無關。

## Solution Code
```cpp
class Solution {
public:
    int minimumOperations(vector<int>& nums) {
        bitset<101> b;
        for (auto x: nums) {
            if (x > 0) {
                b.set(x);
            }
        }
        return (int)b.count();
    }
};
```

## Alternatives / Optimization
- **原本的做法（sort + 數相鄰不同值）：** 排序後用 `cur`（初始 0）數「值有變化」的次數；`cur` 從 0 起跳，天然把 0 濾掉。正確，但瓶頸在 `sort` → `O(n log n)` time，而且會**改動原本的 `nums`**。bitset 版把時間壓到 `O(n)`、又不動原陣列，所以升為主解。
  ```cpp
  class Solution {
  public:
      int minimumOperations(vector<int>& nums) {
          int cur = 0;
          int cnt = 0;
          sort(nums.begin(), nums.end());
          for (auto x: nums) {
              if (x != cur) {
                  cur = x;
                  cnt++;
              }
          }
          return cnt;
      }
  };
  ```
- **Hash set（值域不固定時的通用寫法）：** bitset 能用是因為這題值域剛好固定在 1..100；若值域大或不連續，就改用 `unordered_set` 裝非零值再回傳 `size()`。時間 `O(n)`、空間 `O(n)`，同樣不動原陣列。
  ```cpp
  int minimumOperations(vector<int>& nums) {
      unordered_set<int> s;
      for (int x : nums)
          if (x != 0) s.insert(x);
      return s.size();
  }
  ```

## Pitfalls
- **0 不算一次操作，必須排除。** bitset 版靠 `if (x > 0)` 只標記正值，**絕不能 `set(0)`** —— 一旦把 index 0 也設起來，`count()` 就會多算一次。（sort 版則是靠 `cur` 從 0 起跳跳過 0。）
- **是「相異值的個數」不是「最大值」。** 直覺容易誤以為要一直減到最大值歸零 = 某個數值，但答案跟數值大小無關，只跟「有幾種」有關。
- **bitset 合法的前提是值域固定又小。** 這題 `0 <= nums[i] <= 100` 才能開 `bitset<101>`；若值域大或不連續，固定表會爆掉或浪費，要改用 `unordered_set`。

## Related Problems
- [1189] Maximum Number of Balloons — 同 frequency-counting，一樣是「建計數表再從表推答案」，只是那題取 `min(have/need)`、這題數 distinct。
- [217] Contains Duplicate — 同樣用 set 追蹤相異元素，只是問「有沒有重複」而不是「有幾種」。
- [1207] Unique Number of Occurrences — 先建頻率表，再看這些「出現次數」本身是否有重複，也是從計數表二次推答案。
