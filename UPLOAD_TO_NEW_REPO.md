# Guide: Upload Project to New GitHub Repository

## Step 1: Create New Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: e.g., `crack-detector-pi` or `raspberry-pi-crack-detection`
   - **Description** (optional): "Raspberry Pi 4B crack detection system with OpenCV"
   - **Visibility**: Choose Public or Private
   - **DO NOT** check "Initialize this repository with a README"
   - **DO NOT** add .gitignore or license
3. Click **"Create repository"**

## Step 2: Update Remote URL

After creating the repo, GitHub will show you the repository URL. Use one of these methods:

### Method A: Using HTTPS (Easier, requires GitHub password/token)

```bash
cd ~/MJP  # or your project directory

# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Verify the change
git remote -v

# Push to new repository
git push -u origin main
```

### Method B: Using SSH (Requires SSH key setup)

```bash
cd ~/MJP  # or your project directory

# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# Verify the change
git remote -v

# Push to new repository
git push -u origin main
```

## Step 3: Push Your Code

```bash
# Make sure you're in the project directory
cd ~/MJP

# Push all branches and tags to new repo
git push -u origin main

# If you have other branches, push them too:
# git push -u origin --all
# git push -u origin --tags
```

## Alternative: Keep Both Remotes

If you want to keep the old repo AND add the new one:

```bash
# Add new remote with a different name
git remote add new-origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to new remote
git push -u new-origin main

# To push to both:
# git push origin main    # old repo
# git push new-origin main # new repo
```

## Verify Upload

1. Go to your new repository on GitHub
2. You should see all your files:
   - `src/` directory with all Python files
   - `scripts/` directory
   - `configs/` directory
   - `README.md`, `SETUP_PI.md`, etc.

## Troubleshooting

### Authentication Issues (HTTPS)

If you get authentication errors with HTTPS:
- Use a Personal Access Token instead of password
- Create token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
- Use the token as your password when pushing

### Permission Denied (SSH)

If SSH doesn't work:
- Make sure you have SSH keys set up: `ssh -T git@github.com`
- Or switch to HTTPS method

### Repository Already Exists Error

If you get "repository already exists":
- Make sure you created an empty repository (no README)
- Or use: `git push -u origin main --force` (⚠️ only if you're sure!)

## Quick Reference

```bash
# Check current remote
git remote -v

# Change remote URL
git remote set-url origin NEW_URL

# Push to new repo
git push -u origin main
```

