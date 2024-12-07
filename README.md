# ShopBot
### A project made by Owen Schmidt for any discord server. This bot allows users to make transactions in exchange for items, and also implements a currency to help these transactions.

## About
Uses MongoDB to store inventories of users that are tied to their discord ids. Uses discordpy to interface with discord. 

### Commands
/pay
/give
/inventory

## Usage
To use, add a .env file to your local version, and paste this in, where {token} is your apps discord token, and {server} is your mongodb server.
````
.env

DISCORD_TOKEN={token}
SERVER={server}
````
