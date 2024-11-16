
# city_dict = [city.to_dict() for city in state.cities]
#  is == to 
#  city_dict = []
# for city in state.cities:
#     city_dict.append(city.to_dict())

# city_dict = {city.id: city.to_dict() for city in state.cities}   # dict form
#  == with city_dict = {}
# for city in state.cities:
#     city_dict[city.id] = city.to_dict()
    
# return jsonify(city_dict)
