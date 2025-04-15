from typing import Dict, Optional, Any


class BaseWalletClient:
    """Base wallet implementation that defines common methods."""
    
    def get_address(self) -> str:
        """Get the wallet address."""
        raise NotImplementedError("This method must be implemented by subclasses")
    
    def sign_message(self, message: str) -> Dict[str, str]:
        """Sign a message with the wallet's private key."""
        raise NotImplementedError("This method must be implemented by subclasses")
    
    def balance_of(self, address: str) -> Dict:
        """Get the balance of the specified address."""
        raise NotImplementedError("This method must be implemented by subclasses")
    
    def send_transaction(self, transaction: Any) -> Dict[str, str]:
        """Send a transaction."""
        raise NotImplementedError("This method must be implemented by subclasses") 