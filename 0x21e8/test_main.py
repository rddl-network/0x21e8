from fastapi.testclient import TestClient

from main import app
from main import w3s
 
client = TestClient(app)

def test_read_valid():
    response = client.post("/store_data", 
        headers={"accept": "application/json", "Content-Type": "application/json" },
        json={"NFT_MetaDat" : "mytest", "NFT_emissions": 10 },
    )

def test_read_invalid():
    try:
        response = client.post("/store_data", 
            headers={"accept": "application/json", "Content-Type": "application/json" },
            json={"NFT_MetaDat" },
        )
    except TypeError:
        pass
    except:
        assert True