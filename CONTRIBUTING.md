# Contributing to Book Tracker

This document outlines the standards and best practices for contributing to the Book Tracker project.

## Code Organization

### Frontend Structure
```
frontend/
├── src/
│   ├── lib/           # Svelte components
│   ├── styles/        # SCSS styles
│   │   ├── base/      # Base styles, variables, resets
│   │   ├── layouts/   # Layout styles
│   │   └── components/# Component-specific styles
│   └── main.ts        # Application entry point
```

## Styling Guidelines

### 1. SCSS Organization
- All styles MUST be in dedicated SCSS files under the `src/styles` directory
- NO styles should be written in Svelte components using the `<style>` tag
- Component-specific styles should be in `src/styles/components/_component-name.scss`
- Layout styles should be in `src/styles/layouts/_layout-name.scss`
- Base styles and variables should be in `src/styles/base/`

### 2. SCSS File Naming
- All SCSS files should be prefixed with an underscore (_)
- Use kebab-case for file names (e.g., `_book-list.scss`)
- Component styles should match their component name (e.g., `BookList.svelte` → `_book-list.scss`)

### 3. SCSS Imports
- All SCSS files must be imported in `main.scss`
- Use proper namespacing to avoid conflicts (e.g., `@use './layouts/book-list' as book-list-layout`)
- Always import variables first: `@use '../base/variables' as *`

### 4. Variables and Constants
- Use variables from `_variables.scss` for consistent styling
- Common values that should use variables:
  - Colors
  - Spacing
  - Border radius
  - Shadows
  - Transitions
  - Breakpoints

## Component Guidelines

### 1. Svelte Components
- Keep styles separate from components
- Use semantic HTML elements
- Include proper ARIA attributes for accessibility
- Add keyboard event handlers for interactive elements

### 2. Component Organization
- Group related components in appropriate directories
- Keep components focused and single-responsibility
- Extract reusable logic into stores or utilities

## Best Practices

### 1. Accessibility
- Include proper ARIA labels
- Ensure keyboard navigation works
- Maintain proper color contrast
- Provide text alternatives for non-text content

### 2. Responsive Design
- Use the defined breakpoints from variables
- Test layouts at all screen sizes
- Ensure mobile-first approach

### 3. Performance
- Minimize CSS specificity
- Use CSS Grid and Flexbox for layouts
- Avoid deeply nested selectors

## Development Workflow

1. Create feature branch from main
2. Follow style guidelines
3. Test changes across different screen sizes
4. Submit pull request
5. Address review feedback

## Questions?

If you're unsure about any of these guidelines, please open an issue for discussion.
