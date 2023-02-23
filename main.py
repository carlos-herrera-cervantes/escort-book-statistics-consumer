import asyncio

from consumers.operation_statistic_consumer import listen

if __name__ == '__main__':
    asyncio.run(listen())
