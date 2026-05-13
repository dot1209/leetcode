# [138] Copy List with Random Pointer
**Pattern:** [Linked List → Deep Copy](../../patterns/linked-list/deep-copy.md)
**Complexity:**
- Hashmap：Time O(n), Space O(n)
- Interleaving：Time O(n), Space O(1)（不算回傳的 new list）
**Link:** https://leetcode.com/problems/copy-list-with-random-pointer/

## Trigger Signals
- Singly linked list 每個 node 帶 `next` + `random` 兩個指標
- 要 deep copy：new list 的所有指標只能指向 new node，不能指回 old
- `random` 可能指向任意位置或 nullptr → 不能單純線性走過就接好

## Core Insight
**Hashmap 法**：建 `old → new` 的 map，走 list 時用 map 把所有 next/random 翻譯成新 node。

**O(1) 法（interleaving）**：把每個 copy 插在原 node 後面，形成 `A → A' → B → B' → ...`。這條交錯鏈本身就是 hashmap：「`X` 的 copy」永遠是 `X->next`。對應 random 也只需要 `X->random->next`。三 pass 完成 build / wire / split。

## Complexity Analysis
- **Hashmap**：兩次走 list，每次每 node 做常數 hash 操作 → Time O(n)。Map 存 n 個 entry → Space O(n)。
- **Interleaving**：三次走 list，每次每 node 改 O(1) 個指標 → Time O(n)。除了 new node 本身，無額外資料結構 → Extra Space O(1)。

## Solution Code

### Hashmap（two-pass，最乾淨）
```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> mp{{nullptr, nullptr}};
        for (Node* cur = head; cur; cur = cur->next)
            mp[cur] = new Node(cur->val);
        for (Node* cur = head; cur; cur = cur->next) {
            mp[cur]->next = mp[cur->next];
            mp[cur]->random = mp[cur->random];
        }
        return mp[head];
    }
};
```

第一輪只建 node 進 map（含 `nullptr → nullptr`），第二輪只接線。沒有 lazy 邏輯、沒有特例。

### Hashmap（one-pass + helper）
```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> mp;
        auto get_copy = [&](Node* old) -> Node* {
            if (!old) return nullptr;
            auto it = mp.find(old);
            if (it != mp.end()) return it->second;
            return mp[old] = new Node(old->val);
        };
        Node* new_head = get_copy(head);
        Node* copy_cur = new_head;
        for (Node* cur = head; cur; cur = cur->next, copy_cur = copy_cur->next) {
            copy_cur->next = get_copy(cur->next);
            copy_cur->random = get_copy(cur->random);
        }
        return new_head;
    }
};
```

關鍵是同步 walk `copy_cur`，避免每輪用 `get_copy(cur)` 重新查 map。

### Interleaving（O(1) extra space）
```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        // chain nodes by A -> A' -> B -> B' -> ...
        auto cur = head;
        while (cur != nullptr) {
            auto tmp = new Node(cur->val);
            auto next_cur = cur->next;
            cur->next = tmp;
            tmp->next = next_cur;

            cur = next_cur; // move cur
        }
        cur = head;
        // now the copy of a node is its next pointer
        // so the copy of A->random is A->random->next;
        while (cur != nullptr) {
            auto copied = cur->next;
            copied->random = cur->random ? cur->random->next : nullptr;

            // move cur
            cur = copied->next;
        }
        // split the interweave list
        cur = head;
        Node dummy(0);
        auto new_head = &dummy;
        // chain nodes by A -> A' -> B -> B' -> ...
        while (cur != nullptr && cur->next != nullptr) {
            new_head->next = cur->next;
            
            // restore list
            cur->next = cur->next->next;
            
            // move
            new_head = new_head->next;
            cur = cur->next;
        }
        new_head->next = nullptr;

        return dummy.next;
    }
};
```

## Pitfalls

### Hashmap 版
- Lazy 建 copy（走到才建）會多很多特例（head 要不要先建？inner null check？）。改成 **two-pass** 最乾淨
- One-pass + helper 要記得 walking `copy_cur`，不然每輪 `get_copy(cur)` 多一次 hash lookup

### Interleaving 版
- **Pass 2 random null check**：`cur->random` 可能是 nullptr，不能直接 `->next`
- **Pass 3 cursor reset**：上一個 pass 結束時 `cur == nullptr`，pass 3 要重新 `cur = head`
- **Pass 3 必須還原原 list**：題目要求 original 不被修改。每輪 `cur->next = copy->next` 是還原，`copy_tail->next = copy` 才是抽出 copy
- **最後一個 copy 的 `next` 收尾**：依賴 pass 1 的副作用恰好設成 nullptr 不算錯，但建議顯式 `copy_tail->next = nullptr;`，讓 pass 3 的正確性 self-contained
- **`new` dummy vs stack dummy**：用 `Node dummy(0)` 放 stack 上避免 leak（LC 不查但好習慣）

## Related Problems
- [133] Clone Graph — 同樣是 deep copy 含非線性指標的結構，但是 graph 不是 list，只能用 hashmap + DFS/BFS
- [430] Flatten a Multilevel Doubly Linked List — 多層 list 攤平，類似的「指標重接」訓練
