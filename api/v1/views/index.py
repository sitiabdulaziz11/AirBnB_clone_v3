from flask import jsonify


from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def index():
    """Retrieves the number of each object by type dynamically
    """
    results = {}
    
    # Initialize an empty dictionary to store the results
    for cls_name, clss in classes.items():
        key = f"{cls_name.lower()}s"
        results[key] = storage.count(clss)
    return jsonify(results)
    
    # results = {
    #     f"{cls_name.lower()}s": storage.count(cls)
    #     for cls_name, cls in classes.items()
    # }
    # # Return the results as JSON
    # # return {"status": "OK"}
    # return jsonify(results)
