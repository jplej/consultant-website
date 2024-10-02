# Step 1: Build the Jekyll site
Write-Host "Building the site..."
bundle exec jekyll build

# Step 2: Ensure there are no uncommitted changes on the 'main' branch
Write-Host "Checking for uncommitted changes on 'main' branch..."
if (-not (git diff --quiet)) {
    Write-Host "You have uncommitted changes on 'main'. Commit or stash them before running the script."
    exit 1
}

# Step 3: Switch to the 'publish' branch (create it if it doesn't exist)
Write-Host "Switching to the 'publish' branch..."
git checkout publish
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating 'publish' branch..."
    git checkout -b publish
}

# Step 4: Remove existing files in the 'publish' branch
Write-Host "Cleaning up old files in 'publish' branch..."
git rm -rf .

# Step 5: Copy the contents of the _site directory into the root of the 'publish' branch
Write-Host "Copying the contents of _site..."
Copy-Item -Recurse -Force _site/* .

# Step 6: Add and commit changes on the 'publish' branch
Write-Host "Committing changes to 'publish' branch..."
git add .
git commit -m "Deploy site to 'publish' branch"

# Step 7: Push changes to the 'publish' branch
Write-Host "Pushing changes to 'publish' branch..."
git push origin publish --force

# Step 8: Switch back to the 'main' branch safely
Write-Host "Switching back to 'main' branch..."
git checkout main
