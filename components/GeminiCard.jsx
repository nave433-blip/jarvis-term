// React component to render the optional "ui" object as a Gemini-style card.
// Usage:
// <GeminiCard ui={parsed.ui} onAction={(action, button) => { ... }} />
// - action: one of "confirm","cancel","help","run","open"
// - button: the full button object from the ui.buttons array
import React from "react";

export default function GeminiCard({ ui, onAction }) {
  if (!ui) return null;
  const { title, subtitle, markdown, buttons } = ui;

  const handleClick = (btn) => {
    if (onAction) onAction(btn.action, btn);
  };

  return (
    <div style={styles.card}>
      {title && <div style={styles.title}>{title}</div>}
      {subtitle && <div style={styles.subtitle}>{subtitle}</div>}
      {markdown && (
        <div
          style={styles.markdown}
          // NOTE: you should sanitize/pipe through a safe markdown renderer in production
          dangerouslySetInnerHTML={{ __html: markdownToHtml(markdown) }}
        />
      )}
      <div style={styles.buttonRow}>
        {(buttons || []).slice(0, 3).map((b, i) => (
          <button
            key={i}
            onClick={() => handleClick(b)}
            style={b.primary ? styles.primaryButton : styles.button}
          >
            {b.label}
          </button>
        ))}
      </div>
    </div>
  );
}

// Very small markdown -> HTML helper (supports inline backticks and newlines)
function markdownToHtml(md) {
  // minimal replacements; replace code backticks with <code> and newlines with <br>
  return md
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br/>");
}

const styles = {
  card: {
    border: "1px solid #ddd",
    borderRadius: 8,
    padding: 12,
    maxWidth: 520,
    background: "#fff",
    boxShadow: "0 1px 4px rgba(16,24,40,0.06)",
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto",
    margin: 8,
  },
  title: { fontSize: 16, fontWeight: 600, marginBottom: 4 },
  subtitle: { fontSize: 13, color: "#555", marginBottom: 8 },
  markdown: { fontSize: 13, color: "#333", marginBottom: 10 },
  buttonRow: { display: "flex", gap: 8 },
  button: {
    padding: "6px 10px",
    borderRadius: 6,
    border: "1px solid #ccc",
    background: "#fff",
    cursor: "pointer",
  },
  primaryButton: {
    padding: "6px 10px",
    borderRadius: 6,
    border: "none",
    background: "#0b5fff",
    color: "#fff",
    cursor: "pointer",
  },
};