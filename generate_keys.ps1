# Simple PowerShell script for creating config values for the oidc_proxy's values:
#  - jwt_signing_key
#  - storage_encryption_key.
#
# @author Lukas Jeckle
# ================================================================================================================

try
{
    # Check if Python is executable
    if (-not (Get-Command python -ErrorAction SilentlyContinue))
    {
        throw "Python is not installed. Please install Python and try again."
    }
    else
    {
        Write-Host "Found: Python"
    }

    Write-Host ""

    try
    {
        python -c "from cryptography.fernet import Fernet; print(f'jwt_signing_key: {Fernet.generate_key().decode('utf-8')}')"
        python -c "from cryptography.fernet import Fernet; print(f'storage_encryption_key: {Fernet.generate_key().decode('utf-8')}')"
    }
    catch
    {
        throw "Failed to create keys. Ensure python has access to the module 'cryptography'."
    }

}
catch
{
    Write-Host "Error: $_" -f Red
}
finally
{
    Write-Host "Script finished."
}
