# Linked List — In-place Rewiring

## When to Use
題目要求把 list 改變結構，但**不允許開新 node、不能用額外 O(n) 空間**。核心動作是把現有 node 的 `next` 指標重新接線。

常見子題型：
- **Reverse**：整段或部分反轉
- **Reorder / Interleave**：先切兩半、反轉其中一半、再交錯合併
- **Rotate**：把尾巴接到頭、頭斷在某處
- **Swap pairs**：相鄰兩兩交換
- **Remove**：刪掉某些 node（要找到前一個再接過去）

這個變體本質是**不變 node、只變 `next`**，所以時間 O(n)、空間 O(1)。

## Template Code
最常用三個原語（primitives）：

### 1. Dummy head — 避免 head 變動的特例
```cpp
ListNode dummy(0);
dummy.next = head;
ListNode* prev = &dummy;
// ... 修改完之後
return dummy.next;
```

### 2. In-place reverse — 反轉整段或子段
```cpp
ListNode* reverse(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
        ListNode* next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
    }
    return prev;  // 新 head
}
```

### 3. Slow/fast pointer — 找中點或第 n 個 node
```cpp
ListNode* slow = head;
ListNode* fast = head;
while (fast->next && fast->next->next) {
    slow = slow->next;
    fast = fast->next->next;
}
// slow 是第一半的最後一個 node
// slow->next 是第二半的 head（偶數時偏右）
```

複合題（如 reorder list）就是把這三招串起來。

## Pitfalls
- **斷鏈時機**：反轉子段前要先把它與前面 cut 開（`slow->next = nullptr`），否則反轉後會形成 cycle
- **保存 next 再改 next**：每次改 `cur->next` 前都要先 `auto next = cur->next` 存下來，否則就找不到下一格了
- **奇偶長度處理**：split 之後兩半可能不等長；用「較短的那半」當迴圈條件，可以省掉內層 `if` 特判
- **null 安全**：操作前先確認 `head` / `cur->next` 非 null，否則會 deref nullptr。Slow/fast 找中點的 `fast->next->next` 是常見炸點

---

## Problems

### [[143] Reorder List](../../problems/linked-list/reorder_list.md)
**Complexity:** Time O(n), Space O(1)
- **Trigger:** `L0→L1→…→Ln` 重排成 `L0→Ln→L1→Ln-1→…`；要 in-place
- **Insight:** 三招組合 — slow/fast 找中點 → 反轉第二半 → 交錯 merge
- **Pitfall:** Cut 點要 set null；merge 用「較短半」當迴圈條件，可省內層 if
