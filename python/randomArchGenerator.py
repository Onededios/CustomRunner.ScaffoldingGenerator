import os
import random
from faker import Faker
import json

fake = Faker()
base_path = "C:\\repos\\CustomRunner.ScaffoldingGenerator\\RandomFolderStructure"

step_template = {
    "test_name": "",
    "run_order": 0,
    "data_files": [],
    "folders": [],
    "extra_option_arguments": ""
}

def read_template():
    with open('templateTestSuit.json', 'r') as rf:
        return json.load(rf)

def read_collection():
    with open('templateCollection.json', 'r') as rf:
        return json.load(rf)

collection = read_collection()

def create_folder_structure():
    template = read_template()
    
    department = get_random_department()
    
    for i in range(random.randint(1, 6)):
        Faker.seed(random.randint(1, 10000))
        team = get_random_team()
        
        for j in range(random.randint(1, 4)):
            Faker.seed(random.randint(1, 10000))
            application = get_random_app()

            testSuitePath = os.path.join(base_path, department, team, application, "TestSuites")
            collectionPath = os.path.join(base_path, department, team, application, "Collections")
            
            os.makedirs(testSuitePath, exist_ok=True)
            os.makedirs(collectionPath, exist_ok=True)
            
            appName = application.lower()
            
            testFilePath = os.path.join(testSuitePath, f"{appName}.json")
            collectionFilePath = os.path.join(collectionPath, f"{appName}.postman_collection.json")
            print(collectionFilePath)
            
            template['api'] = appName
            template['collection_path'] = collectionFilePath
            
            create_file(testFilePath, update_test_suite_steps(template))
            create_file(collectionFilePath, collection)
    

def get_random_department():
    gen = fake.catch_phrase().title()
    print(f"Department: {gen}")
    return gen

def get_random_team():
    gen = fake.company().title()
    print(f"Team: {gen}")
    return gen

def get_random_app():
    gen = f"Test.{fake.word().capitalize()}.WebApi"
    print(f"App: {gen}")
    return gen

def get_random_test_name():
    gen = fake.sentence(nb_words=5).title().replace(".", "")
    print(f"Test: {gen}")
    return gen

def get_random_test_folder(iteration):
    return f"{iteration} - {fake.sentence(nb_words=3).title().replace('.', '')}"
    
def get_test_folders():
    folders = []
    for x in range(random.randint(1, 10)):
        Faker.seed(random.randint(1, 10000))
        folders.append(get_random_test_folder(x))
    
    return folders
    
def get_random_test_steps():
    steps = []
    for x in range(random.randint(1, 4)):
        Faker.seed(random.randint(1, 10000))
        new_step = step_template.copy()
        new_step['test_name'] = get_random_test_name()
        new_step['folders'] = get_test_folders()
        steps.append(new_step)
        
    return steps
    
def update_test_suite_steps(json):
    updated_json = json.copy()
    updated_json['steps'] = get_random_test_steps()
    return updated_json

def create_file(path, content):
    with open(path, 'w') as wf:
        json.dump(content, wf, indent=4)  # Corrected the parameter to 'indent'
    
if __name__ == "__main__":
    for x in range(10):
        Faker.seed(random.randint(1, 10000))
        create_folder_structure()
