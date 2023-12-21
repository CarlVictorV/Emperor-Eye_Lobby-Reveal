from core import connect
from gui import run_gui
from data import data_container
import asyncio

async def main():
    await connect()
    nameArr = data_container.updated_test()
    print("NameArr: ", nameArr)
    run_gui(nameArr)

if __name__ == "__main__":
    asyncio.run(main())