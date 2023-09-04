import importlib
import inspect

secret_var = 114

def test():
    pass

class a:
    secret_class_var = "secret"

class b:
    def __init__(self):
        pass

instance = b()

payload = {
    "__init__": {
        "__globals__": {
            "secret_var": 514,
            "a": {
                "secret_class_var": "Pooooluted ~"
            }
        }
    }
}

# Use inspect to check for potential supply chain pollution
def check_module(module):
    for _, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            args = [payload, instance]
            try:
                obj(*args)
            except Exception as e:
                print(f"Exception raised at function {obj.__name__}. It is likely safe. Reason: {str(e)}")

check_list = ["merge", "math"]
for item in check_list:
    module = importlib.import_module(item)
    check_module(module)
    if secret_var == 514:
        print(item, "I got you!!!")
        secret_var = 114

