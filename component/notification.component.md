---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Notification Standard

> [!note]
> Two things tell a user something happened. The notification center keeps what happened while they were away. A status message, a HeroUI `Toast` or `Alert`, speaks about now.

## Core Requirement

This standard owns the **notification center** the bell opens, the full notifications page, each item in them, and the data each item carries. The bell itself, its dot, and how its count is fetched belong to [[header.bar.component.md]].

It also owns every **status message**: the toast that reports the result of something the user just did, and the inline alert that reports the state of a page or a section, per "Status Messages" below.

A notification is a short, actionable pointer to something that changed. It is not a feed to read. The panel answers three questions at a glance, in this order:

1. **What needs me?** Decisions waiting for this user, in their own tab.
2. **What is new?** Unread items, marked and grouped by day.
3. **What can I do from here?** Open it, mark it, remove it, or decide it, without leaving the page.

A notification that can only be dealt with by opening another page and searching for the record has failed at its one job.

## Built On HeroUI

| Part | HeroUI component |
| :- | :- |
| The panel the bell opens | `Popover`, or a `Drawer` below the breakpoint |
| The tab row | `Tabs` |
| The type filter | `Select`, per [[dropdown.component.md]] |
| An item's actions | `Button` with `isIconOnly`, and `Dropdown` on a touch screen |
| The pending count | `Chip` with `color="danger"` |
| A toast | `Toast`, through `Toast.Provider` and HeroUI's `toast` queue |
| An inline alert | `Alert` |

Exact props come from the HeroUI MCP server, per [[stacks.rules.md]].

## The Panel

```text
Notification panel            360px to 400px wide, at most min(560px, 80vh) tall
  header row                  Notifications                                  Clear
  tab row                     General | Needs Approval [3]
  filter row                  [All notifications v]                Mark all as read
  pinned rows                 reminders that cannot be removed
  list                        the only part that scrolls
    "2 new notifications"     shown only while the panel is open
    Today
      item                    type icon | sentence, time | unread dot | actions
    Yesterday
    This week
    Older
  footer                      See all notifications
```

- **Only the list scrolls.** The header, the tabs, the filter row, and the pinned rows stay put, the same pinned-above-a-scrolling-list shape [[dropdown.component.md]] gives a search field. A panel that scrolls as a whole lets rows slide under the filter.
- The panel aligns to the bell's end edge. **Below the breakpoint it becomes a `Drawer` from the bottom.**
- **A project with no approval flow shows no tab row.** One list is clearer than a second tab that is always empty.

## Tabs, Filter, and Bulk Actions

| Tab | Holds | Count |
| :- | :- | :- |
| General | Everything informational: assignments, mentions, comments, uploads, reminders, system notices | None |
| Needs Approval | Every decision waiting for this user | The number still pending, hidden at zero |

- **The panel opens on General.** The count on Needs Approval is what pulls the eye there.
- **The count is decisions still pending, not items unread.** A read approval is still waiting.
- **The filter** is a `Select` with All, Unread, then one option per type the project actually sends. A list that short carries no search, per [[dropdown.component.md]].
- **Mark all as read** sits at the end of the filter row and shows only while something in view is unread.
- **Clear** sits at the end of the header row, asks for confirmation, and clears General only. A pending approval is never cleared; it leaves once decided.
- The tab and the filter reset when the panel closes. On the full page they live in the URL instead, per [[refresh.component.md]].

> [!warning]
> A bulk action acts on what the user can see, never on more. With the filter on one type, Mark all as read marks that type and nothing else, and Clear never reaches a pending approval. A bulk action that silently reaches past the filter is the one way this panel can lose something the user still needed.

## Date Groups

- Items are grouped under Today, Yesterday, This week, and Older. This week holds the six days before yesterday.
- **Days are counted in the user's timezone**, so an item from late evening never lands under the wrong day.
- A group with no items is not rendered, and a group heading is not sticky.

## The Item

```text
[icon]  Alex Chen assigned you to Monthly review.                  [dot]
        2 hours ago                                           [actions]
```

| Part | Rule |
| :- | :- |
| Type icon | An `18px` Tabler icon in the muted ink, from the type table below |
| Sentence | Two lines at most. The actor and the object are bold; the words between are muted |
| Time | Muted, written as described below |
| Unread dot | The `7px` danger dot, the marker [[sidebar.component.md]] defines |

- **The whole row opens the item.** Opening marks it read and follows its link: an address inside the project through the router, anything else in a new tab with `noopener`.
- **Read and unread differ in two ways, never in color alone:** the dot, and the weight of the sentence.
- **Time.** Under a minute reads `Just now`, under an hour `N minutes ago`, under a day `N hours ago`. Anything older shows the absolute date and time. The element is a `<time datetime="...">` whose `title` always carries the full absolute time.

### Item Actions

Every item carries Mark as read or Mark as unread, whichever applies, and Remove.

- **On a pointer device** the actions appear on hover and on keyboard focus inside the row, replacing the dot while visible.
- **On a touch screen** a trailing icon button opens the same actions in a `Dropdown`.
- Each action is an icon-only `Button` with its own `aria-label`, and pressing one never opens the item underneath it.

### Approval Items

An item in Needs Approval carries its decision in the row: Approve as `primary`, Reject as `outline`, and Review as `ghost`, all at `size="sm"`.

- **Decide inline only when the row already shows everything needed to decide.** A short request with its dates can be decided from the row. A purchase or a contract cannot, so it shows Review alone.
- **Reject asks for confirmation**, with a reason field when the owning feature requires one.
- **Once decided, the row shows a `Chip`** reading Approved or Rejected, and its buttons go away.
- If someone else already decided, the row says so in one line and refreshes.

> [!failure]
> A decision is sent to the owning feature's own endpoint, through its own authorization and its own audit trail, never through a generic notification endpoint and never to a URL taken from the notification payload. The payload names the record; the client knows how to reach it. Executing a URL a payload supplied is how one forged notification becomes an approval nobody made.

## Notification Types

| Type | Icon | Example sentence |
| :- | :- | :- |
| `task` | `IconChecklist` | **Alex Chen** assigned you to **Monthly review**. |
| `due` | `IconAlarm` | **Monthly review** is due **12 Apr 2026 11:00**. |
| `mention` | `IconAt` | **Alex Chen** mentioned you in **Release notes**. |
| `comment` | `IconMessageCircle` | **Alex Chen** commented on **Ticket 214**. |
| `approval` | `IconClipboardCheck` | **Alex Chen** requested **3 days of leave**. |
| `upload` | `IconUpload` | **report.pdf** was uploaded. |
| `download` | `IconDownload` | **export.csv** is ready to download. |
| `reminder` | `IconBellRinging` | **Today's log** has not been filed. |
| `system` | `IconInfoCircle` | **Maintenance** starts at **22:00**. |

The type list is closed per project. A new type is added here first, with its icon, so the same event never carries two icons.

## Writing a Notification

- **One sentence, actor first, then what happened, then the object**, addressed to the reader as `you`.
- **A date in the sentence is absolute.** A relative date in a notification is wrong by the time it is read.
- **No sensitive value, ever.** A notification never carries an identity number, a salary, a bank account, a price, a health detail, or a password. It names the record, and the project shows the details behind its own access check, per [[security.rules.md]] and [[data.rules.md]]. A notification travels further than the page it points to: into a list, a preview, and later an email or a push.
- **Repeated events on one object close together collapse into one item**, such as `3 new comments on Ticket 214`.

## Data Contract

```json
{
  "id": "0a8e0c0e-0000-0000-0000-000000000000",
  "type": "approval",
  "parts": [
    { "text": "Alex Chen", "strong": true },
    { "text": " requested " },
    { "text": "3 days of leave", "strong": true }
  ],
  "title": "Alex Chen requested 3 days of leave",
  "link": "/leave?id=0a8e0c0e",
  "created_at": "2026-10-19T09:12:00Z",
  "read_at": null,
  "action": { "kind": "approval", "state": "pending", "resource": "leave", "resource_id": "0a8e0c0e" }
}
```

- **`parts` carries the sentence as plain text segments**, with `strong` marking the actor and the object. The client renders each part as text; nothing in a notification is ever HTML or markdown.
- **`title` holds the same sentence as plain text**, for an email or a push.
- **`action` is present only on an approval.** It names the record and never a URL to call.

| Endpoint | Purpose |
| :- | :- |
| `GET /notifications` | A page of items, filtered by `tab`, `unread`, and `type`; the envelope carries `unread` and `pending` |
| `POST /notifications/{id}/read` | Mark one read |
| `POST /notifications/{id}/unread` | Mark one unread |
| `DELETE /notifications/{id}` | Remove one |
| `POST /notifications/read-all` | Mark read, scoped by the same `tab` and `type` as the list |
| `DELETE /notifications` | Clear General, never a pending approval |

Every endpoint follows [[api.rules.md]]: the shared envelope, the shared error shape, and pagination.

## Live Updates, Loading, and Errors

- **The bell asks for the count** once a minute and when the window regains focus, per [[header.bar.component.md]].
- **While the panel is open, a new item never pushes the rows the user is reading.** A small button reading `N new notifications` appears at the top of the list instead.
- **An action updates the row and the dot at once**, and puts them back with an error toast if the server refuses it.

| State | Shown as |
| :- | :- |
| Loading | Three `Skeleton` rows, per [[skeleton.component.md]] |
| General empty | `No notifications yet.` |
| Unread empty | `All caught up.` |
| A type filter empty | `No notifications of this type.` |
| Needs Approval empty | `Nothing waiting for approval.` |
| The list failed to load | An inline `Alert` with `status="danger"` and a Try Again action |

The bell stays silent on a failed count. The panel is different: the user opened it on purpose, so it says when it has no answer.

## The Full Notifications Page

See all notifications, at the foot of the panel, opens the full page.

- It uses the shell and the full width of [[layout.component.md]], with the same tabs, filter, groups, and items as the panel.
- **The tab, the filter, and the page number live in the URL**, per [[refresh.component.md]].
- **It pages with HeroUI's `Pagination`**, per [[pagination.component.md]], never an endless scroll.
- Each row carries a `Checkbox`, and a selection offers Mark as read and Remove for the selected rows only.

## Status Messages

Every result the user should know about is shown in one of four variants. It is a **toast** when it reports an action the user just took, and an **inline alert** when it reports the state of a page or a section.

| Variant | HeroUI | Example title and description |
| :- | :- | :- |
| Info | `Toast` `variant="accent"`, `Alert` `status="accent"` | Up to Date, then `There are no new updates right now.` |
| Success | `variant="success"` | Password Changed, then `Your password was changed.` |
| Warning | `variant="warning"` | No Connection, then `You are offline; changes may not save.` |
| Error | `variant="danger"` | Server Error, then `Something went wrong on the server. Try again shortly.` |

### Toast or Inline Alert

| Placement | Use it for | Lifetime |
| :- | :- | :- |
| Toast | The result of an action the user just took: saved, sent, deleted, copied, or failed | Info and success `4s`, HeroUI's default; warning `6s`; error stays until closed, `timeout: 0`; at least `8s` when it carries an action |
| Inline alert | A state of the page or a section: offline, a section that failed to load, an error for a whole form, a read-only period | Until the state changes |

- **A field's own validation error is never a toast.** It sits under the field, through the field's `FieldError`, where the user is already looking.
- **A state that will still be true in ten seconds is never a toast.** Being offline is an inline warning under the page heading until the connection returns, then a success toast reading Back Online.
- **The login screen keeps its own error**, per [[login.component.md]].

### Rules

- **One `Toast.Provider` per app**, at the root, placed `top end` with HeroUI's `maxVisibleToasts` of three. The same message twice within two seconds shows once.
- **Title and description.** The title names what happened in two to five words. The description says, in one sentence, what it means or what to do next.
- **At most one action**, such as Try Again, Undo, or View, through HeroUI's action button.
- **Every toast can be closed**, and the countdown pauses while the pointer is over it or focus is inside it. HeroUI does both.
- **Copy is sentence case, with no emoji**, per [[uix.component.md]]. An error says what failed and what to do. It never shows a raw server message, a status code on its own, or a stack trace, and it never carries a sensitive value, under the same rule as a notification.

## Accessibility

- **The panel is HeroUI's `Popover`**, so focus moves into it when it opens and Escape closes it and returns focus to the bell. The tabs are HeroUI's `Tabs`, with the arrow keys.
- **An unread item's accessible name starts with `Unread,`**, as visually hidden text. The dot is `aria-hidden`, because a red circle says nothing to a screen reader.
- **Every action is reachable by keyboard**, not only by hover, and has its own `aria-label`.
- **The `N new notifications` button is announced** through a polite live region.
- **An info or success message is announced politely; a warning or an error interrupts**, because it reports something the user has to act on. HeroUI's `Toast` and `Alert` carry the right role for their variant.
- **A toast never takes focus.** It is announced, and the user stays where they were working.
- **The variant is never carried by color alone**: each has its own icon and its own title.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Open the panel on General, and count only pending decisions on Needs Approval | Count unread items on the approval tab |
| Scroll the list only, under a fixed header, tabs, and filter | Let the whole panel scroll |
| Scope every bulk action to what is in view | Let Clear or Mark all reach past the filter |
| Decide inline only when the row shows enough to decide | Put Approve on a row that hides what is being approved |
| Send a decision to the owning feature's endpoint | Call a URL supplied by the notification payload |
| Name the record, and show details behind an access check | Put a sensitive value in a notification |
| Use HeroUI's `Toast` for an action's result and `Alert` for a page's state | Toast a state that will still be true in ten seconds |
| Keep an error toast until it is closed | Let an error vanish after four seconds |
| Put a field's error under the field | Report a field's error as a toast |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[header.bar.component.md]] | The bell, its dot, and the count fetch | What opens this panel |
| [[dropdown.component.md]] | Pickers and menus | The type filter and the touch-screen action menu |
| [[sidebar.component.md]] | The rail's markers | The one dot vocabulary |
| [[skeleton.component.md]] | Skeletons | The loading rows |
| [[pagination.component.md]] | Paging | The full page's pager |
| [[security.rules.md]] | Security | Why a notification never carries a sensitive value |
| [[api.rules.md]] | The API contract | The envelope and the error shape |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This notification standard
6. Existing project conventions

## Related

- [[uix.component.md]]
- [[header.bar.component.md]]
- [[dropdown.component.md]]
- [[sidebar.component.md]]
- [[skeleton.component.md]]
- [[pagination.component.md]]
- [[layout.component.md]]
- [[login.component.md]]
- [[refresh.component.md]]
- [[security.rules.md]]
- [[data.rules.md]]
- [[api.rules.md]]
- [[stacks.rules.md]]
- [[memory.rules.md]]
