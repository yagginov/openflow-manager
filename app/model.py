import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class TrafficModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_trained = False

    def train(self, X, y):
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, sample):
        if not self.is_trained:
            raise Exception("Model is not trained yet.")
        sample = np.array(sample).reshape(1, -1)
        return self.model.predict(sample)[0]

def generate_mock_data():
    # Фейкові дані для тренування (розмір пакету, кількість пакетів, тривалість потоку)
    X = np.random.rand(500, 3) * 1000  # 500 зразків, 3 фічі
    y = np.random.choice([0, 1], size=(500,), p=[0.9, 0.1])  # 0 - норм, 1 - аномалія
    return X, y

if __name__ == "__main__":
    X, y = generate_mock_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = TrafficModel()
    model.train(X_train, y_train)

    acc = model.model.score(X_test, y_test)
    print(f"Test accuracy: {acc:.2f}")

    # Тестовий прогноз
    example = [400, 50, 200]  # умовний потік
    result = model.predict(example)
    print(f"Prediction for {example}: {'Anomaly' if result == 1 else 'Normal'}")
