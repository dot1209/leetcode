# [143] Reorder List
**Pattern:** [Linked List → In-place Rewiring](../../patterns/linked-list/in-place-rewiring.md)
**Complexity:** Time O(n), Space O(1)
**Link:** https://leetcode.com/problems/reorder-list/

## Trigger Signals
- `L0 → L1 → … → Ln` 要重排成 `L0 → Ln → L1 → Ln-1 → L2 → …`
- 要 in-place 修改 list，不能 new node、不能用 O(n) 額外空間
- 觀察：結果鏈是「前半正序 + 後半反序」交錯，因此要切兩半、反轉、合併

## Core Insight
三招組合：
1. **Slow/fast pointer 找中點**：把 list 拆成前後兩半（奇數時前半多一個）
2. **反轉第二半**：得到一條反序鏈
3. **交錯 merge**：把兩條鏈一個一個 zip 起來

關鍵設計：**用較短的那半（反轉後的第二半）當 merge 迴圈條件**，這樣奇偶長度自動處理，不需要 inner if。

## Complexity Analysis
- **Time O(n)**：三輪都是線性走 list（找中點 n/2、反轉 n/2、merge n/2）
- **Space O(1)**：只用了幾個指標變數，沒開新資料結構也沒遞迴

## Solution Code
```cpp
class Solution {
public:
    void reorderList(ListNode* head) {
        // find the mid
        auto slow = head, fast = head;
        while (fast->next != nullptr && fast->next->next != nullptr ) {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* pre = nullptr;
        ListNode* cur = slow->next;
        slow->next = nullptr;
        // first part = second part + 1 (odd)
        // first part = second part (even)
        while (cur != nullptr) {
            auto next = cur->next;
            cur->next = pre;
            pre = cur;
            cur = next;
        }
        // pre will point to the head of reversed list
        ListNode* first = head;
        ListNode* second = pre;
        // second part reach the end
        // pointed the last node in second part to first part implies the nullptr 
        while (second != nullptr) {
            auto fn = first->next;
            auto sn = second->next;
            first->next = second;
            second->next = fn;
            first = fn;
            second = sn;
        }
    }
};
```

Trace `1→2→3→4→5`：
- 找中點：slow=3，second half head=4
- Cut：1→2→3，second=4→5
- Reverse：5→4，prev=5
- Merge：p1=1, p2=5 → 1→5→2，p1=2, p2=4 → 2→4→3，p1=3, p2=null → 結束
- 結果：`1→5→2→4→3` ✓

Trace `1→2→3→4`：
- 找中點：slow=2，second half=3
- Cut：1→2，second=3→4
- Reverse：4→3，prev=4
- Merge：p1=1, p2=4 → 1→4→2，p1=2, p2=3 → 2→3 (3->next 本來就 null)，p1=null, p2=null
- 結果：`1→4→2→3` ✓

## Pitfalls
- **沒 cut 就反轉會 cycle**：`slow->next = nullptr` 必須在反轉前做，否則反轉後 second half 的尾巴會指回前半中間
- **Merge 迴圈條件**：用 `while (p2)` 而非 `while (p1)` 或 `while (p1 && p2)`。p2 一定 ≤ p1（奇數時 p1 多一個 node），p2 走完就結束；p1 那個多出來的 node 它的 `next` 已經被前一輪設好了，自然收尾
- **保存 next 再改 next**：每次改指標前先存 `t1 = p1->next; t2 = p2->next;`，否則後面找不到下一格
- **奇數長度 slow/fast 的偏向**：`while (fast->next && fast->next->next)` 讓 slow 停在前半最後一個（5 個 node 時停在第 3 個）；若改成 `while (fast && fast->next)` slow 會多走一步停在中間偏右
- **`head == nullptr` 或單 node**：要先擋掉，否則第一行 `fast->next` 就 deref nullptr

## Alternative Merge（內層 if 版本）

也可以用 first half 當主迴圈、用 `if (pre)` 處理奇偶。可讀性較差但邏輯也對：

```cpp
cur = head;
while (cur) {
    auto cur_next = cur->next;
    cur->next = p2;
    if (p2) {
        auto p2_next = p2->next;
        p2->next = cur_next;
        p2 = p2_next;
    }
    cur = cur_next;
}
```

差別在用「較長半」當主鏈，內層額外判斷「短半是否還在」。用「較短半」當主鏈可以消掉這個 if。

## Related Problems
- [206] Reverse Linked List — 反轉原語本身
- [876] Middle of the Linked List — 找中點原語本身
- [21] Merge Two Sorted Lists — merge 原語的另一種變體（這題交錯不比較）
- [25] Reverse Nodes in k-Group — 反轉的進階：每 k 個一段
