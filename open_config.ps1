# Simple PowerShell script to open the config.ini file from the release directory root.
#
# @author Lukas Jeckle
# ================================================================================================================

# Path to the configuration file.
$config = Join-Path -Path $PSScriptRoot -ChildPath "_internal\config.ini"

# Check if file exists.
if (Test-Path $config)
{
    Start-Process -FilePath $config
}
else
{
    Write-Host "config.ini not found at: $config" -f Red
}