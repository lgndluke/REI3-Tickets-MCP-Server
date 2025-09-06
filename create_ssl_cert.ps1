# Simple PowerShell script to create a self-signed SSL certificate for the REI3-Tickets-MCP-Server's web-server.
#
# @author Lukas Jeckle
# ================================================================================================================

try
{
	# Check if OpenSSL is installed.
	if (-not (Get-Command openssl -ErrorAction SilentlyContinue))
	{
		throw "OpenSSL is not installed. Please install OpenSSL and try again."
	}
	else
	{
		Write-Host "Found: OpenSSL"
	}

    Write-Host ""

    # Create .\ssl\ directory.
    try
    {
        $ssl_path = Join-Path -Path $PSScriptRoot -ChildPath "ssl"
        if (-not (Test-Path -Path $ssl_path))
        {
            New-Item -ItemType Directory -Path $ssl_path -ErrorAction Stop
            Write-Host "Created directory at: $ssl_path"
        }
        else
        {
            Write-Host "Found: $ssl_path"
        }
    }
    catch
    {
        Write-Error "Failed to create ssl directory: $_"
    }

    Write-Host ""

    # Create ssl_cert.crt and ssl_key.key files inside .\ssl\ directory using OpenSSL.
    try
    {
        $ssl_crt_path = Join-Path -Path $PSScriptRoot -ChildPath "ssl\ssl_cert.crt"
        $ssl_key_path = Join-Path -Path $PSScriptRoot -ChildPath "ssl\ssl_key.key"

        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $ssl_key_path -out $ssl_crt_path
    }
    catch
    {
        Write-Error "Failed to create SSL certificate and key files: $_"
    }

    Write-Host ""

    Write-Host "Next steps:"
    Write-Host "1. Open the config.ini file."
    Write-Host "2. Set the 'enable' of the [web-server] to 'true'."
    Write-Host "3. Paste the path to the ssl_cert.crt into the 'ssl_cert_file' variable."
    Write-Host "   (e.g.: ssl_cert_file = C:\<<SOME_PATH>>\ssl\ssl_cert.crt             "
    Write-Host "4. Paste the path to the ssl_key.key into the 'ssl_key_file' variable."
    Write-Host "   (e.g.: ssl_key_file = C:\<<SOME_PATH>>\ssl\ssl_key.key             "
    Write-Host "5. Adjust the other settings of the [web-server] section as needed."

    Write-Host ""

    $userInput = Read-Host "Press any button to close the script"
}
catch
{
    Write-Error "$_"
}
finally
{
    Write-Host "Script finished."
}