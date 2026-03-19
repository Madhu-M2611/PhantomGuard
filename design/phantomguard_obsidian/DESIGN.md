# Design System Specification

## 1. Overview & Creative North Star: "The Kinetic Void"
This design system is built upon the concept of **The Kinetic Void**. In the high-stakes world of cybersecurity, we move away from static, cluttered interfaces toward a cinematic, editorial experience that feels both atmospheric and hyper-precise. 

The "Void" represents the vast, dark expanse of data, while "Kinetic" elements are the vibrant, neon signals—threats, pulses, and interactions—that cut through the darkness. We avoid "standard" dashboard templates by embracing intentional asymmetry, high-contrast typography, and a "Glass-on-Glass" layering philosophy. This isn't just a tool; it is a high-tech lens into a digital battlefield.

---

## 2. Color Architecture
Our palette is rooted in the deep shadows of a cyber-noir aesthetic, utilizing high-chroma accents for immediate cognitive recognition.

### The Foundation
- **Base Surface:** `surface` (#121318) — The primary canvas.
- **Primary (Action):** `primary` (#c3f5ff) — Electric blue for all primary interactive states.
- **Success (Normal):** `secondary_container` (#13ff43) — High-vibrancy green for stable system health.
- **Danger (Threat):** `error` (#ffb4ab) — Crimson/Red for critical alerts and active intrusions.

### The "No-Line" Rule
To maintain a premium, seamless feel, **1px solid borders for sectioning are strictly prohibited.** Structural boundaries must be defined solely through background shifts. For example, a global navigation rail should sit on `surface_container_low`, while the main workspace sits on the base `surface`.

### Surface Hierarchy & Nesting
Depth is created through "Tonal Stacking" rather than lines. Use the container tiers to define importance:
1. **Background:** `surface` (#121318)
2. **Main Content Blocks:** `surface_container` (#1e1f25)
3. **Elevated Cards/Modals:** `surface_container_high` (#292a2f)
4. **Active/Hovered Elements:** `surface_container_highest` (#34343a)

### The "Glass & Gradient" Rule
Floating panels (modals, tooltips, or flyouts) must utilize Glassmorphism. Use `surface_variant` (#34343a) at 60% opacity with a `24px` backdrop blur. For primary CTAs, apply a subtle linear gradient from `primary` (#c3f5ff) to `primary_container` (#00e5ff) to give the UI a "soul" and a sense of internal illumination.

---

## 3. Typography: Technical Authority
We use a dual-font approach to balance brutalist technicality with refined legibility.

- **Display & Headlines (Space Grotesk):** Use `display-lg` through `headline-sm` for high-impact data points and section titles. The geometric, slightly idiosyncratic nature of Space Grotesk communicates a futuristic, "hacker-elite" aesthetic.
- **Functional & Body (Inter):** All system-critical information, titles, and body text use Inter. Its neutral, clean profile ensures maximum readability in high-stress monitoring environments.
- **Data Points:** For numerical values (IP addresses, timestamps, threat counts), utilize Inter with `tabular-nums` enabled to ensure vertical alignment in data grids.

---

## 4. Elevation & Depth
In this design system, depth is a functional indicator of priority.

### The Layering Principle
Avoid shadows on standard cards. Instead, "stack" your tiers. A `surface_container_lowest` (#0d0e13) card nested within a `surface_container` (#1e1f25) section creates a "recessed" look, suggesting a protected data well.

### Ambient Shadows
When an element must "float" (e.g., a critical alert modal), use an **Ambient Shadow**:
- **Color:** `surface_container_lowest` at 40% opacity.
- **Blur:** 40px to 60px.
- **Spread:** -10px.
This mimics the way light dissipates in a foggy, neon-lit environment.

### The "Ghost Border" Fallback
If an element lacks sufficient contrast against a background, use a **Ghost Border**: 
- **Stroke:** 1px
- **Color:** `outline_variant` (#3b494c) at 15% opacity.
Never use 100% opaque borders; they shatter the cinematic illusion.

---

## 5. Components

### Buttons
- **Primary:** `primary` background, `on_primary` text. Apply a subtle outer glow (0px 0px 12px) using the `primary` color at 30% opacity.
- **Secondary:** Ghost style. `outline` border at 30% opacity, `primary` text. 
- **Corner Radius:** All buttons use `md` (0.375rem) for a sharp, technical feel.

### Input Fields
- **Base State:** `surface_container_high` background with a `sm` (0.125rem) bottom-only "accent bar" in `outline_variant`.
- **Focus State:** The bottom bar transitions to `primary` (#c3f5ff) with a soft glow.
- **Error State:** The bottom bar transitions to `error` (#ffb4ab).

### Cards & Lists
- **Rule:** No divider lines. 
- **Separation:** Use `spacing-8` (1.75rem) between cards. 
- **Interaction:** On hover, a card should shift from `surface_container` to `surface_container_highest`.

### Status Indicators (Cyber-Specific)
- **Pulse:** Use a `2px` dot of `secondary_container` (Success) with a concentric, animating ring to indicate live system monitoring.
- **Threat Levels:** Use `tertiary_container` for "Warning" and `error_container` for "Breach."

---

## 6. Do's and Don'ts

### Do
- **Embrace Asymmetry:** Let a data visualization bleed off the edge of a container to suggest an infinite stream of information.
- **Use High-Contrast Scales:** Pair a `display-lg` metric with a `label-sm` caption to create an editorial hierarchy.
- **Tighten Radii:** Keep corners at `sm` or `md`. Rounded "bubble" shapes are forbidden; they undermine the "Secure" brand pillar.

### Don't
- **Don't use pure white (#FFFFFF):** It is too harsh for the Cyber-noir palette. Use `on_surface` (#e3e1e9) for primary text.
- **Don't use standard Drop Shadows:** Use tonal shifts or ambient, tinted glows only.
- **Don't use generic icons:** Ensure all iconography is "Thin" or "Light" weight (0.75px to 1px strokes) to match the technical precision of Inter.

### Accessibility Note
While the "Ghost Border" and "No-Line" rules are preferred, always ensure that interactive elements maintain a 3:1 contrast ratio against their immediate background. Use `outline` (#849396) for essential UI boundaries if tonal shifts are insufficient for low-vision users.