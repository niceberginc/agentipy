from decimal import Decimal

def from_readable_amount(amount: float, decimals: int) -> int:
    """
    Convert a human-readable token amount to its raw integer representation with proper decimal scaling.
    
    Args:
        amount: The human-readable amount (e.g., 1.5 ETH)
        decimals: The number of decimals used by the token (e.g., 18 for ETH)
    
    Returns:
        Integer representation of the amount with proper decimal scaling
    """
    # Convert to Decimal for precise calculation
    scale = 10 ** decimals
    # Convert to integer after scaling
    scaled_amount = Decimal(str(amount)) * Decimal(scale)
    # Return as string with no decimal part
    return str(int(scaled_amount))