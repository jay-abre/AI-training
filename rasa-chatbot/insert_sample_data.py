from pymongo import MongoClient

def insert_sample_data():
    client = MongoClient('mongodb://root:example@localhost:27017/')
    db = client['car_ecommerce']
    
    # Sample data
    cars = [
        {"brand": "Toyota", "model": "Vios", "year": 2023, "engine": "1.5L", "transmission": "CVT", "price": 755000},
        {"brand": "Honda", "model": "Civic", "year": 2023, "engine": "1.5L Turbo", "transmission": "CVT", "price": 1368000},
        {"brand": "Mitsubishi", "model": "Mirage", "year": 2023, "engine": "1.2L", "transmission": "CVT", "price": 711000},
        {"brand": "Ford", "model": "Everest", "year": 2023, "engine": "2.0L Turbo", "transmission": "10-speed AT", "price": 1999000},
        {"brand": "Hyundai", "model": "Accent", "year": 2023, "engine": "1.4L", "transmission": "6-speed AT", "price": 850000},
        {"brand": "Suzuki", "model": "Ertiga", "year": 2023, "engine": "1.5L", "transmission": "4-speed AT", "price": 968000},
        {"brand": "Toyota", "model": "Fortuner", "year": 2023, "engine": "2.8L Diesel", "transmission": "6-speed AT", "price": 1998000}
    ]
    
    # Insert the data
    result = db.cars.insert_many(cars)
    
    print(f"Inserted {len(result.inserted_ids)} documents into the database.")

if __name__ == "__main__":
    insert_sample_data()