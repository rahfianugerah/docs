---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Dropdown Standard

> [!important]
> Every form dropdown is a HeroUI picker with HeroUI's layout. Past seven options it carries smart search, and a long list scrolls inside a capped panel while the search field stays put.

## Core Requirement

Every dropdown follows this standard. Three things look alike and are not the same thing:

| Case | What it is | Built on |
| :- | :- | :- |
| **Form dropdown** | Picks a value from a set of options | HeroUI `Select` or `Autocomplete` |
| **Action menu** | Runs one of several actions, such as a row's actions or the account menu | HeroUI `Dropdown` |
| **Navigation group** | A collapsible group of links in the sidebar | A disclosure built from HeroUI parts, per "Navigation Groups" below |

A form dropdown never runs an action, an action menu never holds a value, and a navigation group is never either. Mixing them produces a control that announces the wrong thing to a screen reader.

This extends [[uix.component.md]]. Every color, radius, and shadow comes from HeroUI's theme variables, and exact props come from the HeroUI MCP server, per [[stacks.rules.md]].

## Which Picker

| Options | Component | Why |
| :- | :- | :- |
| Seven or fewer, all readable at once | `Select` | Every option is visible without typing, so a search field would be noise |
| More than seven | `Autocomplete`, with smart search | The trigger looks exactly like a `Select`, and the search sits at the top of the panel |
| A value the user types more often than picks, or one that may be new | `ComboBox` | The field itself is the input |
| Thousands, or a set that lives on the server | `Autocomplete`, filtering on the server | The database filters, per [[search.component.md]] |

**Smart search is the default.** A dropdown omits it only when it holds seven options or fewer, because then every option is already on screen and typing is slower than looking.

## The Layout Is HeroUI's

A dropdown keeps HeroUI's anatomy and HeroUI's look. The trigger of an `Autocomplete` is the same as the trigger of a `Select`, so a short dropdown and a long one in the same form read as the same control:

```tsx
import { Autocomplete, Description, Label, ListBox, SearchField } from "@heroui/react";

<Autocomplete>
  <Label>Country</Label>
  <Autocomplete.Trigger>
    <Autocomplete.Value />
    <Autocomplete.ClearButton />
    <Autocomplete.Indicator />
  </Autocomplete.Trigger>
  <Description>Where the invoice is sent</Description>
  <Autocomplete.Popover>
    <Autocomplete.Filter filter={smartFilter}>
      <SearchField aria-label="Search countries">
        <SearchField.Group>
          <SearchField.SearchIcon />
          <SearchField.Input />
        </SearchField.Group>
      </SearchField>
      <ListBox className="max-h-80 overflow-y-auto">{/* ListBox.Item per option */}</ListBox>
    </Autocomplete.Filter>
  </Autocomplete.Popover>
</Autocomplete>
```

- **The label sits above, the description below**, as HeroUI lays them out. A placeholder is never the label.
- **An optional field carries the clear button**; a required one does not, so it cannot be emptied by accident.
- **The trigger, the panel, and the options are never restyled.** A color changes through a HeroUI variable, per [[uix.component.md]]; the layout does not change at all.
- **Long lists group with `ListBox.Section`**, each with a heading, when the options fall into natural groups.
- **A disabled option stays visible**, dimmed, so the user can see it exists and is unavailable rather than wonder where it went.

## Smart Search

Search that a person does not have to think about. It finds what they meant, not only what they typed letter for letter.

1. **Ignores case and accents.** `jose` finds `José`, and `JAKARTA` finds `Jakarta`. This is HeroUI's `useFilter` with `sensitivity: "base"`.
2. **Matches every word, in any order.** `west java` finds `Java, West`. Each word of the query has to appear somewhere in the option; their order does not matter.
3. **Matches what the user can see.** The option's label, and any alias the option declares, such as a code or an abbreviation. Never an internal identifier the user has never seen.
4. **Ranks the obvious answer first**: an exact match, then a label that starts with the query, then a word that starts with it, then anything that contains it.
5. **Focuses the search field when the panel opens**, so typing starts at once.
6. **Says what it searched for when nothing matches**: `No results for "Jakrta"`, never a blank panel.
7. **Clearing the search restores the full list** and keeps the current selection.

The shared filter covers rules 1 and 2, and every dropdown in a project uses this one function:

```tsx
import { useFilter } from "@heroui/react";

export function useSmartFilter() {
  const { contains } = useFilter({ sensitivity: "base" });
  return (text: string, query: string) =>
    query.trim().split(/\s+/).every((word) => contains(text, word));
}
```

- **Aliases and ranking need the list in the project's hands.** Filter and sort the options yourself and pass the result to the `ListBox`, the same controlled shape HeroUI's asynchronous filtering example uses. A boolean filter can include an option but cannot order it.
- **A list over about fifty options is ranked**, because past that the first screenful is all anyone reads.
- **Matching rules beyond these belong to [[search.component.md]]**, which owns normalization and the matching ladder for every search in the project. A dropdown never invents its own.

## Long Lists Scroll Inside the Panel

**The list scrolls; the panel, the search field, and the page do not.**

- **Cap the list at about eight visible rows**: `max-h-80`, which is 320px, or half the viewport on a short screen. The panel never grows past the edge of the screen.
- **Put the cap on the `ListBox`, not on the popover.** The search field sits outside the list, so it stays pinned at the top while the options scroll beneath it.
- **The scrollbar is visible** while the list overflows, per [[scrollbar.component.md]]. A list with a hidden scrollbar looks complete at eight rows.
- **Over about a hundred options, virtualize the `ListBox`**, so only the rows on screen are rendered. HeroUI supports it through React Aria's `Virtualizer`.
- **The selected option is scrolled into view when the panel opens**, and the arrow keys keep the active option in view. HeroUI does both; never break them with a wrapper that scrolls on its own.
- **A set that lives on the server loads as it scrolls**, with a loading row at the bottom, per [[loading.component.md]]. It never fetches thousands of rows to filter in the browser.

## Multiple Selection

- `selectionMode="multiple"` on the picker and on its `ListBox`.
- The trigger shows the selected values; **past three, it shows the first three and a count**, so the trigger keeps one line.
- The panel stays open between selections, and the search field keeps its query, so picking five related options is five clicks, not five searches.

## Action Menus

An action menu is a HeroUI `Dropdown`. It runs something; it holds no value.

- **The trigger says what the menu is for**, with a label or an icon button that carries an accessible name. A bare ellipsis with no name announces nothing.
- **A destructive action comes last**, after a separator, in the danger color, and asks for confirmation when it cannot be undone, per [[button.component.md]].
- **A third row action becomes a menu**, per [[table.component.md]].

## Navigation Groups

A collapsible group in a sidebar: a parent row that expands to reveal nested links. It is navigation, not a form control, and HeroUI has no sidebar, so it is built from HeroUI parts and theme variables, per [[sidebar.component.md]].

```html
<button class="navparent" aria-expanded="false" aria-controls="grp-reports">
  <span class="icon" aria-hidden="true"></span>
  <span>Reports</span>
  <span class="chev" aria-hidden="true"></span>
</button>
<div class="subnav" id="grp-reports">
  <a href="/reports/daily">Daily</a>
  <a href="/reports/monthly">Monthly</a>
</div>
```

```css
.navparent {
  display: flex; align-items: center; gap: 11px; width: 100%;
  padding: 8px 10px; border: none; background: none;
  font: inherit; font-weight: 500; color: var(--ink2);
  border-radius: var(--r-sm); cursor: pointer; text-align: left;
}
.navparent .icon { color: var(--ink3); }
.navparent .chev { margin-left: auto; color: var(--ink3); transition: transform .16s ease; }
.navparent:hover { background: var(--line2); color: var(--ink); }
.navparent[aria-expanded="true"] { color: var(--accent-tua); font-weight: 600; }
.navparent[aria-expanded="true"] .icon { color: var(--accent); }
.navparent[aria-expanded="true"] .chev { transform: rotate(180deg); }

.subnav { margin: 1px 0 4px 19px; padding-left: 14px; border-left: 1px solid var(--line2); }
.subnav a { display: block; padding: 7px 10px; font-size: .8rem; color: var(--ink2); }
.subnav a[aria-current="page"] { background: var(--accent-soft); color: var(--accent-tua); font-weight: 600; }
```

**The icon belongs to the title only.**

- The parent row carries exactly two icons: the group icon at the start, the chevron at the end.
- Every item inside the group is **text only**. No leading icon, no bullet, no dot. The indent and the rail already say it is a child.
- A flat top-level link that is not a group keeps its own icon.

Rules:

- The parent is a `button` with `aria-expanded` and `aria-controls`, never an `a` with no `href`.
- The current page carries `aria-current="page"`, not just a class.
- A group whose child is the current route opens by default, so a reload does not collapse the section being worked in.
- Two levels only: group and item. A third level means the grouping is wrong.
- **The chevron rotates 180 degrees** rather than swapping glyphs, and it stays `--ink3` in every state, because it marks state rather than activity.
- The nested list is indented with a rail and **never takes the overlay shadow**: it is inline navigation, not a floating panel.

## Accessibility

HeroUI supplies the roles, the keyboard map, and the announcements: the combobox and listbox roles, arrow keys, Home and End, typeahead, Enter, and Escape. Keep them intact.

- **Every picker has a visible label.** A placeholder is not one.
- **The search field has an accessible name**, such as `Search countries`, because its icon is not a label.
- **The empty state is text**, so a screen reader hears that nothing matched instead of silence.
- A trigger is at least 44px tall on a touch screen, per [[uix.component.md]].
- **Never mark the selected option with color alone.** HeroUI's item indicator shows the check; keep it.
- **Never wrap a picker in a handler that swallows keys or scrolls on its own.** It breaks the keyboard map HeroUI built.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Use `Select` for seven options or fewer | Put a search field on a three-option dropdown |
| Use `Autocomplete` with smart search past seven | Make the user scroll a long list to find one option |
| Keep HeroUI's anatomy, label above and description below | Restyle the trigger, the panel, or the option rows |
| Share one smart filter across the project | Write a new matching rule per dropdown |
| Ignore case and accents, and match every word in any order | Match only an exact, case-sensitive prefix |
| Cap the `ListBox` at about eight rows so it scrolls under a pinned search | Cap the popover, so the search field scrolls away |
| Virtualize past about a hundred options | Render thousands of rows into the panel |
| Filter a server-sized set on the server | Fetch everything to filter it in the browser |
| Show `No results for "..."` | Leave an empty panel |
| Use `Dropdown` for actions and `Select` for values | Run an action from a value picker |
| Keep a navigation group's items text only | Put an icon or a bullet on a nested item |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The HeroUI setup, the theme variables, and the overlay rules | Every value this file names but does not define |
| [[search.component.md]] | Matching and normalization for every search | The rules smart search inherits rather than redefines |
| [[scrollbar.component.md]] | Where a scrollbar must be visible | Why an overflowing list shows its scrollbar |
| [[sidebar.component.md]] | The rail a navigation group sits in | The grouping, the markers, and the drawer around it |
| [[table.component.md]] | The row actions | Where a third row action becomes an action menu |
| [[loading.component.md]] | Loading states | The loading row at the bottom of a server-fed list |
| [[button.component.md]] | The button variants | The danger action at the bottom of a menu |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This dropdown standard
6. Existing project conventions

## Related

- [[uix.component.md]]
- [[search.component.md]]
- [[scrollbar.component.md]]
- [[sidebar.component.md]]
- [[table.component.md]]
- [[calendar.component.md]]
- [[refresh.component.md]]
