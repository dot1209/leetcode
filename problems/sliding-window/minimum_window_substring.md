# [76] Minimum Window Substring
**Pattern:** [Sliding Window](../../patterns/sliding-window.md)
**Complexity:** Time O(S+T), Space O(σ)=O(1)
**Link:** https://leetcode.com/problems/minimum-window-substring/

## Trigger Signals
- 給 `s` 和 `t`,找 `s` 裡**最短**的連續子字串,使其涵蓋 `t` 的所有字元(**含重複次數**,`t="aabc"` 要有兩個 a)
- 「連續區間 + 涵蓋一組目標 + 求最短」→ variable-size sliding window
- 暴力解(枚舉每個起點往後找)是 O(S²·σ),相鄰視窗只差頭尾 → 可增量

## Core Insight
節奏是「**擴右 → 縮左 → 再擴右**」:
1. 右指針 `r` 一直把字元吃進視窗,直到視窗**裝齊** `t`。
2. 一旦裝齊,左指針 `l` 一直縮,縮到「再縮就不合法」為止;**縮的過程中更新最短答案**。
3. 縮到不合法後回到 1,繼續擴 `r`。

合法性怎麼判斷才不會慢?——不要每步重掃整個視窗(那是 O(σ)/步)。維護一個 `formed` = 「目前有幾種必要字元的數量已達標」,`formed == required`(t 的 distinct 數)就是合法,O(1)。`formed` 只在「某字元剛好跨過門檻」時增減。

## Complexity Analysis
- **Time O(S+T)**:建 `need` 表 O(T);主迴圈裡 `l`、`r` 各自只單調往右走過 S 次,每步 O(1)。內層 while 的總次數被 `l` 的總移動量 ≤ S 攤還掉,不是 O(S²)。
- **Space O(σ) = O(1)**:`need` 與 `win` 兩個計數,被字母表 σ(≤128)封頂,與 S、T 無關。

**和未優化版的對比(容易算錯的地方)**:用 `is_ok` 逐字元比對整個 `target` 的版本,每步檢查是 **O(σ)**(σ = t 的 distinct 數,不是 S),總共 **O(S·σ)**。因為 σ 是常數,它技術上仍是 O(S),只是常數很肥——**不是 O(S²)**。要真的 O(S²),檢查得掃「與視窗長度成正比」的東西(例如每步重數整個視窗、或拿 O(S) 長的 substr 去比)。

## Solution Code
```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        unordered_map<char, int> target;
        for (auto c : t) {
            target[c]++;
        }
        int l = 0, final_l = 0;
        unordered_map<char, int> tmp;
        int best_l = 0, best_len = s.size() + 1;
        int formed = 0;
        int required = target.size();
        for (int r = 0; r < s.size(); r++) {
            tmp[s[r]]++;
            if (tmp[s[r]] == target[s[r]]) {
                formed++;
            }
            while (formed == required) {
                // update res
                if (r - l + 1 < best_len) {
                    best_len = r - l + 1;
                    best_l = l;
                }
                // shrink
                if (tmp[s[l]] == target[s[l]]) {
                    formed--;
                }
                tmp[s[l]]--;
                l++;
            }
        }
        return best_len == s.size() + 1 ? "" : s.substr(best_l, best_len);
    }
};
```

## Pitfalls

### `unordered_map::operator[]` 會偷插 key → 汙染 `size()`
若用 map 版寫成 `if (tmp[s[r]] == target[s[r]])`,當 `s[r]` 不在 `t` 裡,`target[s[r]]` 會**插入一個 value=0 的 entry**,讓 `target.size()` 從 distinct(t) 一路膨脹(實測 `ADOBECODEBANC`/`ABC` 會從 3 變 7)。若判斷式是 `while (formed == target.size())`,右邊偷偷變大、`formed` 最多只到 3 → 條件永遠 false → shrink 一次都沒跑 → 回傳 `""`(WA)。
- **修法 A(推薦)**:用 `int[128]` 陣列,沒有「key 不存在」的概念,`need[foreign]` 天生是 0,不會長出來。
- **修法 B**:開頭存 `int required = target.size();`,之後判斷用 `required`,查詢用 `.count()` / `.find()` 而非 `operator[]`。

### `formed` 的增減時機
- 加:`win[c] == need[c]`(用 `==`,只在剛好達標那次 +1;`>=` 會重複加)。
- 減:在 `win[cl] == need[cl]` 時 `formed--`,且必須在 `win[cl]--` **之前**(抓「即將跌破」)。

### 把 `substr` 留到最後
別在內層 while 裡每次 `res = s.substr(...)`;只記 `best_l`/`best_len`,迴圈結束才 substr 一次,省掉反覆的字串配置。

## 一段除錯實錄(關於 MLE 與記憶體的觀念)
這題我一度懷疑某版本 MLE,過程中釐清了幾個常見誤解:
- `s.substr(pos, len)` 的 `len` 算成負的**不會**配置巨大字串——它是 `size_t`,會被 clamp 成 `min(len, size()-pos)`(實測 `substr(0, -1)` 對 `"abc"` 回傳 `"abc"`)。`pos > size()` 則是丟 `out_of_range`,屬 Runtime Error 而非 MLE。
- 「substr 一直複製」也**不會** MLE:`res = s.substr(...)` 會釋放舊值,任何時刻只有一份活著。**MLE 量的是峰值同時佔用,不是累計配置量**。
- 真正會吃記憶體的是 `unordered_map` 的 per-node 開銷;換成 `int[128]` 陣列可把額外空間壓到固定 O(1)。

## Related Problems
- [567] Permutation in String — 幾乎同款,維護「已匹配字元種數」,fixed window
- [438] Find All Anagrams in a String — 同 567,收集所有起點
- [340] Longest Substring with At Most K Distinct Characters — 摘要值改成「視窗內 distinct 數」
- [3] Longest Substring Without Repeating Characters — variable window 入門款
