# Google L4 — Practice Sessions

紀錄規則見 [README](README.md)。**Hint 等級與完成狀態要分開看**；下表是依已有對話可驗證的基線，未完成者不算正式通過。

| 日期（台灣） | 題目 | 解題獨立性／提示 | Code 狀態 | L4 品質 | 證據與需回訪項目 |
|---|---|---|---|---|---|
| 2026-11-11 | [827] Making A Large Island | Independent AC（使用者提供完整 Code；歷史提示量未完全核實） | 使用者回報 AC | Not Assessed（完整 Mock 未記錄） | DSU、重複 Root 去重；Follow-up 的 Stale Size／Union by Size 證明曾需修正。 |
| 2026-11-14 | [907] Sum of Subarray Minimums | Major Hint（核心 Contribution、Tie-breaking、Stack 規則經引導） | 本段對話中未確認最終 AC | Not Assessed（未完成完整 Coding Round） | Stack Top 時機、Previous ≤ 與 Next <、相同值歸屬、溢位；安排不同題變形驗證。 |
| 2026-11-15 | [1590] Make Sum Divisible by P | In Progress（目前接受過 Minor Hint；待完成評估） | 尚未提交 Code | Not Assessed | 自行想到 Prefix Modulo 與歷史 Index；減法方向曾修正，已獨立判斷最短區間要保留最新 Index。 |

## 後續新增格式

每題完成後新增一列，必要時在下方補充：

- **Problem / Date / Cold or Revisit：** LeetCode 編號、日期、是否第一次接觸、若重複則檢查至少間隔 7 個完整日。
- **Initial Approach：** 使用者自己提出的第一個解法與 Time／Space。
- **Hints：** `None / Minor / Major`，以及實際揭露了什麼，不能因為最終 AC 就忘記提示。
- **Code & Proof：** 是否自行實作並 AC；Complexity、Correctness、Edge Cases 是否交代清楚。
- **L4 Quality：** `Strong / Borderline / Weak / Not Assessed`，簡潔列出原因。
- **Weaknesses：** 分別記 Conceptual Gap 與 Implementation Slip。
- **Next Verification：** 用另一道陌生變形驗證，不在 7 天內重複同題。
