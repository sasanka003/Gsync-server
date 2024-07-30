def test_get_plantations(client):
    response = client.get("/plantations/all")
    
    