from core import connect
from gui import run_testing_gui
from data import data_container
import asyncio

async def main():
    print("before tae")
    await connect()
    nameArr = data_container.updated_test()
    print("NameArr: ", nameArr)
    run_testing_gui(nameArr)

if __name__ == "__main__":
    asyncio.run(main())