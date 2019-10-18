Github URL:
-------------
https://github.com/rmit-s3603315-benjamin-randall/HurricaneExchange/

Live project:
------------------
https://hurricane-exchange-staging.herokuapp.com

Release Notes
----------------

	v0.1 Alpha:


		Extremely basic site with bare functionality
		Includes:
		- Account creation and login
		- Account dashboard
		- Modify user avatar
		- View stocks
		- Create trading accounts
		- View trading accounts

	v0.2 Alpha:

		Trading:
		- Buying Stocks
		- Selling Stocks
		- Prices and day change are now stored and can be views on stock list
		- Trading accounts can now be deleted

		Account:
		- Users now require an email when registering.
		- Simple access to avatar changing

		UI:
		- Converted Interface over to use Bootstrap 4
		- Prompts to help users once they log in for the first time/have no trading account.
		- stock list page no supports jumping forwards and backwards 10 pages.

		Back-end:
		- Transaction history model, not yet implemented for users.

	v0.3 Alpha:

		Leaderboard:

		- users are now ranked by how rich they are, currently in a very primitive state and doesn't account for asset value

		Buying stocks:

		- Quick buy feature, a modal popup to quickly buy stocks without being redirected
		- A Stock history graph is now visible when viewing the detailed stock buy page
		- check to prevent users buying negative stocks (and many other checks to prevent similar problems)
		- detailed buy page no shows daily change
		- stocks are now ordered by how valuable they are, this is planned to be expanded on more
		- A total cost now displays and is updated when the user changes the quantity they are buying

		Trading accounts:

		- you can now set a default trading account, when you click the "trading accounts" button you will be directed to your default account     first, you can still switch between accounts or view them all with the "view all" button
		- you can see the value of each account you have on the view all page, on the account page you can see the total value on shares you  have bought.
		- various other minor visual changes and bug fixes

	v0.4 Alpha:

		- Added cards to display leaderboard, trading accounts and stock changes on homepage
		- users accounts value is now displayed on a graph on homepage
		- Stock Recommendations on home page (experimental)

		Leaderboard:

		- implemented the Datatables library to display the leaderboards
		- There are now 2 leader boards, 1)Funds and 2)Total asset value (all stocks value + funds)

		Stocks and shares:

		- re-worked the UI on the stock detail page, should no longer have to scroll to view full page
		- Added a filtering and searching function to sort through the stock list using Datatables
		- Added modal popup for selling shares

		Trading Accounts:

		- Fixed bug so default trading account is displayed first in lists
		- Added trading account name to the transaction history table
		- Upon trading account deletion, if user's have multiple trading accounts they can now select whether to sell all their shares or transfer them to another account
		- Fixed bug where other user's trading accounts could be viewed through url changes
		- Added a transfer shares button to transfer stocks between the trading account being viewed to another selected account through a popup

		Misc:

		- Fix floating point rounding, so values contain 2 numbers after decimal
		- Implemented a first time setup for users
		- Implemented better admin functionality, can now view models associated to users on their management page
