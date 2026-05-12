---
description: "Use when writing or modifying CSS/SCSS files. Enforce native CSS Nesting with hierarchical selectors mirroring HTML structure, CSS Custom Properties for theming, and component-based organization."
applyTo: "**/*.css, **/*.scss"
---

# CSS Nesting & Component Organization Guidelines

## Overview

This project uses **native CSS Nesting** with hierarchical selectors that mirror the HTML DOM structure. All styles should be organized by component and leverage CSS Custom Properties for maintainability and theming.

---

## 1. CSS Nesting Syntax (Native)

Use native CSS Nesting (supported in modern browsers) with the `&` selector:

### ✅ Do This

```css
/* Hero section - mirrors HTML hierarchy */
.hero-section {
  background: linear-gradient(135deg, var(--primary-color), #0a1a2e);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);

  & h1 {
    color: #fff;
    font-size: 2.5rem;
    margin-bottom: var(--spacing-md);
  }

  & p {
    color: var(--text-light);
    font-size: 1.1rem;
    max-width: 600px;
  }

  /* Modifier variant */
  &.dark-mode {
    background: linear-gradient(135deg, #1a2332, #0f1419);
  }
}
```

### ❌ Don't Do This

```css
/* Avoid flat selectors */
.hero-section { ... }
.hero-section h1 { ... }
.hero-section p { ... }
.hero-section.dark-mode { ... }

/* Avoid old SCSS patterns that don't validate as CSS Nesting */
.hero-section {
  h1: { }    /* Invalid syntax */
}
```

---

## 2. Reflect HTML Hierarchy

**Principle**: CSS structure follows DOM nesting exactly. If your HTML is:

```html
<div class="section-card">
  <h3 class="card-title">Título</h3>
  <div class="card-body">
    <p>Conteúdo</p>
    <button class="btn btn-primary">Ação</button>
  </div>
  <footer class="card-footer">
    <small>Rodapé</small>
  </footer>
</div>
```

**Then your CSS mirrors that structure:**

```css
.section-card {
  background: #fff;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-md);

  & .card-title {
    font-size: 1.25rem;
    color: var(--primary-color);
    margin-bottom: var(--spacing-sm);
  }

  & .card-body {
    margin-bottom: var(--spacing-md);

    & p {
      color: var(--text-default);
      line-height: 1.6;
    }

    & .btn {
      margin-top: var(--spacing-sm);
    }
  }

  & .card-footer {
    border-top: 1px solid var(--border-color);
    padding-top: var(--spacing-sm);
    color: var(--text-muted);
  }
}
```

---

## 3. CSS Custom Properties (Variables)

**Always use CSS Custom Properties** for:
- Colors (primary, secondary, text, backgrounds)
- Spacing (padding, margins, gaps)
- Border radius (consistent roundness)
- Shadows
- Transitions/animations

### Root Level (`:root` + Dark Mode)

```css
:root {
  /* Colors */
  --primary-color: #01244A;
  --secondary-color: #0a5a8f;
  --brand-accent: #fbdc06;
  
  --text-default: #333;
  --text-light: #666;
  --text-muted: #999;
  
  --bg-light: #f8f9fa;
  --bg-white: #fff;
  --border-color: #ddd;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
}

/* Dark Mode Overrides */
[data-bs-theme="dark"] {
  --text-default: #f0f0f0;
  --text-light: #ccc;
  --bg-light: #1a1a1a;
  --bg-white: #2a2a2a;
  --border-color: #444;
  --brand-accent: #fbdc06;
}
```

---

## 4. Component Organization

Organize CSS into semantic components that match your HTML structure:

### Layout Components
- `.hero-section` - Hero banner
- `.navbar-custom` - Navigation bar
- `.footer-section` - Footer area
- `.sidebar` - Sidebar container

### Form Components
- `.form-section` - Form container
- `.form-group-compact` - Compact form groups
- `.form-grid-full` - Full-width form grid
- `.form-grid-compact` - Auto-fit grid (200px min)

### Card/List Components
- `.section-card` - Generic card container
- `.kit-item` - Kit list item
- `.lead-item` - Lead card

### State/Utility
- `.empty-state` - Empty state messaging
- `.loading` - Loading state
- `.error` - Error styling

### Example Organized Structure

```css
/* ========================================
   LAYOUT COMPONENTS
   ======================================== */

.hero-section {
  /* Hero styles */
}

.navbar-custom {
  /* Navbar styles */
}

/* ========================================
   FORM COMPONENTS
   ======================================== */

.form-section {
  /* Form container */

  & .form-group-compact {
    /* Compact form group */
  }

  & .form-grid-compact {
    /* Grid layout */
  }
}

/* ========================================
   CARD COMPONENTS
   ======================================== */

.section-card {
  /* Card styles */

  & .card-title {
    /* Title in card */
  }

  & .card-body {
    /* Body content */
  }
}

.kit-item {
  /* Kit item styles */
}

/* ========================================
   STATE & UTILITIES
   ======================================== */

.empty-state {
  /* Empty state styling */
}

.loading {
  /* Loading indicator */
}
```

---

## 5. Responsiveness

Use media queries **within the component** to keep related styles together:

```css
.section-card {
  padding: var(--spacing-md);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);

  & h2 {
    font-size: 1.5rem;
  }

  /* Mobile first - responsive at larger breakpoints */
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    padding: var(--spacing-sm);

    & h2 {
      font-size: 1.25rem;
    }
  }

  @media (min-width: 1200px) {
    padding: var(--spacing-lg);

    & h2 {
      font-size: 1.75rem;
    }
  }
}
```

---

## 6. Bootstrap Integration

When using Bootstrap classes alongside custom CSS:

```css
.hero-section {
  /* Custom styles for hero */

  & .btn {
    /* Override or extend Bootstrap button */
    border-radius: var(--radius-md);
    transition: all var(--transition-normal);

    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }
  }

  & .container-lg {
    /* Customize Bootstrap container */
    max-width: 1000px;
  }
}
```

---

## 7. Best Practices

✅ **Do:**
- Keep nesting **3-4 levels deep** max for readability
- Use meaningful class names that describe the component
- Group related properties (colors, layout, effects)
- Prefix component variations with `&`
- Use CSS variables for all colors, spacing, and effects
- Add comments for sections (Layout, Forms, Cards, etc.)
- Test in modern browsers (CSS Nesting support: Chrome 120+, Firefox 117+, Safari 16.5+)

❌ **Don't:**
- Nest too deeply (hurts readability and CSS performance)
- Use `!important` (indicates design problem)
- Mix inline styles in HTML with CSS file styles
- Create class names that don't match component intent
- Repeat magic numbers—use variables instead
- Forget dark mode support (use `[data-bs-theme="dark"]`)

---

## 8. Browser Support Note

Native CSS Nesting is supported in:
- ✅ Chrome 120+
- ✅ Firefox 117+
- ✅ Safari 16.5+
- ✅ Edge 120+
- ⚠️ IE 11: Not supported (no longer recommended)

If you need older browser support, consider using a CSS preprocessor (Sass/SCSS) or PostCSS plugin.

---

## Examples

### Complete Component Example

```css
.kit-item {
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  transition: all var(--transition-normal);

  & .kit-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);

    & h4 {
      color: var(--primary-color);
      font-size: 1.125rem;
      margin: 0;
    }

    & .kit-status {
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.875rem;
      background: var(--bg-light);
      color: var(--text-muted);
    }
  }

  & .kit-description {
    color: var(--text-light);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: var(--spacing-md);
  }

  & .kit-actions {
    display: flex;
    gap: var(--spacing-sm);

    & .btn {
      flex: 1;
      padding: 0.5rem 1rem;
      border-radius: var(--radius-sm);
    }
  }

  /* Hover effect */
  &:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--primary-color);
  }

  /* Dark mode */
  @media (prefers-color-scheme: dark) {
    background: var(--bg-white);
    border-color: var(--border-color);
  }
}
```

---

## Related Documentation

- [MDN CSS Nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting)
- [Bootstrap 5.3.8 Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
