```python
from fastapi import FastAPI
app = FastAPI()

@app.get()
@app.post()
@app.put()
@app.delete()

@app.options()
@app.head()
@app.patch()
@app.trace()
# when using GraphQL you normally perform all the actions using only post.
# type hinting
# https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html

'''
pydantic ISSUE:

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None) -> Dict:
    return {"item_id": item_id, "q": q}


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Dict:
    return {"item_id": item_id}

override function, but the type check don't override accorddingly
'''


```