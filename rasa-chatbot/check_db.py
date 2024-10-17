from pymongo import MongoClient

def check_database():
    client = MongoClient('mongodb://root:example@localhost:27017/')
    db = client['car_ecommerce']
    
    # List all collections
    print("Collections in the database:")
    print(db.list_collection_names())
    
    # Count documents in the 'cars' collection
    cars_count = db.cars.count_documents({})
    print(f"Number of cars in the database: {cars_count}")
    
    # Sample query: Find all Toyota cars
    toyota_cars = list(db.cars.find({"brand": "Toyota"}))
    print(f"Number of Toyota cars: {len(toyota_cars)}")
    for car in toyota_cars:
        print(f"  - {car['model']}: ₱{car['price']:,}")

if __name__ == "__main__":
    check_database()