# [1358] Number of Substrings Containing All Three Characters
**Pattern:** [Sliding Window](../../patterns/sliding-window.md)
**Complexity:** Time O(N), Space O(1)
**Link:** https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/

## Trigger Signals
- 字串只含 a/b/c，問**有幾個** substring 同時含齊三種字元 → 連續區間 + 計數 → sliding window 的「計數變體」。
- 訊號是「count substrings containing all of ...」：不是求最長／最短，而是數個數。合法性隨長度單調（視窗越長越容易裝齊），所以對每個右端點可以 O(1) 算出合法左端點的數量。
- 暴力枚舉所有 (l, r) 是 O(N²)；相鄰右端點的狀態只差頭尾 → 可增量維護。

## Core Insight
核心轉念：**不要去數「總共有幾個合法 substring」，而是固定右端點 `r`，數「以 `r` 結尾的合法 substring 有幾個」，再全部加起來。**

關鍵單調性：若 `[left, r]` 已裝齊 a/b/c，那麼把左界往左推得到的 `[left-1, r]`、`[left-2, r]`、…、`[0, r]` **也都合法**（往左只會多加字元，不會弄丟已有的字元）。所以合法起點是一段前綴 `0..L`，只要知道**最大的合法起點 `L`**，以 `r` 結尾的合法 substring 數量就是 `L + 1`。

這題有兩個 O(N)／O(1) 解法，差別只在「怎麼維護 L」以及「用半開還是閉區間記數」——剛好是 off-by-one 慣例的活教材。

### 解法一：縮放視窗（shrink while valid）
右指針吃字元；一旦視窗裝齊三種，就一直縮左指針直到**剛好不合法**為止。跳出 while 時 `l` 停在「第一個讓視窗不合法的起點」，也就是合法起點集合 `[0, l)` 的**開區間右界**——這段裡有 `l` 個合法起點，所以 `res += l`。

注意這裡加的是 `l` 而非 `l + 1`：while 是「**還合法就縮**」，所以它會多縮一步、停在不合法處，`l` 已等於「最大合法起點 + 1」。`l` 是 `[0, l)` 的開（exclusive）右界，記數 = 右界 − 左界 = `l`，天生沒有 `+1`。

### 解法二：記最後出現位置（last occurrence）
換個視角：對每個右端點 `r`，維護 a/b/c 各自**最後一次出現的 index**。`[k, r]` 要裝齊三種 ⟺ `k` 不能超過任何字元的最後出現位置，所以最大合法起點 `L = min(last[a], last[b], last[c])`，合法起點是 `0..L` 共 `L + 1` 個，故 `res += min(last) + 1`。某字元還沒出現時 `last = -1`，`min` 為 -1、`+1` 後加 0，自動處理「還沒湊齊」的情況。

### 兩解的橋：半開 `l` vs 閉區間 `L + 1`
兩個解算的是**同一個量**（以 r 結尾的合法起點數），只是用不同的區間慣例編碼：
- 解法一的 `l` 是合法起點集合 `[0, l)` 的**開**（exclusive）右界 → 記數 `= l`。
- 解法二的 `min(last)` 是最大合法起點 `L`，對應**閉**區間 `[0, L]` → 記數 `= L + 1`。
- 兩者數值相等：`l == L + 1`。這就是「為什麼解法一加 `l` 而不是 `l+1`」的答案——閉區間天生帶 `+1`，開區間沒有。

## Complexity Analysis
- **Time O(N)**：
  - 解法一：`l`、`r` 各自只單調往右走過 N 次，內層 while 的總執行次數被 `l` 的總移動量 ≤ N 攤還掉，不是 O(N²)。
  - 解法二：單一迴圈，每步對三個數取 `min` 是 O(1)。
- **Space O(1)**：兩者都只用固定大小的 `cnt[3]`／`last[3]`，與 N 無關。
- 解法二額外有一個性質：它**只讀當前字元 `s[r]`**（解法一需回看 `s[l]` 來減計數），所以是真正的 streaming／單趟不回看解；輸入若是無法整段儲存的字元流，解法一得緩衝到目前視窗。

## Solution Code

### 解法一：縮放視窗
```cpp
class Solution {
public:
    int numberOfSubstrings(string s) {
        // if [left, r] is a valid substring
        // [left-1, r], [left-2, r], ..., [0, r] are also valid substrings
        int cnt[3] = {0};
        int l = 0;
        int res = 0;
        for (int r = 0; r < s.size(); r++) {
            cnt[s[r] - 'a']++;
            while (cnt[0] && cnt[1] && cnt[2]) {
                cnt[s[l] - 'a']--;
                l++;
            }
            // invalid
            res += l;
        }
        return res;
    }
};
```

### 解法二:記最後出現位置
```cpp
class Solution {
public:
    int numberOfSubstrings(string s) {
        // Count valid substrings grouped by their right end r.
        // [k, r] is valid  <=>  k <= the last occurrence of every char,
        // so the largest valid start is L = min(last[a], last[b], last[c]),
        // which gives starts 0..L  ->  L + 1 valid substrings ending at r.
        int last[3] = {-1, -1, -1};                 // last seen index of a, b, c
        int res = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            last[s[r] - 'a'] = r;
            // Any char still unseen -> its last is -1 -> L = -1 -> adds 0
            // (correct: no valid substring exists yet).
            // ex: s = "ccabc", at r = 3 -> last = {a:2, b:3, c:1} -> L = 1
            //     -> starts {0, 1} -> L + 1 = 2 ("ccab", "cab")
            res += min({last[0], last[1], last[2]}) + 1;
        }
        return res;
    }
};
```

## Pitfalls
- **解法一加 `l`、解法二加 `min(last) + 1`，別搞混**：同一個量的開／閉區間兩種寫法。解法一寫成 `res += l + 1` 會多算（`l` 已是「最大合法起點 + 1」）；解法二漏掉 `+1` 會少算。判準：手上那個界是「最後一個合法起點」（閉，要 +1）還是「第一個不合法起點」（開，不用 +1）。
- **`int last[3] = {-1}` 不會把三個都設成 -1！** C++ aggregate 初始化只把列出的值由前往後填，沒列到的元素一律 value-initialize 成 0 → 實際是 `{-1, 0, 0}`。要全 -1 必須寫滿 `{-1, -1, -1}`（或 `fill` / `memset(last, -1, sizeof last)`——`memset` 能用是因為 byte `0xFF` 重複即 -1，但對非 0／-1 的填充值不成立，例如 `memset(.., 1, ..)` 會得到 `0x01010101`）。`{0}` 看似「會廣播」純屬巧合：補的 0 剛好等於你要的值；換成非 0 的值就會中招。
- **`res` 的型別**：本題 `n ≤ 5×10⁴`，答案最大 `n(n+1)/2 ≈ 1.25×10⁹`，仍 < `INT_MAX`（≈ 2.14×10⁹），`int` 夠用；但邊際不大，`n` 再大些（≳ 65535）就溢位，需換 `long long`。
- **`r < s.size()` 的 signed／unsigned 比較**：`r` 是 `int`、`s.size()` 是 `size_t`，會觸發 `-Wsign-compare`；`int n = s.size();` 再比 `r < n` 可消除（解法二已用 `(int)` cast）。

## Follow-ups
- **推廣到任意字元集 / k 種必要字元**：把寫死的 `cnt[0] && cnt[1] && cnt[2]` 換成 LC76 那套 `formed == required` 計數器（`formed` = 已達標的 distinct 字元種數），記數一樣 `res += l`。LC76、LC30、本題其實是同一副骨架，只差「合法判斷」怎麼寫。
- **`atMost(K)` 家族**：因為 `s` 只含 a/b/c，「裝齊三種」⟺「**剛好 3 種 distinct**」= `atMost(3) − atMost(2)`。`atMost(K)` 視窗（每步加 `r - l + 1`，正是本題的上界鏡像）配上恆等式 `exactly(K) = atMost(K) − atMost(K-1)`，可解一大票「subarray／substring 恰好／至多 K 種」的題。

## Related Problems
- [76] Minimum Window Substring — 同樣「裝齊一組目標字元」，但求最短而非計數；`formed` 計數器可直接套用。
- [3] Longest Substring Without Repeating Characters — variable window 計數入門，合法性反向（每字元至多 1 次）。
- [340] Longest Substring with At Most K Distinct — `atMost(K)` 視窗本體。
- [992] Subarrays with K Different Integers — `exactly(K) = atMost(K) − atMost(K-1)` 的代表題。
