# HydroFish_Backend

1. **Install Docker:**
   Ensure that Docker is installed and updated to the latest version. You can download and install Docker from the [official website](https://www.docker.com/products/docker-desktop/).

   If you are using Windows Subsystem for Linux (WSL), you can install Docker Desktop for Windows and enable WSL integration. Refer to your operating system guide and WSL documentation for detailed instructions on [official website documentation](https://docs.docker.com/desktop/).

   ```bash
   wsl --install
   ```

2. Add a `.env` file in the root directory of the project similar to below.
   ```bash
   DB_NAME='hydrofish'
   DB_USER='user'
   DB_PASSWORD='1234'
   DB_HOST='db'
   ```
3. Type
   ```bash
   docker-compose up
   ```

### Common Windows Error:

**Error:** -bash: ./entrypoint.sh: /bin/bash^M: bad interpreter: No such file or directory

Or other .sh files

**Fix:** This error occurs due to Windows behavior that modifies files to have Windows line endings (CRLF). To fix this, change the line endings back to LF. One way to do this is by using the sed command:

```
sed -i -e 's/\r$//' entrypoint.sh
```

If you face issue, just message Mark.
