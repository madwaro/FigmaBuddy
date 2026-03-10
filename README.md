# Figma Copy Checker

A UX copy review tool that uses **GitHub Copilot** and **Figma's MCP server** to check UI text against the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/).

Select a frame in Figma, ask Copilot to check the copy, and get an instant structured report with actionable feedback — right from VS Code.

## What it checks

| Category | Examples |
|----------|----------|
| **Voice & tone** | Conversational language, no blame, "you"/"we" pronouns |
| **Capitalization** | Sentence-style caps on buttons, labels, headings |
| **Punctuation** | No periods on buttons, Oxford comma, no exclamation points |
| **Word choice & brevity** | Simple words, contractions, front-loaded key info |
| **Active voice** | Action-oriented text, passive only to avoid blame |
| **UI-element rules** | Specific checks for buttons, errors, dialogs, tooltips, labels, links |
| **Inclusive language** | Gender-neutral terms, people-first disability language |
| **Accessibility** | No idioms, US English spelling, scannable structure |

Issues are categorized by severity: 🔴 High · 🟡 Medium · 🔵 Low

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) installed
- [Figma desktop app](https://www.figma.com/downloads/) with MCP server enabled
- A Figma plan with Dev Mode access (Professional, Organization, or Enterprise with a Dev or Full seat)

## Setup

### 1. Enable the Figma MCP server

1. Open the **Figma desktop app** and open a design file.
2. In Figma, go to **Figma menu → Preferences → Enable Dev Mode MCP Server** (or find the toggle in the Dev Mode settings panel).
3. Figma will start a local MCP server on `http://127.0.0.1:3845/mcp`.

### 2. Open this project in VS Code

```bash
git clone https://github.com/madwaro/FigmaCopyChecker.git
cd FigmaCopyChecker
code .
```

The workspace already includes:

- **`.vscode/mcp.json`** — Connects VS Code to the Figma MCP server
- **`.github/copilot-instructions.md`** — The full style guide ruleset Copilot uses for reviews

No dependencies to install. No build step.

### 3. Verify the connection

Open Copilot Chat in VS Code (`Ctrl+Shift+I` / `Cmd+Shift+I`). You should see **figma-desktop** listed as a connected MCP server. If not, make sure Figma is open with the MCP server enabled and restart VS Code.

## Usage

1. In Figma, **select the frame** you want to review.
2. In VS Code, open **Copilot Chat** and type:

   ```
   Check the copy on this selection
   ```

3. Copilot will pull the text from your Figma selection, evaluate it against the style guide, and return a structured report.

4. The report is automatically saved to the `./reports/` folder as a markdown file (e.g., `2026-03-10-homepage.md`).

### Example prompts

- `Check the copy on this selection`
- `Review the UX copy for this frame`
- `Audit the text in this dialog for style guide compliance`

## Reports

Every review is saved to `./reports/` with the naming format:

```
YYYY-MM-DD-<frame-name>.md
```

Reports include:
- Summary with issue count and severity breakdown
- Each issue with the rule violated, current text, and a suggested fix
- What's working well (positive feedback)
- General recommendations

## Customization

The rules live in `.github/copilot-instructions.md`. You can:

- **Add rules** for your team's specific terminology or product voice
- **Adjust severity** thresholds to match your review process
- **Modify the output format** to fit your workflow

## References

- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Brand Voice: Simple and Human](https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human)
- [Top 10 Tips for Microsoft Style](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)
- [Capitalization](https://learn.microsoft.com/en-us/style-guide/capitalization)
- [Bias-Free Communication](https://learn.microsoft.com/en-us/style-guide/bias-free-communication)
- [Writing Style for Windows Apps](https://learn.microsoft.com/windows/apps/design/style/writing-style)
- [Figma MCP Server Docs](https://developers.figma.com/docs/figma-mcp-server/)
