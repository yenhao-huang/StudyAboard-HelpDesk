import os
import pandas as pd
import uuid

data = "../../data/docs/common_questions"

for file in os.listdir(data):
    if file.endswith(".csv"):
        file_path = os.path.join(data, file)
        df = pd.read_csv(file_path)
        df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_csv(file_path, index=False)
        print(f"Added UUIDs to {file_path}")

