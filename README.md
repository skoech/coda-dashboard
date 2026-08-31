# CODA Dashboard
[![GitHub Actions](https://github.com/skoech/coda-dashboard/workflows/Build%20and%20Deploy/badge.svg)](https://github.com/skoech/coda-dashboard/actions)

The CODA dashboard is a static dashboard that tracks [Canonical's Open Documentation Academy (CODA)](https://documentation.academy/) issues across multiple public GitHub repositories.

The dashboard replaces the [GitHub issues list](https://github.com/canonical/open-documentation-academy/issues). Its purpose is to provide contributors with a single source of truth for CODA issues, and to eliminate the need for maintainers to duplicate issues across their parent repositories and that of CODA.

## How it works

**Configuration**: Repositories are defined in `config.yaml`, with specific per-repo labels to filter issues
**Fetching issues**: `fetch_issues.py` pulls issues with GitHub API using configured labels
**Building the frontend**: `build_frontend.py` generates static HTML using Jinja2 templates
**Deploying the dashboard**: GitHub Actions automatically builds and deploys the dashboard to GitHub Pages

## Usage

The dashboard helps contributors view open issues from all [projects particpating in CODA](https://documentation.academy/projects/), and browse through them using filters and tags. It enables maintainers to add their project(s) and then configure label or set of labels they want to use.

### For contributors

- All the open issues from all participating projects will be displayed on the dashboard. Check the counter on the header section to know the number of issues.
- Use dropowns to filter through the issues by project, label and whether an issue is assigned or not. 
- An issue card contains a project tag, a preview of the issue, and label tags for all labels associated with the issue. ![alt text](image.png)
  - These details are meant to give you context about the issue.
- Click on the *Read more* button to see the full issue on GitHub. You can also go to GitHub issue by clicking on the issue title.

### For maintainers

- To add a new project to be displayed on the dashboard, add your repository details to `config.yaml`:

```yaml
repositories:
  - owner: your-org-or-username # GitHub org or user
    repo: your-repo-name
    labels:
      - coda  # Or your custom label/set of labels
    maintainer(s):
      name: Your Name
      github: your-github-username
    contributor guide: https://link-to-contributor-guide
```

> [!IMPORTANT]
> The standard `coda` label is highly recommended for ease and uniformity, but if this is not possible for your project, please add a custom label or set of labels, which should be comma-separated.

> GitHub API uses AND logic for multiple labels. If you use a set of labels, only issues with **all** the labels specified will be fetched.

- Commit and push your changes to the repository.
  - The dashboard auto-updates hourly via GitHub Actions. If you want to see your changes immediately, trigger [the workflow](https://github.com/skoech/coda-dashboard/actions/workflows/deploy_dashboard.yml) manually.


## Contribute to the CODA dashboard

The dashboard is its very early stages, so we welcome different kinds of contributions to make it better:

- Report a bug
- Suggest a new feature.
- Improve the user interface
- Improve documentation
- Optimize performance
- Share your ideas for making the CODA an the dashboard more useful

To raise a bug or request a new feauture, [open an issue](https://github.com/skoech/coda-dashboard/issues/new) in the dashboard repository.

Chat to us on our [Matrix forum](https://matrix.to/#/#documentation:ubuntu.com) about how to make the dashboard and the community better, or if you need any help.

To make a contribution, build the dashboard locally, make your changes, test them and submit a pull request.

### How to build the dashboard locally

The dashboard is automatically deployed to GitHub Pages. To run locally:

1. Fork the repository

2. Clone your fork and navigate to the `coda-dashboard` directory:

  ```bash
  git clone git@github.com:your-username/coda-dashboard.git
  cd coda-dashboard
  ```

3. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. To test if the issues are being fetched properly:

   ```bash
   python3 fetch_issues.py
   ```

6. Build the dashboard:

   ```bash
   python3 build_frontend.py
   ```

7. Open `index.html` in your browser to serve the dashboard

## License

CODA Dashboard is free and open source software distributed under the Apache-2.0 license.

© 2026 Canonical Ltd.
