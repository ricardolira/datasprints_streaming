import random
import googlemaps
import json
import dotenv
import faust
import os
from faker import Faker


from sqlalchemy import create_engine
dotenv.load_dotenv()
engine = create_engine(os.environ['URI'])
gmaps = googlemaps.Client(key=os.environ['API_KEY'])
fake = Faker()

app = faust.App(
    'leader-streaming',
    broker='kafka://kafka:9092',
    value_serializar='raw',
)


@app.agent()
async def register_address_in_database(addresses):
    async for address in addresses:
        print(f"ADD ADDRESS TO DATABASE: {address}")
        address_data = json.loads(address)
        query = f"""
            insert into public.addresses (id, trips_id, address)
	        values (nextval('addresses_id_seq'), {address_data.get("id")}, '{address_data.get("address")}');
        """
        engine.execute(query)
        print("SUCCESS!!!")

@app.agent()
async def retrieve_address_from_coords(data_files):
    async for data_file in data_files:
        print(data_file)
        try:
            the_address = fake.address()
        except:
            the_address = "GOT AN ERROR"
        data = json.loads(data_file)
        raw_json_data = f'{{"address": "{the_address}", "id": {data.get("index")}}}'\
            .replace('\n', ' ')
        await register_address_in_database.send(value=raw_json_data)
#
#
@app.timer(2.0, on_leader=True)
async def receiver():
    # data_as_json = return_json_file()
    query = """
        select index, pickup_longitude, pickup_latitude
            from trips order by random() limit 1;
    """
    print("FETCHING NEW DATA!!")
    result = engine.execute(query)
    result = result.fetchone()
    index, pickup_longitude, pickup_latitude = result
    trip_data = f'{{"index": {index}, "pickup_longitude": {pickup_longitude}, "pickup_latitude": {pickup_latitude}}}'
    print(trip_data)
    await retrieve_address_from_coords.send(value=trip_data)
