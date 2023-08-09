import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from sqlalchemy.orm import Session
from database.database import database as get_db
import asyncio

loop = asyncio.get_event_loop()


class TestDateCalculation():
    def __init__(self,db:Session):
            self.db = db
            
            
    async def greeting(self):
        greeting = "hello world"
        return  greeting


    def main(self):
        result = loop.run_until_complete(self.greeting())
        


if __name__ == "__main__":
    cls = TestDateCalculation(db=get_db)
    cls.main()