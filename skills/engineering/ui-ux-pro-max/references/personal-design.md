# Personal design preferences

These preferences were accumulated in the user's original skill. Preserve them as reusable defaults, while following the current request and the project's established design system.

## Task and flow first

Design around the user's sequence of understanding and action rather than a flat inventory of features. Make one primary job clear on each screen. Separate unrelated jobs into focused pages with quiet, understandable navigation.

Use a single-column main flow where it makes cause, action, and result clear. Use columns for genuine comparison or parallel inspection. Put each action near the area it affects and its result in the next logical place.

Use tabs or segmented controls for peer alternatives, including import methods and result views, especially when their content lengths differ substantially. Choose the structure before visual decoration.

Keep global headers for identity, navigation, and concise context. Put page actions and state in the relevant content area. Show status that changes the user's next decision; avoid decorative counters and permanent low-value status lines.

## Visual and language defaults

Prefer a calm, minimal, content-first interface, with light surfaces, restrained accents, stable spacing, clear dividers, readable density, modest typography, and consistent blue accents where appropriate. Apple product pages and GitHub product or documentation pages are useful references for restraint, not layouts to copy regardless of the task.

For tools and inspectors, put controls and real data near the top. Avoid oversized titles, long introductory subtitles, decorative hero blocks, excessive empty space, and marketing copy that delays the task. Keep labels short and functional.

Prefer clarity over spectacle in internal demos, workflow screens, and evaluation tools. Avoid defaulting to dark themes, purple gradients, excessive glass effects, or generic AI-product decoration. A user-requested theme or an existing brand system can change these choices.

## Demos and structured-output inspectors

A demo should support a real product flow rather than expose a collection of API buttons. Keep inspection and interaction on separate pages when they serve different goals. Surface controls, selectors, data, and outcomes in a coherent sequence.

For AI or structured-output inspection, provide a clear raw-data or JSON view with comparable visibility to the human-readable view. Avoid imposing that view on unrelated consumer tasks. Use peer tabs for portrait, memories, results, and raw data when this makes comparison and navigation clearer.

## Platform-specific checks

Use the actual platform's conventions and the project's components. Stable interaction states, consistent vector icons, readable contrast, clear focus, useful error recovery, and reduced-motion preferences matter across relevant contexts. Mobile safe areas, Dynamic Type, touch targets, and device orientation apply when building mobile surfaces; they do not turn a browser page into a React Native app.

For implemented browser tools, check that the first screen reaches the task, labels are concise, unrelated jobs are separated, long and short views remain navigable, and the flow works at the requested desktop and mobile widths.
