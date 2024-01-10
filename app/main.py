from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
 
class Item(BaseModel):
    ID: int
    Name: str
    Price: int
 
app = FastAPI()
 
Item_list =[
    {"ID": 1,"Name":"Book","Price":150},
    {"ID": 2,"Name":"Pen","Price":50},
    {"ID": 3,"Name":"Phone","Price":100000},
    {"ID": 4,"Name":"table","Price":20000},
    ]  
 
df = pd.json_normalize(Item_list)
 
@app.get("/Items/")
async def items():    
    #return  Item_list
    return df.to_json(orient='records')

#curl http://localhost:8080/Items/{ID}
@app.get("/Items/{item_id}")
async def items(item_id: int):
    item = df[df['ID'] == item_id]
    if item.empty:
        return {"message": "Item not found"}
    return item.to_json(orient='records')

#curl -X POST -H "accept: application/json" -H "Content-Type: application/json" -d "{\"ID\":10, \"Name\":\"Sample\", \"Price\":123}" http://localhost:8080/Items/
@app.post("/Items/")
async def items(item: Item):
    #Item_list.append({"ID": item.ID,"Name":item.Name,"Price":item.Price})
    #return Item_list
    global df
    new_data = pd.DataFrame({"ID": [item.ID], "Name": [item.Name], "Price": [item.Price]})
    df = pd.concat([df, new_data], ignore_index=True)
    return df.to_json(orient='records')

#curl -X DELETE -H "accept: application/json" http://localhost:8080/Items/2
@app.delete("/Items/{item_id}")
async def items(item_id: int):
    global df
    df = df.drop(df.index[df["ID"]==item_id])
    return df.to_json(orient='records')