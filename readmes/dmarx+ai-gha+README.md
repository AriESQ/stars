# 

## Introduction

This is a template repository that provides a foundation for GitHub Action-based agents. It includes a modular system for dynamic documentation generation and other reusable components that make it easier to build and maintain agent-driven workflows.

### Key Features

- Modular documentation system with Jinja2 templates
- Automatic project structure documentation
- Reusable GitHub Actions workflows
- Centralized configuration management
- Utility functions for common operations
- Clean, maintainable architecture optimized for AI agents
- Built-in test framework with pytest
- Automated workflow dependencies
- Git operations handled through utilities
## Repository Setup

### Required Repository Settings

1. **Workflow Permissions**
   - Go to Repository Settings → Actions → General → Workflow permissions
   - Enable "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

2. **Branch Protection** (Optional but recommended)
   - Go to Repository Settings → Branches → Branch protection rules
   - Add rule for your main branch (e.g., `main` or `master`)
   - Enable:
     - "Require pull request reviews before merging"
     - "Require status checks to pass before merging"
   - Allow:
     - "Allow specific actors to bypass required pull requests"
     - Add "github-actions[bot]" to the bypass list

### Required Secrets and Variables

No additional secrets are required for basic functionality. The workflows use the default `GITHUB_TOKEN` which is automatically provided.

### Repository Setup Commands

If you're setting up using GitHub CLI, you can run these commands:
```bash
# Enable workflows
gh repo edit --enable-actions

# Set workflow permissions
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/OWNER/REPO/actions/permissions/workflow" \
  -f default_workflow_permissions='write' \
  -F can_approve_pull_request_reviews=true

# Enable Issues (recommended for tracking)
gh repo edit --enable-issues
```

Replace `OWNER/REPO` with your repository details.

### Common Issues

1. **Workflow Permission Errors**
   - Error: "Resource not accessible by integration"
   - Solution: Ensure workflow permissions are set to "Read and write"

2. **Git Push Failures**
   - Error: "GitHub Actions is not permitted to create or approve pull requests"
   - Solution: Check "Allow GitHub Actions to create and approve pull requests"

3. **Workflow Trigger Issues**
   - Error: Workflows not triggering each other
   - Solution: Ensure `GITHUB_TOKEN` has sufficient permissions and "Read and write permissions" is enabled
## Usage

### Installation

This project is designed to be used as a template repository. To get started:

1. Click "Use this template" on GitHub
2. Clone your new repository
3. Install the development dependencies:
   ```bash
   pip install -e ".[test]"
   ```

### Dynamic README Generation

The README is automatically generated from templates in `docs/readme/`. The system works as follows:

1. Base template (`docs/readme/base.md.j2`) defines the overall structure
2. Individual sections are stored in `docs/readme/sections/` as separate templates
3. Configuration is centralized in `pyproject.toml`
4. GitHub Actions automatically rebuild the README when:
   - Templates are modified
   - Project structure changes
   - Configuration is updated

To manually trigger a README rebuild:
```bash
python -m readme_generator readme
```

### Project Structure Management

The repository includes automatic project structure documentation:

1. Structure is updated on file changes
2. Tree output is formatted as a template
3. README is automatically rebuilt to include the new structure

To manually update the structure:
```bash
python -m readme_generator structure
```

### Testing

The project uses pytest for testing. To run tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=readme_generator

# Run specific test file
pytest tests/test_tree_generator.py
```

Tests are automatically run:
- On every push to main
- When workflows are triggered
- Before README updates
- Before structure updates

### Development

This project follows a modular design principle to make it easier for AI agents to work with the codebase:

- Each component is self-contained and focused
- Configuration is centralized in `pyproject.toml`
- Utilities are designed to be reusable across workflows
- Git operations are handled through utility functions
- All features are tested using pytest

To add new README sections:
1. Create a new template in `docs/readme/sections/`
2. Include it in `docs/readme/base.md.j2`
3. Add any necessary configuration to `pyproject.toml`
4. Add tests for new functionality
## Development Guidelines

### Code Organization for LLM Interaction

When developing this project (or using it as a template), keep in mind these guidelines for effective collaboration with Large Language Models:

1. **Separation of Concerns**
   - Each package should have a single, clear responsibility
   - New features should be separate packages when appropriate
   - Avoid coupling between packages
   - Use consistent patterns across packages, but implement independently
   - Cross-cutting concerns should use shared conventions

2. **File Length and Modularity**
   - Keep files short and focused on a single responsibility
   - If you find yourself using comments like "... rest remains the same" or "... etc", the file is too long
   - Files should be completely replaceable in a single LLM interaction
   - Long files should be split into logical components

3. **Dependencies**
   - All dependencies managed in `pyproject.toml`
   - Optional dependencies grouped by feature:
     ```toml
     [project.optional-dependencies]
     test = ["pytest", ...]
     site = ["markdown2", ...]
     all = ["pytest", "markdown2", ...]  # Everything
     ```
   - Use appropriate groups during development:
     ```bash
     pip install -e ".[test]"  # Just testing
     pip install -e ".[all]"   # Everything
     ```

4. **Testing Standards**
   - Every new feature needs tests
   - Tests should be clear and focused
   - Use pytest fixtures for common setups
   - All workflows depend on tests passing
   - Test files should follow same modularity principles

5. **Why This Matters**
   - LLMs work best with clear, focused contexts
   - Complete file contents are better than partial updates with ellipsis
   - Tests provide clear examples of intended behavior
   - Shorter files make it easier for LLMs to:
     - Understand the complete context
     - Suggest accurate modifications
     - Maintain consistency
     - Avoid potential errors from incomplete information

6. **Real World Example**
   Our own organization follows these principles:
   ```
   src/
   ├── readme_generator/  # Core README generation
   │   ├── generators/
   │   └── utils.py
   └── site_generator/    # Demo site generation
       ├── generator.py
       └── __main__.py
   ```

7. **Best Practices**
   - Aim for files under 200 lines
   - Each file should have a single, clear purpose
   - Use directory structure to organize related components
   - Prefer many small files over few large files
   - Consider splitting when files require partial updates
   - Write tests alongside new features
   - Run tests locally before pushing
# LLM-Focused Summary System

## Overview
The project includes an automated summary generation system designed to help LLMs efficiently work with the codebase. This system generates both local directory summaries and project-wide summaries to provide focused, relevant context for different tasks.

## Types of Summaries

### Directory Summaries
Each directory in the project contains a `SUMMARY` file that concatenates all text files in that directory. This provides focused, local context when working on directory-specific tasks.

### Project-Wide Summaries
Special project-wide summaries are maintained in the `SUMMARIES/` directory on the `summaries` branch:

- `READMEs.md`: Concatenation of all README files in the project
- `README_SUBs.md`: Same as above but excluding the root README
- `PYTHON.md`: Structured view of all Python code including:
  - Function and class signatures
  - Type hints
  - Docstrings
  - Clear indication of class membership

## Accessing Summaries

### Directory Summaries
These are available on any branch in their respective directories:
```bash
# Example: View summary for the readme_generator package
cat src/readme_generator/SUMMARY
```

### Project-Wide Summaries
These live exclusively on the `summaries` branch:
```bash
# Switch to summaries branch
git checkout summaries

# View available summaries
ls SUMMARIES/
```

## Using Summaries Effectively

### For Local Development
Directory summaries are useful when:
- Getting up to speed on a specific package
- Understanding local code context
- Planning modifications to a package

### For Project-Wide Understanding
The `SUMMARIES/` directory helps with:
- Understanding overall project structure
- Finding relevant code across packages
- Reviewing API signatures and documentation
- Planning cross-package changes

### For LLM Interactions
- Point LLMs to specific summaries based on the task
- Use directory summaries for focused work
- Use project-wide summaries for architectural decisions
- Combine different summaries as needed for context

## Implementation Notes
- Summaries are automatically updated on every push to `main`
- The `summaries` branch is workflow-owned and force-pushed on updates
- Summary generation is configured in `pyproject.toml` under `[tool.summary]`
- Don't modify summaries directly - they're automatically generated
## GitHub Pages

### Requirements

1. **Public Repository**
   - GitHub Pages is available out-of-the-box for public repositories
   - For private repositories, a GitHub Enterprise plan is required
   - If you plan to make your repository public later, you can still set up and test the site generation locally

2. **Repository Settings**
   - Once your repository is public (or on an Enterprise plan):
     - Go to Repository Settings → Pages
     - Under "Build and deployment":
       - Set Source to "GitHub Actions"

3. **Branch Setup**
   - Create a `gh-pages` branch:
     ```bash
     git checkout --orphan gh-pages
     git reset --hard
     git commit --allow-empty -m "Initial gh-pages commit"
     git push origin gh-pages
     git checkout main  # Return to main branch
     ```
   - This branch is required for GitHub Pages deployment
   - The deployment workflow will manage this branch automatically once created

### Installation

```bash
# Install with site generation dependencies
pip install -e ".[all]"
```

### Local Development

The site generator can be used locally regardless of repository visibility:

```bash
# Generate site locally
python -m site_generator build

# Site will be generated in _site/ directory (git-ignored)
# View the generated site by opening _site/index.html in your browser
```

### GitHub Actions Integration

When requirements are met (public repository or Enterprise plan), the site automatically rebuilds and deploys when:
- The README is updated through the `build-readme` workflow
- The deployment workflow is modified
- The workflow is manually triggered

### File Structure

```
your-repo/
├── _site/           # Generated directory (git-ignored)
│   └── index.html   # Generated site
├── docs/
│   └── site/       
│       └── template.html  # Site template
└── src/
    └── site_generator/   # Generator package
```

### Customization

The site template is located in `docs/site/template.html` and can be customized with:
- Custom CSS styles
- Additional JavaScript
- Modified layout and structure
- Custom header/footer content

### Command Line Usage

```bash
# Generate site with default settings
python -m site_generator build

# Specify custom output directory
python -m site_generator build --output_dir="custom_dir"
```

### Testing

The site generation can be tested locally even if GitHub Pages deployment isn't available:
```bash
# Run the test suite
pytest tests/test_site_generator.py
```

### Troubleshooting

#### Common Issues

1. **"Resource not accessible by integration" Error**
   - **Problem**: Deployment fails with "Resource not accessible by integration" or "Create Pages site failed"
   - **Solution**: Ensure you've:
     1. Created the `gh-pages` branch (see Branch Setup section above)
     2. Enabled GitHub Pages in repository settings
     3. Set source to "GitHub Actions" in Pages settings
     4. Enabled proper workflow permissions

2. **Deployment Not Starting**
   - **Problem**: Workflow runs but site doesn't deploy
   - **Solution**: Verify that:
     1. Repository is public or on Enterprise plan
     2. `gh-pages` branch exists
     3. Workflow has correct permissions in repository settings

3. **Empty Site Deployment**
   - **Problem**: Site deploys but shows no content
   - **Solution**: Check that:
     1. Build step is generating content in `_site` directory
     2. `upload-pages-artifact` step has correct path
     3. Site generator is installed with all dependencies

For any persistent issues, check the workflow run logs for specific error messages and ensure all setup steps have been completed in order.
## Project Structure

The repository is organized as follows:

```
ai-gha
├── .github
│   └── workflows
│       ├── README.md
│       ├── build-readme.yml
│       ├── deploy-gh-pages.yml
│       ├── generate-summaries.yml
│       ├── test.yml
│       └── update-structure.yml
├── .gitignore
├── LICENSE
├── README.md
├── docs
│   ├── README.md
│   ├── readme
│   │   ├── README.md
│   │   ├── base.md.j2
│   │   └── sections
│   │       ├── development.md.j2
│   │       ├── introduction.md.j2
│   │       ├── prerequisites.md.j2
│   │       ├── site.md.j2
│   │       ├── structure.md.j2
│   │       ├── summaries.md.j2
│   │       ├── todo.md.j2
│   │       └── usage.md.j2
│   └── site
│       ├── README.md
│       └── template.html
├── pyproject.toml
├── src
│   ├── README.md
│   ├── readme_generator
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── generators
│   │   │   ├── README.md
│   │   │   ├── __init__.py
│   │   │   ├── readme_generator.py
│   │   │   ├── structure_generator.py
│   │   │   └── tree_generator.py
│   │   └── utils.py
│   ├── site_generator
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── generator.py
│   └── summary_generator
│       ├── README.md
│       ├── __init__.py
│       ├── __main__.py
│       ├── generator.py
│       ├── signature_extractor.py
│       └── special_summaries.py
└── tests
    ├── conftest.py
    ├── test_generators.py
    ├── test_site_generator.py
    ├── test_summary_generator.py
    └── test_tree_generator.py

```

### Key Components

- `.github/workflows/`: GitHub Actions workflow definitions
  - `build-readme.yml`: Automatically rebuilds README when content changes
  - `update-structure.yml`: Updates project structure documentation

- `docs/readme/`: README template files
  - `base.md.j2`: Main template file
  - `sections/`: Individual section templates

- `src/readme_generator/`: Core Python package
  - `generators/`: Generation components
    - `tree_generator.py`: Tree generation utilities
    - `readme_generator.py`: README generation logic
    - `structure_generator.py`: Structure documentation
  - `utils.py`: Shared utility functions
  - `__main__.py`: CLI entry point

- `pyproject.toml`: Project configuration and dependencies
## TODO

### Documentation Improvements
- [ ] Add automatic table of contents generation
- [ ] Add module summary with function signatures
- [ ] Expand documentation with more examples
- [ ] Add API integration instructions

### Feature Additions
- [ ] Add more utility functions for common agent operations
- [ ] Create workflow templates for common agent tasks
- [ ] Add more reusable components
- [ ] Add GitHub Pages integration for project documentation

### Testing Enhancements
- [ ] Add more test cases for edge cases
- [ ] Add integration tests for workflows
- [ ] Improve test coverage
