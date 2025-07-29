# Simple PowerShell script to install the commit message hook.
#
# @author lgndluke
# ================================================================================================================

try
{
    Copy-Item commit-msg .git\hooks
    Write-Host "Successfully installed commit-msg hook!" -f Green
}
catch
{
    Write-Error "Failed to install commit-msg hook!"
}
finally
{
    Write-Host "Script finished."
}
