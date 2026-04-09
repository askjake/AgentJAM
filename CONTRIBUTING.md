# Contributing to AgentJAM

Thank you for considering contributing to AgentJAM! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Provide detailed information**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs

### Suggesting Features

1. **Check existing feature requests** first
2. **Clearly describe the use case** and benefit
3. **Provide examples** of how it would work
4. **Consider backward compatibility**

### Pull Requests

#### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/AgentJAM.git
cd AgentJAM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

#### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, commented code
   - Follow PEP 8 style guide
   - Add type hints where appropriate

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Check linting
   flake8 src/
   
   # Format code
   black src/
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: Brief description
   
   - Detailed point 1
   - Detailed point 2"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub

#### PR Guidelines

- **Title**: Clear, descriptive summary
- **Description**: 
  - What changes were made
  - Why they were needed
  - Any breaking changes
  - Related issues (use `Fixes #123`)
- **Tests**: Include tests for new features
- **Documentation**: Update relevant docs
- **Commits**: Keep history clean and logical

### Code Style

```python
# Good
def calculate_complexity(query: str) -> float:
    """
    Calculate query complexity score.
    
    Args:
        query: User input query string
    
    Returns:
        Complexity score between 0.0 and 1.0
    """
    score = 0.0
    # Implementation
    return score

# Bad
def calc(q):  # No types, no docstring
    s=0.0  # Poor naming, no spaces
    return s
```

### Testing

- Write unit tests for new functions
- Ensure existing tests pass
- Aim for >80% code coverage
- Test edge cases and error conditions

```python
# Example test
def test_model_selection():
    selector = ModelSelector(config)
    
    # Test high complexity
    result = selector.select_model("Design a complex architecture")
    assert result["name"] == "Claude Opus 4.6"
    
    # Test low complexity
    result = selector.select_model("Is service running?")
    assert result["name"] == "Claude Haiku 4.5"
```

### Documentation

- Update README.md for user-facing changes
- Update docs/ for architectural changes
- Add docstrings to all public functions
- Include examples for new features

## Release Process

(For maintainers)

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create release tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions will build and publish

## Questions?

- Open a discussion on GitHub Discussions
- Tag issues with `question` label
- Reach out to maintainers

## Thank You!

Every contribution helps make AgentJAM better for everyone. We appreciate your time and effort! 🙏
