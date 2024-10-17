from pymongo import MongoClient

class MongoConnector:
    def __init__(self):
        self.client = MongoClient('mongodb://root:example@localhost:27017/')
        self.db = self.client['car_ecommerce']

    def search_cars(self, brand):
        return list(self.db.cars.find({"brand": brand}))

    def get_car_info(self, model):
        return self.db.cars.find_one({"model": model})

    def get_car_price(self, brand, model):
        car = self.db.cars.find_one({"brand": brand, "model": model})
        return car['price'] if car else None

# Sample data insertion (you should replace this with your actual data)
    def insert_sample_data(self):
        cars = [
            {"brand": "Toyota", "model": "Vios", "year": 2023, "engine": "1.5L", "transmission": "CVT", "price": 755000},
            {"brand": "Honda", "model": "Civic", "year": 2023, "engine": "1.5L Turbo", "transmission": "CVT", "price": 1368000},
            {"brand": "Mitsubishi", "model": "Mirage", "year": 2023, "engine": "1.2L", "transmission": "CVT", "price": 711000},
            {"brand": "Ford", "model": "Everest", "year": 2023, "engine": "2.0L Turbo", "transmission": "10-speed AT", "price": 1999000},
            {"brand": "Hyundai", "model": "Accent", "year": 2023, "engine": "1.4L", "transmission": "6-speed AT", "price": 850000},
            {"brand": "Suzuki", "model": "Ertiga", "year": 2023, "engine": "1.5L", "transmission": "4-speed AT", "price": 968000}
        ]
        self.db.cars.insert_many(cars)

# Uncomment and run this once to insert sample data
# if __name__ == "__main__":
#     mongo = MongoConnector()
#     mongo.insert_sample_data()