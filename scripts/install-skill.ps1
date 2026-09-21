<#
.SYNOPSIS
    Install the genie-dashboard-design skill for GitHub Copilot (VS Code) or Claude Code.

.DESCRIPTION
    Two modes:

      Personal - installs to your user profile; works in EVERY repo you open,
                 commits nothing, needs no permissions on the team repo.
      Repo     - vendors the skill into one repository so the whole team gets it
                 on clone. Requires commit access to that repo.

    Copilot scans .github/skills/, .claude/skills/ and .agents/skills/ in a workspace,
    and ~/.copilot/skills/, ~/.claude/skills/, ~/.agents/skills/ for personal installs.
    Claude Code scans .claude/skills/ - so .claude/skills covers both tools.

.PARAMETER TargetRepo
    Path to the repository to install into. Omit when using -Personal.

.PARAMETER Personal
    Install to your user profile instead of a repository.

.PARAMETER Dir
    Subdirectory to install into. Defaults to .github/skills for a repo install,
    or .copilot/skills for a personal install.

.EXAMPLE
    .\scripts\install-skill.ps1 -Personal

.EXAMPLE
    .\scripts\install-skill.ps1 C:\work\OSLAUNCH

.EXAMPLE
    .\scripts\install-skill.ps1 C:\work\OSLAUNCH -Dir .claude\skills
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetRepo,

    [switch]$Personal,

    [string]$Dir
)

$ErrorActionPreference = 'Stop'

$SkillName = 'genie-dashboard-design'
$SourceDir = Join-Path (Split-Path -Parent $PSScriptRoot) "skills\$SkillName"

if ($Personal) {
    $TargetRoot = $env:USERPROFILE
    if (-not $Dir) { $Dir = '.copilot\skills' }
}
elseif ($TargetRepo) {
    $TargetRoot = $TargetRepo
    if (-not $Dir) { $Dir = '.github\skills' }
}
else {
    Write-Error "Specify a target repo, or -Personal. See: Get-Help .\scripts\install-skill.ps1"
    exit 1
}

if (-not (Test-Path -LiteralPath $TargetRoot)) {
    Write-Error "Target does not exist: $TargetRoot"
    exit 1
}

if (-not (Test-Path -LiteralPath (Join-Path $SourceDir 'SKILL.md'))) {
    Write-Error "Cannot find the skill at $SourceDir - run this from a clone of the plugin repo."
    exit 1
}

$Dest = Join-Path (Join-Path $TargetRoot $Dir) $SkillName

if (Test-Path -LiteralPath $Dest) { Remove-Item -LiteralPath $Dest -Recurse -Force }
New-Item -ItemType Directory -Path $Dest -Force | Out-Null

Copy-Item -Path (Join-Path $SourceDir '*') -Destination $Dest -Recurse -Force
Get-ChildItem -LiteralPath $Dest -Recurse -Force -Directory |
    Where-Object { $_.Name -eq '__pycache__' } |
    Remove-Item -Recurse -Force

$FileCount = (Get-ChildItem -LiteralPath $Dest -Recurse -File).Count
Write-Host "Installed $SkillName ($FileCount files)"
Write-Host "  -> $Dest"
Write-Host ""

if ($Personal) {
    Write-Host "This is a personal install: the skill is available in every repo you open,"
    Write-Host "and nothing is added to any project's git history."
    Write-Host ""
    Write-Host "To update later, re-run this command after pulling the latest plugin repo."
}
elseif (-not (Test-Path -LiteralPath (Join-Path $TargetRoot '.git'))) {
    Write-Host "Note: $TargetRoot is not a git repository, so this copy is local to you."
}
else {
    Write-Host "Commit it so the whole team gets it on their next pull:"
    Write-Host "  cd `"$TargetRoot`""
    Write-Host "  git add $Dir\$SkillName"
    Write-Host "  git commit -m 'Add $SkillName skill'"
}

Write-Host ""
Write-Host "In VS Code, open Copilot Chat in agent mode and type / to see the skill,"
Write-Host "or just describe the dashboard you want - Copilot loads it by description."
