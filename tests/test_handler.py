import json
import src.handler as handler

class FakeTable:
 def __init__(self): self.items=[]
 def put_item(self,Item): self.items.append(Item)
class FakeS3:
 def head_object(self,**kwargs): return {"ContentLength":42,"ContentType":"application/json"}
 def put_object(self,**kwargs): pass

def test_process_record(monkeypatch):
 fake=FakeS3(); monkeypatch.setattr(handler,"s3",fake)
 table=FakeTable()
 rec={"body":json.dumps({"Records":[{"s3":{"bucket":{"name":"source"},"object":{"key":"incoming%2Fdemo.json"}}}]})}
 result=handler.process_record(rec,table,"target")
 assert result[0]["status"]=="PROCESSED"
 assert table.items[0]["sizeBytes"]==42
