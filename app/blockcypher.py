import requests
from result import Err, Ok, Result


# https://api.blockcypher.com/v1/btc/main/addrs/1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD/balance
def get_btc_balance(address: str) -> Result[int, str]:
    try:
        r = requests.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance")
        return Ok(r.json()["final_balance"])
    except Exception as e:
        return Err(str(e))
