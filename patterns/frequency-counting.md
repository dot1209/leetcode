# Frequency Counting

Frequency counting 的核心動作只有一個：**先掃一遍把每個元素出現幾次記下來，再從這張計數表推出答案**。它的價值在於把「問某個元素出現幾次 / 某種組合能湊幾組 / 兩堆東西組成是否一樣」這類問題，從「每次都重新數」壓成「數一次、之後 O(1) 查表」。一旦計數表建好，答案通常只是對表做一次簡單的彙整——取 min、比對兩張表是否相等、找第一個次數為 1 的位置等等。

最常見的具體形式是 **bottleneck min**：要用手上的字元拼出某個目標字（如 `balloon`），每個目標字母需要的份數不同（`l`、`o` 各要 2 份），那麼能拼出的組數 = `min(擁有量 / 需要量)`——卡在「最稀缺的那個字母」上，所以叫 bottleneck。

計數表的載體有兩種選擇：值域固定且小（如只有小寫字母 26 個）就用**固定陣列** `int freq[26]`，O(1) 空間又快取友善；值域大或不連續（任意整數、字串 key）才用 **hash map**。

## When to Use
- 問題只關心**每個元素出現幾次**，不關心它們的順序或位置 → 順序資訊可以直接丟掉
- 要判斷兩個集合「組成是否相同」（anagram）、或一堆字元「能否湊出 / 湊幾組」目標
- 訊號詞：`how many times`、`can construct / form`、`anagram`、`maximum number of "<word>"`、`first unique`、`appears more than ...`
- 只在乎「有**幾種**不同的值」而非哪個值 → 退化成 **count distinct**：用 presence set / bitset 標記出現過的元素，再數 key 的個數（如 [2357]）
- 值域有限（小寫字母、ASCII、固定範圍整數）特別適合——用陣列當計數表就好
- **bottleneck 形式的訊號**：要用一袋字元重複拼出某個固定 pattern，且 pattern 內字母有重複 → 答案是 `min(have / need)`

## Typical Complexity
**Time:** O(n + k) — 建表掃過全部 n 個元素是 O(n)；之後從計數表推答案是掃過值域 / distinct key 的數量 k（字母表就是常數 26）。所以實務上幾乎都是 **O(n)**，因為 k 要嘛是常數、要嘛 ≤ n。
**Space:** O(k) — 計數表的大小由**值域**決定，不是輸入長度：固定字母表是 O(1)（26 格與 n 無關），任意 key 的 hash map 最壞是 O(n)（全部不重複）。

關鍵理解：時間花在「建表」那一遍線性掃描上，推答案那步通常是對固定大小的表做彙整、不隨 n 增長。想知道是 O(1) 還是 O(n) 空間，看的是 **key 的值域**而不是元素個數。

## Template Code
```cpp
// 1. Count occurrences into a fixed-size table (small known alphabet).
int freq[26] = {0};
for (char c : s) freq[c - 'a']++;

// 2. Derive the answer from the table. Examples:
//    - bottleneck: how many full copies of a target word can we build?
//      answer = min over required letters of (freq[letter] / need[letter])
//    - anagram check: compare two freq tables for equality
//    - first unique: scan for the first element whose count == 1
```

## Pitfalls
- **bottleneck 要先除以「需要的份數」再取 min。** 目標字裡重複出現的字母（`balloon` 的 `l`、`o` 各 2 個）必須用 `freq / 2` 再進 `min`，忘了除就會高估能拼的組數。
- **選錯計數表載體。** 值域固定且小就用陣列（快、省、無 hash 開銷）；只有在 key 是任意整數 / 字串時才用 hash map。反過來對 26 個字母開 `unordered_map` 是浪費。
- **整數除法是有意的，不是 bug。** `freq / need` 用整除正是要「湊不滿一組就不算」，這正確；別誤把它改成浮點。
- **大陣列開在 stack 上的風險。** 值域很大時（如 `int freq[100001]`）固定陣列會吃掉不少 stack 空間，必要時改 `static` / `vector` / heap。

---

## Problems

### [[1189] Maximum Number of Balloons](../problems/frequency-counting/max_number_of_balloons.md)
**Complexity:** Time O(n), Space O(1)
- **Trigger:** 用 `text` 裡的字元重複拼 `balloon`，問最多拼幾個 → 經典 bottleneck min
- **Insight:** 數出每個字母擁有量，答案 = `min(freq[c] / need[c])`，卡在最稀缺的字母；`l`、`o` 需要 2 份所以要先除以 2
- **Pitfall:** `l`、`o` 忘了除以 2 會高估；`b`、`a`、`n` 的 `/1` 是 no-op（可省，留著無害）

### [[2357] Make Array Zero by Subtracting Equal Amounts](../problems/frequency-counting/make_array_zero.md)
**Complexity:** Time O(n), Space O(1)（bitset 解；原本的 sort 解是 O(n log n)）
- **Trigger:** 只在乎有幾種不同的非零值、不在乎順序 → count distinct
- **Insight:** 每次操作剛好消掉「一種」最小的非零值，所以答案 = 相異非零值的個數；用 set / bitset 直接數 distinct 即可
- **Pitfall:** 0 不算一次操作要排除；答案跟「數值大小」無關只跟「有幾種」有關；值域小（0..100）時 bitset 最優（O(n)/O(1) 又不動原陣列）

### [[3517] Smallest Palindromic Rearrangement I](../problems/frequency-counting/smallest_palindrome.md)
**Complexity:** Time O(n), Space O(n)
- **Trigger:** 回文重排成字典序最小 → 只在乎每個字母有幾個 → 建 freq 表推結構
- **Insight:** 每字母取一半、`a→z` 升序排成前半段（字典序最小），奇數字母放正中間，後半段鏡射；回文保證頂多一個奇數字母
- **Pitfall:** `reserve` 只改 capacity 不改 size（要用 index 寫先 `resize`）；space 是 O(n) 不是 O(1)（`half`/`rev` 隨 n 成長）；SSO 是 library 技巧、非 compiler optimization
