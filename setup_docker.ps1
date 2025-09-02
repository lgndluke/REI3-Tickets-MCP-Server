# Simple PowerShell script that can be used to setup the REI3 Tickets MCP servers Dockerfile.
#
# @author Lukas Jeckle
# ================================================================================================================

try
{
    # Check if Docker in installed.
    if (-not (Get-Command docker -ErrorAction SilentlyContinue))
    {
        throw "Docker is not installed. Please install Docker and try again."
    }
    else
    {
        Write-Host "Found: Docker"
    }

    # Check if Git is installed.
    if (-not (Get-Command git -ErrorAction SilentlyContinue))
    {
        throw "Git is not installed. Please install Git and try again."
    }
    else
    {
        Write-Host "Found: Git"
    }

    Write-Host ""

    # Build REI3 Tickets MCP servers docker image from Dockerfile.
    $dockerfilePath = ".\Dockerfile"
    if (-Not (Test-Path $dockerfilePath))
    {
        throw "Dockerfile not found. Ensure you're in the right directory."
    }

    $imageName = 'rei3_tickets_mcp_server'

    Write-Host "Building Docker image '$imageName' from Dockerfile ..."

    try
    {
        docker build -t $imageName .
    }
    catch
    {
        throw "Failed to build docker image."
    }

    Write-Host "Docker image '$imageName' was built successfully." -f Green
    Write-Host ""

    Write-Host "Recommendations:"
    Write-Host "  -> Change the host inside the config.ini file to: 0.0.0.0"
    Write-Host "  -> Enable the web-server for more convinient Tickets-API management."
    Write-Host ""
    Write-Host "You can create the container by using the following command:"
    Write-Host "docker run -d -p 54321:54321 --name rei3-tickets-mcp-server rei3_tickets_mcp_server"
    Write-Host ""
}
catch
{
    Write-Host "Error: $_" -f Red
}
finally
{
    Write-Host "Script finished."
}
