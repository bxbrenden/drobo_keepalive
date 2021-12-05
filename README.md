# Drobo Keepalive

## Description
For whatever reason (energy efficiency, I think), my Drobo 5N goes to sleep after a while.
This sleeping breaks my Plex service.
Therefore, I made this tool to write a small timestamp to a file on the Drobo every minute.

## Running the Docker Container
```bash
docker run --name drobo-keepalive -v /etc/localtime:/etc/localtime -d --restart unless-stopped -v /drobo/Videos:/drobo/Videos bxbrenden/drobo_keepalive:latest
```
